#!/usr/bin/env python

import cPickle, re, itertools, datetime
from common import lib
from collections import defaultdict

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
    self.tags = ['PhoneLabSystemAnalysis-Snapshot', 'ActivityManager','PhoneStatusBar','PhoneLabSystemAnalysis-Misc',]
    self.devices = set([])
    self.start_time = None
    self.end_time = None
    
    self.applications = set([])
    self.system_applications = set([])
    
    self.device_applications = {}
    self.install_counts = {}
    self.coinstalled_applications = lib.AutoDict()
    
    self.popular_installs = []

    self.device_filtered_logs={}
    
  
  def process(self, time_limit=None):

    tmpmap={}
    lastadded=''
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

        
      
      if logline.log_tag == 'PhoneLabSystemAnalysis-Misc' or logline.log_tag == 'PhoneStatusBar' or  'START' in logline.line:

          if(logline.line) not in tmpmap:
                tmpmap[logline.line] = 1
                lastadded=logline.line
                if len(tmpmap) > 1000:
                    tmpmap={}
                    tmpmap[logline.line]=1
                devicename = logline.device
                if devicename in self.device_filtered_logs:
                    self.device_filtered_logs[devicename].append(logline.line)
                else:
                    newlist = []
                    newlist.append(logline.line)
                    self.device_filtered_logs[devicename] = newlist

    # processing app foreground time
    componentforgroundtime = dict()
    componentstarttimes = defaultdict(int)
    currentfgapp=None
    newfgapp=None
    screenontime=None
    screenofftime=None
    cumulativeontime=0
    newfgappontime=None
    appstartedstate = False
    screenonstate= False
    screenoffstate= False

    for dev in self.device_filtered_logs:
        for lgline in self.device_filtered_logs[dev]:
            if 'android.intent.action.SCREEN_ON' in lgline:
                ss = lgline.split()
                screenontime=datetime.datetime.strptime(ss[1]+ss[2], '%Y-%m-%d%H:%M:%S.%f')
                screenonstate = True
                screenoffstate = False
                appstartedstate = False
            elif 'START' in lgline:
                ss = lgline.split()
                tmpappstarttime = datetime.datetime.strptime(ss[1]+ss[2], '%Y-%m-%d%H:%M:%S.%f')
                clms = lgline.split()
                appstr = ' '.join(clms[8:])
                tmpappstr=appstr[1:appstr.find('}')]
                tmpappstrsplits=tmpappstr.split()
                for jj in tmpappstrsplits:
                    if jj.startswith('cmp'):
                        appcmp=jj.split('=')
                        newfgapp=appcmp[1][0:appcmp[1].find('/')]
                        componentstarttimes[newfgapp]+=1
                tmptimeactive=0.0
                if currentfgapp != None:
                    if appstartedstate:
                        tmptimeactive = (tmpappstarttime - newfgappontime).total_seconds()
                    elif screenonstate:
                        tmptimeactive = (tmpappstarttime - screenontime).total_seconds()

                    if screenoffstate:
                        tmptimeactive = 0.0;

                    if currentfgapp in componentforgroundtime:
                        cumutime = componentforgroundtime[currentfgapp]
                        cumutime += tmptimeactive
                        componentforgroundtime[currentfgapp] = cumutime
                    else:
                        componentforgroundtime[currentfgapp] = tmptimeactive

                    if screenonstate==True:
                        currentfgapp = newfgapp
                        newfgappontime = tmpappstarttime
                        appstartedstate=True

            elif 'android.intent.action.SCREEN_OFF' in lgline:
                if screenontime == None: continue
                if screenoffstate == True:continue
                screenoffstate = True
                screenonstate = False
                ss  =lgline.split()
                offtime=datetime.datetime.strptime(ss[1]+ss[2], '%Y-%m-%d%H:%M:%S.%f')
                if newfgapp!=None:
                    if appstartedstate:
                        appfgtime = (offtime-newfgappontime).total_seconds()
                    else:
                        appfgtime = (offtime-screenontime).total_seconds()

                    if newfgapp in componentforgroundtime:
                        cumutime = componentforgroundtime[newfgapp]
                        cumutime += appfgtime
                        componentforgroundtime[newfgapp] = cumutime
                    else:
                        componentforgroundtime[newfgapp] = appfgtime




      
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
  t.process()
  t.dump()
