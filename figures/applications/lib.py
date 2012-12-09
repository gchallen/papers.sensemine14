#!/usr/bin/env python


import re, itertools
from common import lib
from statistics.lib import *

def label_line(logline):
  if logline.log_tag == 'PhoneLabSystemAnalysis-Snapshot' and logline.json != None and logline.json.has_key('InstalledUserApp'):
    return 'installed_user_app'
  elif logline.log_tag == 'PhoneLabSystemAnalysis-Snapshot' and logline.json != None and logline.json.has_key('InstalledSystemApp'):
    return 'installed_system_app'
  elif logline.log_tag == 'ActivityManager' and Application.ACTIVITY_MANAGER_PATTERN.match(logline.log_message):
    return 'start_activity'
  elif logline.log_tag == 'PhoneLabSystemAnalysis-BatteryChange' and logline.json != None and logline.json.has_key('Plugged'):
    return 'battery_status'
  elif logline.log_tag == 'PhoneLabSystemAnalysis-Misc' and logline.json != None and logline.json.has_key('Action'):
    if logline.json['Action'] == 'android.intent.action.SCREEN_ON':
      return 'screen_on'
    elif logline.json['Action'] == 'android.intent.action.SCREEN_OFF':
      return 'screen_off'
  elif logline.log_tag == 'PhoneLabSystemAnalysis-Packages':
    return 'package_addremove'
  return None
  
class Application(lib.LogFilter):
  TAGS = ['PhoneLabSystemAnalysis-Snapshot','PhoneLabSystemAnalysis-Misc', 'ActivityManager', 'PhoneStatusBar', 'NfcService', 'PhoneLabSystemAnalysis-BatteryChange',]
  
  ACTIVITY_MANAGER_PATTERN = re.compile(r"""^START.*?cmp=(?P<cmp>[\w\.\/]+)""")
  
  PACKAGENAME_PATTERN = re.compile(r"""PackageName: (?P<packagename>[^,]+),""")
  PHONELAB_APPS = ['edu.buffalo.cse.phonelab.harness.participant', 
                   'edu.buffalo.cse.phonelab.harness.developer',
                   'edu.buffalo.cse.phonelab.services',
                   'edu.buffalo.cse.phonelab.systemanalysis']

  def __init__(self, **kwargs):
    self.applications = set([])
    self.system_applications = set([])
    self.device_applications = {}
    self.install_counts = {}
    self.coinstalled_applications = lib.AutoDict()
    self.popular_installs = []
    
    self.activities = []
    self.screen_states = []
    self.device_activities = {}
    self.device_screen_states = {}

    """09 Dec 2012 : GWA : FIXME
    self.device_package_management = {}"""

    self.label_line = label_line    
    super(Application, self).__init__(self.TAGS, **kwargs)
  
  def process_line(self, logline):
    if logline.device not in self.s.experiment_devices:
      return

    if logline.label == 'installed_user_app':
      if not self.device_applications.has_key(logline.device):
        self.device_applications[logline.device] = set([])
      application = Application.PACKAGENAME_PATTERN.match(logline.json['InstalledUserApp']).group('packagename').strip()
      
      if not self.install_counts.has_key(application):
        self.install_counts[application] = 0
      
      if not application in self.device_applications[logline.device]:
        self.install_counts[application] += 1
        self.applications.add(application)
        
      self.device_applications[logline.device].add(application)
    elif logline.label == 'installed_system_app':
      application = Application.PACKAGENAME_PATTERN.match(logline.json['InstalledSystemApp']).group('packagename').strip()
      self.system_applications.add(application)
    elif logline.label == 'start_activity':
      pass
    elif logline.label == 'screen_on':
      self.device_screen_states[logline.device] = ScreenState(logline.device, logline.datetime)
    elif logline.label == 'screen_off':
      if self.device_screen_states.has_key(logline.device):
        self.device_screen_states[logline.device].end = logline.datetime
        self.screen_states.append(self.device_screen_states[logline.device])
        del(self.device_screen_states[logline.device])

    """09 Dec 2012 : GWA : FIXME
    elif logline.label == 'package_addremove':
      if not logline.device in self.device_package_management:
        self.device_package_management[logline.device] = logline.json
      elif logline.json not in self.device_package_management[logline.device]:
        self.device_package_management[logline.device].append(logline.json)"""

  def process(self):
    self.s = Statistic.load()

    self.process_loop()
              
    for first_application, second_application in itertools.combinations(sorted(self.applications), 2):
      self.coinstalled_applications[first_application][second_application] = 0
    
    for device in self.device_applications.keys():  
      for first_application, second_application in itertools.combinations(sorted(self.device_applications[device]), 2):
        self.coinstalled_applications[first_application][second_application] += 1
    
    self.popular_installs = [app for app in reversed(sorted(list(self.applications), key=lambda k: self.install_counts[k])) if app not in self.PHONELAB_APPS]

    """ 09 Dec 2012 : GWA : FIXME
    for dev in self.device_package_management:
        installs = self.device_package_management[dev]"""

class ScreenState(object):
  def __init__(self, device, start):
    self.device = device
    self.start = start
    self.end = None
    
class Activity(object):
  def __init__(self, logline, match):
    self.device = logline.device
    self.start = logline.datetime
    self.end = None
    self.package = match.group('cmp').strip()
    
if __name__=="__main__":
  Application.load(verbose=True)
