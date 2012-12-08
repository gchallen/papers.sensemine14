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
  
  def __init__(self, **kwargs):
    self.reset()
    
    self.label_line = label_line
    
    super(Power, self).__init__(self.TAGS, **kwargs)
  
  def reset(self):
    self.device_extents = {}
    
  def process_line(self, logline):
    if logline.label == 'battery_level':
      if not self.device_extents.has_key(logline.device):
        self.device_extents[logline.device] = []
      p = PowerState(logline)
      
      if p.plugged:
        if self.device_discharging.has_key(logline.device):
          if self.device_discharging[logline.device].time_length() >= Power.EXTENT_REJECTION_THRESHOLD:
            self.device_extents.append(self.device_discharging[logline.device])
          del(self.device_discharging[logline.device])
        if not self.device_charging.has_key(logline.device):
          self.device_charging[logline.device] = ChargingExtent(p)
        else:
          if p.datetime - self.device_charging[logline.device].states[-1].datetime >= Power.EXTENT_BREAK_THRESHOLD:
            if self.device_charging[logline.device].time_length() >= Power.EXTENT_REJECTION_THRESHOLD:
              self.device_extents.append(self.device_charging[logline.device])
            self.device_charging[logline.device] = ChargingExtent(p)
          else:
            self.device_charging[logline.device].states.append(p)
      else:
        if self.device_dcharging.has_key(logline.device):
          if self.device_charging[logline.device].time_length() >= Power.EXTENT_REJECTION_THRESHOLD:
            self.device_extents.append(self.device_charging[logline.device])
          del(self.device_charging[logline.device])
        if not self.device_discharging.has_key(logline.device):
          self.device_discharging[logline.device] = DischargingExtent(p)
        else:
          if p.datetime - self.device_discharging[logline.device].states[-1].datetime >= Power.EXTENT_BREAK_THRESHOLD:
            if self.device_discharging[logline.device].time_length() >= Power.EXTENT_REJECTION_THRESHOLD:
              self.device_extents.append(self.device_discharging[logline.device])
            self.device_discharging[logline.device] = DischargingExtent(p)
          else:
            self.device_discharging[logline.device].states.append(p)
              
  def process(self):
    self.reset()
    self.device_charging = {}
    self.device_discharging = {}
    
    self.process_loop()
  
  def battery_below_threshold(self, device, threshold):
    for p in self.device_power[device]:
      if p.battery_level < threshold:
        return True
    return False

class PowerExtent(object):
  def __init__(self, power_state):
    self.states = [power_state,]
  
  def time_length(self):
    return self.states[-1].datetime - self.states[0].datetime
   
class ChargingExtent(PowerExtent):
  def __init__(self, power_state):
    return super(PowerExtent, self).__init__(power_state)

class DischargingExtent(PowerExtent):
  def __init__(self, power_state):
    return super(PowerExtent, self).__init__(power_state)
  
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