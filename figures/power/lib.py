#!/usr/bin/env python
import datetime

from common import lib

def label_line(logline):
  if logline.log_tag == 'PhoneLabSystemAnalysis-BatteryChange' and logline.json != None and logline.json.has_key('BatteryLevel'):
    return 'battery_level'
  elif logline.log_tag == 'PhoneLabSystemAnalysis-Snapshot' and logline.json != None:
    if logline.json.has_key('UidInfo'):
      return 'uidinfo'
    elif logline.json.has_key('ProcInfo'):
      return 'procinfo'
    elif logline.json.has_key('SensorInfo'):
      return 'sensorinfo'
    elif logline.json.has_key('PerSnapshotPerTypeInfo'):
      return 'breakdown'
  return None
  
class Power(lib.LogFilter):
  TAGS = ['PhoneLabSystemAnalysis-BatteryChange', 'PhoneLabSystemAnalysis-Snapshot',]
  EXTENT_BREAK_THRESHOLD = datetime.timedelta(hours=1)
  EXTENT_REJECTION_THRESHOLD = datetime.timedelta(minutes=1)
  UNNEEDED_OPPORTUNISTIC_THRESHOLD = datetime.timedelta(hours=24)
  
  def __init__(self, **kwargs):
    self.reset()
    
    self.label_line = label_line
    
    super(Power, self).__init__(self.TAGS, **kwargs)
  
  def reset(self):
    self.all_device_extents = {}
    self.filtered_device_extents = {}
    self.charging_extents = []
    self.discharging_extents = []
    self.processed = False
    
  def process_line(self, logline):
    if logline.label == 'battery_level':
      if not self.all_device_extents.has_key(logline.device):
        self.all_device_extents[logline.device] = []
      p = PowerState(logline)
      
      if p.plugged:
        if self.device_discharging.has_key(logline.device):
          if self.device_discharging[logline.device].time_length() >= Power.EXTENT_REJECTION_THRESHOLD:
            self.all_device_extents[logline.device].append(self.device_discharging[logline.device])
          del(self.device_discharging[logline.device])
        if not self.device_charging.has_key(logline.device):
          self.device_charging[logline.device] = ChargingExtent(p)
        else:
          if p.datetime - self.device_charging[logline.device].states[-1].datetime >= Power.EXTENT_BREAK_THRESHOLD:
            if self.device_charging[logline.device].time_length() >= Power.EXTENT_REJECTION_THRESHOLD:
              self.all_device_extents[logline.device].append(self.device_charging[logline.device])
            self.device_charging[logline.device] = ChargingExtent(p)
          else:
            self.device_charging[logline.device].states.append(p)
      else:
        if self.device_charging.has_key(logline.device):
          if self.device_charging[logline.device].time_length() >= Power.EXTENT_REJECTION_THRESHOLD:
            self.all_device_extents[logline.device].append(self.device_charging[logline.device])
          del(self.device_charging[logline.device])
        if not self.device_discharging.has_key(logline.device):
          self.device_discharging[logline.device] = DischargingExtent(p)
        else:
          if p.datetime - self.device_discharging[logline.device].states[-1].datetime >= Power.EXTENT_BREAK_THRESHOLD:
            if self.device_discharging[logline.device].time_length() >= Power.EXTENT_REJECTION_THRESHOLD:
              self.all_device_extents[logline.device].append(self.device_discharging[logline.device])
            self.device_discharging[logline.device] = DischargingExtent(p)
          else:
            self.device_discharging[logline.device].states.append(p)
              
  def process(self):
    self.reset()
    self.device_charging = {}
    self.device_discharging = {}
    
    self.process_loop()
    
    for device in self.device_charging.keys():
      if self.device_charging[device].time_length() >= Power.EXTENT_REJECTION_THRESHOLD:
        self.all_device_extents[device].append(self.device_charging[device])
    
    for device in self.device_discharging.keys():
      if self.device_discharging[device].time_length() >= Power.EXTENT_REJECTION_THRESHOLD:
        self.all_device_extents[device].append(self.device_discharging[device])
    
    self.filter_extents()
    self.set_all_extents()
    self.label_needed_extents()
    
  def filter_extents(self):
    for device in self.devices:
      if len(self.all_device_extents[device]) == 0:
        self.filtered_device_extents[device] = []
        continue
        
      current_extent = self.all_device_extents[device][0]
      self.filtered_device_extents[device] = []
      
      for other_extent in self.all_device_extents[device][1:]:
        
        if current_extent.__class__.__name__ != other_extent.__class__.__name__:
          self.filtered_device_extents[device].append(current_extent)
          current_extent = other_extent
          
        if (other_extent.states[0].datetime - current_extent.states[-1].datetime) < Power.EXTENT_BREAK_THRESHOLD:
          current_extent.states += other_extent.states
        else:
          self.filtered_device_extents[device].append(current_extent)
          current_extent = other_extent
      
      self.filtered_device_extents[device].append(current_extent)
      
  def set_all_extents(self): 
    for device in self.filtered_device_extents.keys():
      for extent in self.filtered_device_extents[device]:
        if isinstance(extent, ChargingExtent):
          self.charging_extents.append(extent)
        else:
          self.discharging_extents.append(extent)    
  
  def label_needed_extents(self):
    for extent in [e for e in self.charging_extents if e.is_opportunistic()]:
      for forward_extent in [e for e in self.filtered_device_extents[extent.device] if e.start() > extent.start()]:
        if forward_extent.min() < extent.battery_change():
          extent.needed = True
          break
        if forward_extent.max() > PowerExtent.CHARGED_THRESHOLD or \
          forward_extent.end() - extent.start() > self.UNNEEDED_OPPORTUNISTIC_THRESHOLD:
          break

  def battery_below_threshold(self, device, threshold):
    for p in self.device_power[device]:
      if p.battery_level < threshold:
        return True
    return False

