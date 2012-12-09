#!/usr/bin/env python
import datetime, re

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
    self.all_device_uidpowers = {}
    self.filtered_device_uidpowers = {}
    self.all_device_breakdowns = {}
    self.filtered_device_breakdowns = {}
    
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
    elif logline.label == 'uidinfo':
      if not self.all_device_uidpowers.has_key(logline.device):
        self.all_device_uidpowers[logline.device] = []
        self.filtered_device_uidpowers[logline.device] = []
      u = UIDPower(logline)
      if u.type == UIDPower.UIDPOWER_TYPE:
        self.all_device_uidpowers[logline.device].append(UIDPower(logline))
    elif logline.label == 'breakdown':
      if not self.all_device_breakdowns.has_key(logline.device):
        self.all_device_breakdowns[logline.device] = []
        self.filtered_device_breakdowns[logline.device] = []
      s = PowerSnapshot(logline)
      if s.type == PowerSnapshot.POWERSNAPSHOT_TYPE:
        self.all_device_breakdowns[logline.device].append(PowerSnapshot(logline))
              
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
    self.filter_uidpowers()
    self.filter_breakdowns()
    
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
  
  def filter_uidpowers(self):
    for device in self.all_device_uidpowers.keys():
      new_uidpowers = []
      uidhash = {}
      for uidpower in self.all_device_uidpowers[device]:
        if not uidhash.has_key(uidpower.uid):
          uidhash[uidpower.uid] = uidpower
        else:
          if uidhash[uidpower.uid].start == uidpower:
            continue
          uidhash[uidpower.uid].minus(uidpower)
          if uidhash[uidpower.uid].is_valid():
            new_uidpowers.append(uidhash[uidpower.uid])
          uidhash[uidpower.uid] = uidpower
      self.filtered_device_uidpowers[device] = sorted(new_uidpowers, key=lambda k: k.start)
  
  def filter_breakdowns(self):
    for device in self.all_device_breakdowns.keys():
      new_breakdowns = []
      last_breakdown = None
      for breakdown in self.all_device_breakdowns[device]:
        if last_breakdown == None:
          last_breakdown = breakdown
        else:
          if breakdown.start == last_breakdown.start:
            continue
          last_breakdown.minus(breakdown)
          if last_breakdown.is_valid():
            new_breakdowns.append(last_breakdown)
          last_breakdown = breakdown
      self.filtered_device_breakdowns[device] = new_breakdowns
      
  def battery_below_threshold(self, device, threshold):
    for extent in self.filtered_device_extents[device]:
      if extent.min() < threshold:
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

class PowerSnapshot(object):
  PATTERN = \
    re.compile(r"""Type:[ ](?P<type>[^,]+),[ ]
                   AverageCostPerByte:[ ](?P<averagecostperbyte>[\d\.\-E]+),[ ]
                   TimeSince:[ ](?P<timesince>[\d\.\-E]+),[ ]
                   AppWifiRunning:[ ](?P<appwifirunning>[\d\.\-E]+),[ ]
                   PhoneOnTimeMs:[ ](?P<phoneontimems>[\d\.\-E]+),[ ]
                   PhoneOnPower:[ ](?P<phoneonpower>[\d\.\-E]+),[ ]
                   ScreenOnPower:[ ](?P<screenonpower>[\d\.\-E]+),[ ]
                   ScreenOnTimeMs:[ ](?P<screenontimems>[\d\.\-E]+),[ ]
                   RadioUsagePower:[ ](?P<radiousagepower>[\d\.\-E]+),[ ]
                   WifiRunningTimeMs:[ ](?P<wifirunningtimems>[\d\.\-E]+),[ ]
                   WifiPower:[ ](?P<wifipower>[\d\.\-E]+),[ ]
                   BtOnTimeMs:[ ](?P<btontimems>[\d\.\-E]+),[ ]
                   BtPower:[ ](?P<btpower>[\d\.\-E]+),[ ]
                   IdleTimeMs:[ ](?P<idletimems>[\d\.\-E]+),[ ]
                   IdlePower:[ ](?P<idlepower>[\d\.\-E]+)""", re.VERBOSE)
  
  MAX_INTERVAL = datetime.timedelta(minutes=60)
  POWERSNAPSHOT_TYPE = 'STATS_SINCE_CHARGED'
  
  ATTRIBUTES = ['app_wifi_running', 'phone_on_time_ms', 'phone_on_power', 'screen_on_time_ms', 'screen_on_power',
                'radio_usage_power', 'wifi_running_time_ms', 'wifi_power', 'bt_on_time_ms', 'bt_power',
                'idle_time_ms', 'idle_power']
  
  def __init__(self, logline):
    self.device = logline.device
    self.start = logline.datetime
    self.end = None
    
    snapshot_match = PowerSnapshot.PATTERN.match(logline.json['PerSnapshotPerTypeInfo'])
    if snapshot_match == None:
      print logline.json['PerSnapshotPerTypeInfo']

    self.type = snapshot_match.group('type')
    
    self.time_since = int(float(snapshot_match.group('timesince')))
    self.app_wifi_running = float(snapshot_match.group('appwifirunning'))
    self.phone_on_time_ms = int(float(snapshot_match.group('phoneontimems')))
    self.phone_on_power = float(snapshot_match.group('phoneonpower'))
    self.screen_on_time_ms = int(float(snapshot_match.group('screenontimems')))
    self.screen_on_power = float(snapshot_match.group('screenonpower'))
    self.radio_usage_power = float(snapshot_match.group('radiousagepower'))
    self.wifi_running_time_ms = int(float(snapshot_match.group('wifirunningtimems')))
    self.wifi_power = float(snapshot_match.group('wifipower'))
    self.bt_on_time_ms = int(float(snapshot_match.group('btontimems')))
    self.bt_power = float(snapshot_match.group('btpower'))
    self.idle_time_ms = int(float(snapshot_match.group('idletimems')))
    self.idle_power = float(snapshot_match.group('idlepower'))
  
  def minus(self, other):
    self.end = other.start
    for attribute in PowerSnapshot.ATTRIBUTES:
      setattr(self, attribute, getattr(other, attribute) - getattr(self, attribute))
  
  def is_valid(self):
    if self.end == None or self.end <= self.start or (self.end - self.start) >= PowerSnapshot.MAX_INTERVAL:
      return False
    
    for attribute in PowerSnapshot.ATTRIBUTES:
      if getattr(self, attribute) < 0.0:
        return False

    return True
  
  def total_power(self):
    if self.end == None:
      return None
    
    return self.phone_on_power + self.screen_on_power + self.radio_usage_power + self.wifi_power + self.bt_power + self.idle_power
  
  def __str__(self):
    return "%.20s : %s -> %s : " % (self.device, self.start, self.end,) + ",".join(["%s: %s" % (attribute, getattr(self, attribute),) for attribute in PowerSnapshot.ATTRIBUTES])
      
