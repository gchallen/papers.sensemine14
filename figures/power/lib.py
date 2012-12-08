#!/usr/bin/env python

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
  return None
  
class Power(lib.LogFilter):
  TAGS = ['PhoneLabSystemAnalysis-BatteryChange', 'PhoneLabSystemAnalysis-Snapshot',]
  
  def __init__(self, **kwargs):
    self.reset()
    
    self.label_line = label_line
    
    super(Power, self).__init__(self.TAGS, **kwargs)
  
  def reset(self):
    self.device_power = {}
    
  def process_line(self, logline):
    if logline.label == 'battery_level':
      if not self.device_power.has_key(logline.device):
        self.device_power[logline.device] = []
      p = PowerState(logline)
      if self.device_power[logline.device] != p:
        self.device_power[logline.device].append(p)

  def process(self):
    self.reset()
    
    self.process_loop()
  
  def battery_below_threshold(self, device, threshold):
    for p in self.device_power[device]:
      if p.battery_level < threshold:
        return True
    return False

class PowerState(object):
  def __init__(self, logline):
    self.device = logline.device
    self.datetime = logline.datetime
    self.battery_level = int(logline.json['BatteryLevel']) / 100.0
  
  def __eq__(self, other):
    return isinstance(other, PowerState) and self.device == other.device and self.datetime == other.datetime
  
  def __hash__(self):
    return hash((self.device, self.datetime))
    
if __name__=="__main__":
  Power.load(verbose=True)