class PowerExtent(object):
  CHARGED_THRESHOLD = 0.90
  
  def __init__(self, power_state):
    self.device = power_state.device
    self.states = [power_state,]
  
  def time_length(self):
    return self.states[-1].datetime - self.states[0].datetime
  
  def start(self):
    return self.states[0].datetime
  
  def end(self):
    return self.states[-1].datetime
  
  def max_battery_state(self):
    return max(self.states, key=lambda k: k.battery_level)
  
  def min_battery_state(self):
    return min(self.states, key=lambda k: k.battery_level)
  
  def max(self):
    return self.max_battery_state().battery_level
  
  def min(self):
    return self.min_battery_state().battery_level
  
class ChargingExtent(PowerExtent):
  OPPORTUNISTIC_THRESHOLD = 0.90
  OPPORTUNISTIC_LENGTH = datetime.timedelta(minutes=10)
  
  def __init__(self, power_state):
    self.needed = False
    return super(ChargingExtent, self).__init__(power_state)
  
  def battery_change(self):
    return self.max_battery_state().battery_level - self.min_battery_state().battery_level
  
  def is_opportunistic(self):
    return all([self.max_battery_state().battery_level >= ChargingExtent.OPPORTUNISTIC_THRESHOLD,
                self.time_length() >= ChargingExtent.OPPORTUNISTIC_LENGTH])
    
class DischargingExtent(PowerExtent):
  def __init__(self, power_state):
    return super(DischargingExtent, self).__init__(power_state)
  
  def battery_change(self):
    return self.min_battery_state().battery_level - self.max_battery_state().battery_level
  
class PowerState(object):
  def __init__(self, logline):
    self.device = logline.device
    self.datetime = logline.datetime
    self.battery_level = int(logline.json['BatteryLevel']) / 100.0
    self.plugged = logline.json['Plugged']
  
  def __eq__(self, other):
    return isinstance(other, PowerState) and self.device == other.device and self.datetime == other.datetime
  
  def __hash__(self):
    return hash((self.device, self.datetime))
    
if __name__=="__main__":
  Power.load(verbose=True)