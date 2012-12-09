#!/usr/bin/env python

import re

from common import lib
from location.lib import DeviceLocation

def label_line(logline):
  if logline.log_tag == 'PhoneLabSystemAnalysis-Telephony' and logline.json != None and logline.json.has_key('State'):
    return 'threeg_state'
  elif logline.log_tag == 'PhoneLabSystemAnalysis-Wifi' and logline.json != None and logline.json.has_key('State'):
    return 'wifi_state'
  elif logline.log_tag == 'PhoneLabSystemAnalysis-Location' and logline.json != None and \
       logline.json.has_key('Action') and logline.json['Action'] == 'edu.buffalo.cse.phonelab.LOCATION_UPDATE':
    return 'location'
  elif logline.log_tag == 'PhoneLabSystemAnalysis-Snapshot' and logline.json != None and logline.json.has_key('Taffic'):
    return 'traffic'
  return None

class Networking(lib.LogFilter):
  TAGS = ['PhoneLabSystemAnalysis-Telephony', 'PhoneLabSystemAnalysis-Wifi', 'PhoneLabSystemAnalysis-Location', 'PhoneLabSystemAnalysis-Snapshot']
  
  TRAFFIC_TYPE_PATTERN = re.compile(r"""Type: (?P<type>\w+), Rx: (?P<rx>\d+), Tx: (?P<tx>\d+)""")
  
  def __init__(self, **kwargs):
    self.reset()
    
    self.label_line = label_line
    super(Networking, self).__init__(self.TAGS, **kwargs)
  
  def reset(self):
    self.data_sessions = []
    self.data_usages = []
  
  def process_line(self, logline):
    if logline.label == 'threeg_state':
      if logline.json['State'] == 'DATA_CONNECTED':
        if self.threeg_states.has_key(logline.device):
          return
        self.threeg_states[logline.device] = ThreeGSession(logline)
      elif logline.json['State'] == 'DATA_DISCONNECTED':
        if not self.threeg_states.has_key(logline.device):
          return
        else:
          self.threeg_states[logline.device].end = logline.datetime
          self.data_sessions.append(self.threeg_states[logline.device])
          del(self.threeg_states[logline.device])
    elif logline.label == 'wifi_state':
      if logline.json['State'] == 'CONNECTED':
        if self.wifi_states.has_key(logline.device):
          if self.wifi_states[logline.device].bssid == WifiSession.get_bssid(logline):
            return
        self.wifi_states[logline.device] = WifiSession(logline)
      elif logline.json['State'] == 'DISCONNECTED':
        if not self.wifi_states.has_key(logline.device):
          return
        else:
          self.wifi_states[logline.device].end = logline.datetime
          self.data_sessions.append(self.wifi_states[logline.device])
          del(self.wifi_states[logline.device])
    elif logline.label == 'location':
      if self.wifi_states.has_key(logline.device):
        self.wifi_states[logline.device].locations.append(DeviceLocation(logline))
      if self.threeg_states.has_key(logline.device):
        self.threeg_states[logline.device].locations.append(DeviceLocation(logline))
    elif logline.label == 'traffic':
      self.usage_state.add(logline)
        
  def process(self, time_limit=None):
    self.reset()
    
    self.wifi_states = {}
    self.threeg_states = {}
    self.usage_state = UsageState()
    
    self.process_loop()
    self.data_usages = self.usage_state.data_usages
    
class NetworkSession(object):
  def __init__(self, logline):
    self.device = logline.device
    self.start = logline.datetime
    self.end = None
    self.locations = []

class WifiSession(NetworkSession):
  BSSID_PATTERN = re.compile(r"""BSSID:\s*(?P<bssid>[A-Fa-f0-9:]+),""")
  
  def __init__(self, logline):
    super(WifiSession, self).__init__(logline)
    self.bssid = WifiSession.get_bssid(logline)
    
  @classmethod
  def get_bssid(cls, logline):
    return WifiSession.BSSID_PATTERN.search(logline.log_message).group('bssid')

class ThreeGSession(NetworkSession):
  def __init__(self, logline):
    super(ThreeGSession, self).__init__(logline)