class UIDPower(object):
  MAX_INTERVAL = datetime.timedelta(minutes=60)
  
  UIDPOWER_TYPE = 'STATS_SINCE_CHARGED'
  UID_PATTERN = re.compile(r"""UID: (?P<uid>\d+), UidName: (?P<name>[^,]+),.*?PerUidPerTypeInfo: \[(?P<breakdown>.*?)\]""")
  BREAKDOWN_PATTERN = \
    re.compile(r"""Type:[ ](?P<type>[^,]+),[ ]
                   CpuTime:[ ](?P<cputime>[\d\.\-E]+),[ ]
                   CpuFgTime:[ ](?P<cpufgtime>[\d\.\-E]+),[ ]
                   WakelockTime:[ ](?P<wakelocktime>[\d\.\-E]+),[ ]
                   GpsTime:[ ](?P<gpstime>[\d\.\-E]+),[ ]
                   Power:[ ](?P<power>[\d\.\-E]+),[ ]
                   WifiRunningTimeMS:[ ](?P<wifirunningtime>[\d\.\-E]+)""", re.VERBOSE)
  
  ATTRIBUTES = ['cpu_time', 'cpu_fg_time', 'wakelock_time', 'gps_time', 'power',]
  
  def __init__(self, logline):
    self.device = logline.device
    self.start = logline.datetime
    self.end = None
    
    uid_match = UIDPower.UID_PATTERN.match(logline.json['UidInfo'])
    self.uid = int(uid_match.group('uid'))
    self.name = uid_match.group('name').strip()
    self.type = None
    
    for breakdown_match in UIDPower.BREAKDOWN_PATTERN.finditer(uid_match.group('breakdown')):
      if breakdown_match.group('type') == UIDPower.UIDPOWER_TYPE:
        self.type = breakdown_match.group('type').strip()
        self.cpu_time = int(float(breakdown_match.group('cputime')))
        self.cpu_fg_time = int(float(breakdown_match.group('cpufgtime')))
        self.wakelock_time = int(float(breakdown_match.group('wakelocktime')))
        self.gps_time = int(float(breakdown_match.group('gpstime')))
        self.power = float(breakdown_match.group('power'))
  
  def minus(self, other):
    self.end = other.start
    for attribute in UIDPower.ATTRIBUTES:
      setattr(self, attribute, getattr(other, attribute) - getattr(self, attribute))
    
  def is_valid(self):
    if self.end == None or self.end <= self.start or (self.end - self.start) >= UIDPower.MAX_INTERVAL:
      return False
    
    for attribute in UIDPower.ATTRIBUTES:
      if getattr(self, attribute) < 0.0:
        return False
      
    return True
  
  def __str__(self):
    return "%.20s : %s (%d),  %s -> %s : " % (self.device, self.name, self.uid, self.start, self.end,) + ",".join(["%s: %s" % (attribute, getattr(self, attribute),) for attribute in UIDPower.ATTRIBUTES])
  
class ProcPower(object):
  MAX_INTERVAL = datetime.timedelta(minutes=60)
  
  PROCPOWER_TYPE = 'STATS_SINCE_CHARGED'
  PROC_PATTERN = re.compile(r"""UID: (?P<uid>\d+), UidName: (?P<name>[^,]+),.*?PerUidPerTypeInfo: \[(?P<breakdown>.*?)\]""")
  BREAKDOWN_PATTERN = \
    re.compile(r"""Type:\s*(?P<type>[^,]+).*?
                   CpuTime:\s*(?P<cputime>\d+).*?
                   CpuFgTime:\s*(?P<cpufgtime>\d+).*?
                   WakelockTime:\s*(?P<wakelocktime>\d+).*?
                   GpsTime:\s*(?P<gpstime>\d+).*?
                   Power:\s*(?P<power>[\d\.]+).*?
                   WifiRunningTimeMS:\s*(?P<wifirunningtime>\d+)""", re.VERBOSE)
  
  ATTRIBUTES = ['cpu_time', 'cpu_fg_time', 'wakelock_time', 'gps_time', 'power',]
  
  def __init__(self):
    pass
