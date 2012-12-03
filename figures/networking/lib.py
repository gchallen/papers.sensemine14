#!/usr/bin/env python

import re, cPickle

from common import lib
from location.lib import DeviceLocation

class Networking:
  @classmethod
  def load(cls, path):
    return cPickle.load(open(path, 'rb'))
  
  def __init__(self, path):
    self.path = path
    self.tags = ['PhoneLabSystemAnalysis-Telephony', 'PhoneLabSystemAnalysis-Wifi', 'PhoneLabSystemAnalysis-Location',]
    self.devices = set([])
    
    self.data_sessions = []
    
  def process(self):
    
    wifi_states = {}
    threeg_states = {}
    
    for logline in lib.LogFilter(self.tags).generate_loglines():
      self.devices.add(logline.device)
      if logline.log_tag == 'PhoneLabSystemAnalysis-Telephony' and logline.json.has_key('State'):
        if logline.json['State'] == 'DATA_CONNECTED':
          if threeg_states.has_key(logline.device):
            continue
          threeg_states[logline.device] = ThreeGSession(logline)
        elif logline.json['State'] == 'DATA_DISCONNECTED':
          if not threeg_states.has_key(logline.device):
            continue
          else:
            threeg_states[logline.device].end = logline.datetime
            self.data_sessions.append(threeg_states[logline.device])
            del(threeg_states[logline.device])
      elif logline.log_tag == 'PhoneLabSystemAnalysis-Wifi' and logline.json != None and logline.json.has_key('State'):
        if logline.json['State'] == 'CONNECTED':
          if wifi_states.has_key(logline.device):
            if wifi_states[logline.device].bssid == WifiSession.get_bssid(logline):
              continue
          wifi_states[logline.device] = WifiSession(logline)
        elif logline.json['State'] == 'DISCONNECTED':
          if not wifi_states.has_key(logline.device):
            continue
          else:
            wifi_states[logline.device].end = logline.datetime
            self.data_sessions.append(wifi_states[logline.device])
            del(wifi_states[logline.device])
      elif logline.log_tag == 'PhoneLabSystemAnalysis-Location' and logline.json != None \
        and logline.json.has_key('Action') and logline.json['Action'] == 'edu.buffalo.cse.phonelab.LOCATION_UPDATE':
        
        if wifi_states.has_key(logline.device):
          wifi_states[logline.device].locations.append(DeviceLocation(logline))
        if threeg_states.has_key(logline.device):
          threeg_states[logline.device].locations.append(DeviceLocation(logline))
            
  def dump(self):
    cPickle.dump(self, open(self.path, 'wb'), cPickle.HIGHEST_PROTOCOL)

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

if __name__=="__main__":
  t = Networking('data.dat')
  t.process()
  t.dump()

  
