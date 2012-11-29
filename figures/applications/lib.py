#!/usr/bin/env python

import cPickle, re, itertools
from common import lib

class Application:
  PACKAGENAME_PATTERN = re.compile(r"""PackageName:\s*(?P<packagename>[^,]+),""")
  
  @classmethod
  def load(cls, path):
    return cPickle.load(open(path, 'rb'))
  
  def __init__(self, path):
    self.path = path
    self.tags = ['PhoneLabSystemAnalysis-Snapshot', ]
    self.devices = set([])
    
    self.applications = set([])
    self.device_applications = {}
    self.coinstalled_applications = lib.AutoDict()
    
  def process(self):
    for logline in lib.LogFilter(self.tags).generate_loglines():
      if logline.log_tag == 'PhoneLabSystemAnalysis-Snapshot' and logline.json != None and logline.json.has_key('InstalledUserApp'):
        if not self.device_applications.has_key(logline.device):
          self.device_applications[logline.device] = set([])
        application = Application.PACKAGENAME_PATTERN.search(logline.log_message).group('packagename').strip()
        self.device_applications[logline.device].add(application)
        self.applications.add(application)
      self.devices.add(logline.device)
    
    for first_application, second_application in itertools.combinations(sorted(self.applications), 2):
      self.coinstalled_applications[first_application][second_application] = 0
    
    for device in self.device_applications.keys():  
      for first_application, second_application in itertools.combinations(sorted(self.device_applications[device]), 2):
        self.coinstalled_applications[first_application][second_application] += 1
      
  def dump(self):
    cPickle.dump(self, open(self.path, 'wb'), cPickle.HIGHEST_PROTOCOL)

if __name__=="__main__":
  t = Application('data.dat')
  t.process()
  t.dump()
