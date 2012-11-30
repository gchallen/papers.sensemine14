#!/usr/bin/env python

import cPickle, re, itertools, datetime
from common import lib

class Application:
  PACKAGENAME_PATTERN = re.compile(r"""PackageName:\s*(?P<packagename>[^,]+),""")
  PHONELAB_APPS = ['edu.buffalo.cse.phonelab.harness.participant', 
                   'edu.buffalo.cse.phonelab.harness.developer',
                   'edu.buffalo.cse.phonelab.services',
                   'edu.buffalo.cse.phonelab.systemanalysis']
  @classmethod
  def load(cls, path):
    return cPickle.load(open(path, 'rb'))
  
  def __init__(self, path):
    self.path = path
    self.tags = ['PhoneLabSystemAnalysis-Snapshot', ]
    self.devices = set([])
    self.start_time = None
    self.end_time = None
    
    self.applications = set([])
    self.system_applications = set([])
    
    self.device_applications = {}
    self.install_counts = {}
    self.coinstalled_applications = lib.AutoDict()
    
    self.popular_installs = []
    
  def process(self, time_limit=None):
    for logline in lib.LogFilter(self.tags).generate_loglines():
      
      if self.start_time == None:
        self.start_time = logline.datetime
      self.end_time = logline.datetime
      
      if time_limit != None and (self.end_time - self.start_time) >= time_limit:
        break
      
      if logline.log_tag == 'PhoneLabSystemAnalysis-Snapshot' and logline.json != None and logline.json.has_key('InstalledUserApp'):
        if not self.device_applications.has_key(logline.device):
          self.device_applications[logline.device] = set([])
        application = Application.PACKAGENAME_PATTERN.search(logline.log_message).group('packagename').strip()
        
        if not self.install_counts.has_key(application):
          self.install_counts[application] = 0
        
        if not application in self.device_applications[logline.device]:
          self.install_counts[application] += 1
          self.applications.add(application)
          
        self.device_applications[logline.device].add(application)
      elif logline.log_tag == 'PhoneLabSystemAnalysis-Snapshot' and logline.json != None and logline.json.has_key('InstalledSystemApp'):
        application = Application.PACKAGENAME_PATTERN.search(logline.log_message).group('packagename').strip()
        self.system_applications.add(application)
        
      self.devices.add(logline.device)
      
    for first_application, second_application in itertools.combinations(sorted(self.applications), 2):
      self.coinstalled_applications[first_application][second_application] = 0
    
    for device in self.device_applications.keys():  
      for first_application, second_application in itertools.combinations(sorted(self.device_applications[device]), 2):
        self.coinstalled_applications[first_application][second_application] += 1
    
    self.popular_installs = [app for app in reversed(sorted(list(self.applications), key=lambda k: self.install_counts[k])) if app not in self.PHONELAB_APPS]
                                                   
  def dump(self):
    cPickle.dump(self, open(self.path, 'wb'), cPickle.HIGHEST_PROTOCOL)

if __name__=="__main__":
  t = Application('data.dat')
  t.process(datetime.timedelta(hours=2))
  t.dump()