class UsageState(object):
  def __init__(self):
    self.devices = set([])
    self.total = {}
    self.threeg = {}
    self.data_usages = []
  
  def add(self, logline):
    match = Networking.TRAFFIC_TYPE_PATTERN.match(logline.json['Taffic'])
    if match == None:
      return
    if not logline.device in self.devices:
      self.total[logline.device] = []
      self.threeg[logline.device] = []
      self.devices.add(logline.device)
    
    total_len = len(self.total[logline.device])
    threeg_len = len(self.threeg[logline.device])
    
    if match.group('type') == 'mobile':
      if threeg_len > 0 and logline.datetime == self.threeg[logline.device][-1].datetime:
        pass
      elif total_len == 1 and threeg_len == 0:
        if (abs(logline.datetime - self.total[logline.device][0].datetime)).seconds == 0:
          self.threeg[logline.device].append(logline)
        else:
          self.total[logline.device] = []
      elif total_len == 2 and threeg_len == 1:
        if (abs(logline.datetime - self.total[logline.device][1].datetime)).seconds == 0:
          self.threeg[logline.device].append(logline)
        else:
          self.total[logline.device] = []
          self.threeg[logline.device] = []
      else:
        self.threeg[logline.device].append(logline)
    elif match.group('type') == 'total':
      if total_len > 0 and logline.datetime == self.total[logline.device][-1].datetime:
        pass
      elif total_len == 0 and threeg_len == 1:
        if (abs(logline.datetime - self.threeg[logline.device][0].datetime)).seconds == 0:
          self.total[logline.device].append(logline)
        else:
          self.threeg[logline.device] = []
      elif total_len == 1 and threeg_len == 2:
        if (abs(logline.datetime - self.threeg[logline.device][1].datetime)).seconds == 0:
          self.total[logline.device].append(logline)
        else:
          self.total[logline.device] = []
          self.threeg[logline.device] = []
      else:
        self.total[logline.device].append(logline)
    
    total_len = len(self.total[logline.device])
    threeg_len = len(self.threeg[logline.device])
    
    if total_len == 2 and threeg_len == 2:
      total_0_m = Networking.TRAFFIC_TYPE_PATTERN.match(self.total[logline.device][0].json['Taffic'])
      threeg_0_m = Networking.TRAFFIC_TYPE_PATTERN.match(self.threeg[logline.device][0].json['Taffic'])
      total_1_m = Networking.TRAFFIC_TYPE_PATTERN.match(self.total[logline.device][1].json['Taffic'])
      threeg_1_m = Networking.TRAFFIC_TYPE_PATTERN.match(self.threeg[logline.device][1].json['Taffic'])
      
      threeg = ThreeGUsage(logline.device,
                           int(threeg_1_m.group('rx')) - int(threeg_0_m.group('rx')),
                           int(threeg_1_m.group('tx')) - int(threeg_0_m.group('tx')),
                           self.threeg[logline.device][0].datetime,
                           self.threeg[logline.device][1].datetime)
      
      if threeg.tx >= 0 and threeg.rx >= 0:
        if threeg.tx > 0 or threeg.rx > 0:
          self.data_usages.append(threeg)
          
        wifi = WifiUsage(logline.device,
                         (int(total_1_m.group('rx')) - int(total_0_m.group('rx'))) - threeg.rx,
                         (int(total_1_m.group('tx')) - int(total_0_m.group('tx'))) - threeg.tx,
                         self.total[logline.device][0].datetime,
                         self.total[logline.device][1].datetime)
        if wifi.tx > 0 or wifi.rx > 0:
          self.data_usages.append(wifi)
      
      self.total[logline.device].pop(0)
      self.threeg[logline.device].pop(0)
      
class NetworkUsage(object):
  def __init__(self, device, rx, tx, start, end):
    self.device = device
    self.start = start
    self.end = end
    self.rx = rx
    self.tx = tx

class ThreeGUsage(NetworkUsage):
  def __init__(self, *args):
    super(ThreeGUsage, self).__init__(*args)
    
class WifiUsage(NetworkUsage):
  def __init__(self, *args):
    super(WifiUsage, self).__init__(*args)

if __name__=="__main__":
  Networking.load(verbose=True)