#!/usr/bin/env python

import re, itertools
from common import lib

class Application(lib.LogFilter):
  TAGS = ['PhoneLabSystemAnalysis-Snapshot']
  
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
    
    super(Application, self).__init__(self.TAGS, **kwargs)
    
  def process_line(self, logline):
    if logline.log_tag == 'PhoneLabSystemAnalysis-Snapshot' and logline.get_json() != None and logline.json.has_key('InstalledUserApp'):
      if not self.device_applications.has_key(logline.device):
        self.device_applications[logline.device] = set([])
      application = Application.PACKAGENAME_PATTERN.match(logline.json['InstalledUserApp']).group('packagename').strip()
      
      if not self.install_counts.has_key(application):
        self.install_counts[application] = 0
      
      if not application in self.device_applications[logline.device]:
        self.install_counts[application] += 1
        self.applications.add(application)
        
      self.device_applications[logline.device].add(application)
    elif logline.log_tag == 'PhoneLabSystemAnalysis-Snapshot' and logline.get_json() != None and logline.json.has_key('InstalledSystemApp'):
      application = Application.PACKAGENAME_PATTERN.match(logline.json['InstalledSystemApp']).group('packagename').strip()
      self.system_applications.add(application)
  
  def process(self):
    self.process_loop()
              
    for first_application, second_application in itertools.combinations(sorted(self.applications), 2):
      self.coinstalled_applications[first_application][second_application] = 0
    
    for device in self.device_applications.keys():  
      for first_application, second_application in itertools.combinations(sorted(self.device_applications[device]), 2):
        self.coinstalled_applications[first_application][second_application] += 1
    
    self.popular_installs = [app for app in reversed(sorted(list(self.applications), key=lambda k: self.install_counts[k])) if app not in self.PHONELAB_APPS]

if __name__=="__main__":
  Application.load()