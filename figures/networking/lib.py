#!/usr/bin/env python

import re

from common import lib
from location.lib import DeviceLocation

def label_line(logline):
  if logline.log_tag == 'PhoneLabSystemAnalysis-Telephony' and logline.json.has_key('State'):
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
  
  def __init__(self, **kwargs):
    
    self.data_sessions = []
    
    self.label_line = label_line
    super(Networking, self).__init__(self.TAGS, **kwargs)
  
  def process_line(self, logline):
    if logline.label == 'threeg_state':
      if logline.json['State'] == 'DATA_CONNECTED':
        if self.threeg_states.has_key(logline.device):
          continue
        self.threeg_states[logline.device] = ThreeGSession(logline)
      elif logline.json['State'] == 'DATA_DISCONNECTED':
        if not self.threeg_states.has_key(logline.device):
          continue
        else:
          self.threeg_states[logline.device].end = logline.datetime
          self.data_sessions.append(self.threeg_states[logline.device])
          del(self.threeg_states[logline.device])
    elif logline.label == 'wifi_state':
      if logline.json['State'] == 'CONNECTED':
        if self.wifi_states.has_key(logline.device):
          if self.wifi_states[logline.device].bssid == WifiSession.get_bssid(logline):
            continue
        self.wifi_states[logline.device] = WifiSession(logline)
      elif logline.json['State'] == 'DISCONNECTED':
        if not self.wifi_states.has_key(logline.device):
          continue
        else:
          self.wifi_states[logline.device].end = logline.datetime
          self.data_sessions.append(self.wifi_states[logline.device])
          del(self.wifi_states[logline.device])
    elif logline.label == 'traffic':
      if self.wifi_states.has_key(logline.device):
        self.wifi_states[logline.device].locations.append(DeviceLocation(logline))
      if self.threeg_states.has_key(logline.device):
        self.threeg_states[logline.device].locations.append(DeviceLocation(logline))
        
  def process(self, time_limit=None):
    
    self.wifi_states = {}
    self.threeg_states = {}
    self.traffic_states = {}
    
    self.process_loop()
    
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

class NetworkUsage(object):
  def __init__(self, device, rx, tx, start, end, is_wifi):
    self.device = device
    self.start = start
    self.end = end
    self.rx = rx
    self.tx = tx
    self.is_wifi = is_wifi
    
    if self.rx < 0 or self.tx < 0:
      raise Exception("Negative RX or TX for NetworkUsage object.") 
  
  def __str__(self):
    if self.is_wifi:
      return "%.20s : %s -> %s, %d/%d TX/RX over Wifi" % (self.device, self.start, self.end, self.tx, self.rx,)
    else:
      return "%.20s : %s -> %s, %d/%d TX/RX over 3G" % (self.device, self.start, self.end, self.tx, self.rx,)

if __name__=="__main__":
  Networking.load(verbose=True)