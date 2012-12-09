#!/usr/bin/env python

import itertools

from common import lib #@UnusedImport
from statistics.lib import * #@UnusedWildImport

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
    
    self.popular_app_names = {}
    self.popular_app_names['com.google.android.apps.maps'] = 'Google Maps' 
    self.popular_app_names['com.facebook.katana'] = 'Facebook' 
    self.popular_app_names['com.google.android.youtube'] = 'Youtube' 
    self.popular_app_names['com.pandora.android'] = 'Pandora' 
    self.popular_app_names['com.jb.gosms'] = 'GO SMS' 
    self.popular_app_names['com.adobe.reader'] = 'Adobe Reader' 
    self.popular_app_names['com.skype.raider'] = 'Skype' 
    self.popular_app_names['com.twitter.android'] = 'Twitter' 
    self.popular_app_names['com.instagram.android'] = 'Instagram' 
    self.popular_app_names['com.infonow.bofa'] = 'Bank of America' 
    self.popular_app_names['com.android.chrome'] = 'Chrome Browser' 
    self.popular_app_names['com.dropbox.android'] = 'Dropbox' 
    self.popular_app_names['com.devuni.flashlight'] = 'Tiny Flashlight' 
    self.popular_app_names['com.jb.gosms.emoji'] = 'GO SMS Pro Emoji Plugin' 
    self.popular_app_names['com.google.zxing.client.android'] = 'Barcode Scanner'
    self.popular_app_names['com.imangi.templerun'] = 'Temple Run' 
    self.popular_app_names['com.google.android.apps.googlevoice'] = 'Google Voice' 
    self.popular_app_names['com.facebook.orca'] = 'Facebook Messenger' 
    self.popular_app_names['com.weather.Weather'] = 'The Weather Channel' 
    self.popular_app_names['com.google.android.street'] = 'Street View' 
    self.popular_app_names['com.netflix.mediaclient'] = 'Netflix' 
    self.popular_app_names['com.socialnmobile.dictapps.notepad.color.note'] = 'ColorNote' 
    self.popular_app_names['com.rovio.angrybirds'] = 'Angry Birds' 
    self.popular_app_names['com.amazon.mShop.android'] = 'Amazon Mobile' 
    self.popular_app_names['com.google.android.music'] = 'Google Play Music' 
    self.popular_app_names['com.google.android.apps.translate'] = 'Google Translate' 
    self.popular_app_names['com.google.android.apps.docs'] = 'Google Docs' 
    self.popular_app_names['com.amazon.kindle'] = 'Kindle' 
    self.popular_app_names['com.evernote'] = 'Evernote' 
    self.popular_app_names['com.andrewshu.android.reddit'] = 'reddit is fun' 
    self.popular_app_names['com.espn.score_center'] = 'ESPN ScoreCenter' 
    self.popular_app_names['com.zynga.words'] = 'Words With Friends' 
    self.popular_app_names['com.tencent.mobileqq'] = 'QQ2012' 
    self.popular_app_names['com.spotify.mobile.android.ui'] = 'Spotify' 
    self.popular_app_names['com.halfbrick.fruitninjafree'] = 'Fruit Ninja' 
    self.popular_app_names['com.blackboard.android'] = 'Blackboard Mobile' 
    self.popular_app_names['com.sportstracklive.stopwatch'] = 'StopWatch & Timer' 
    self.popular_app_names['com.kiragames.unblockmefree'] = 'Unblock Me' 
    self.popular_app_names['com.bigduckgames.flow'] = 'Flow' 
    self.popular_app_names['net.zedge.android'] = 'Zedge' 

    self.reset()

    self.label_line = label_line    
    super(Application, self).__init__(self.TAGS, **kwargs)
  
  def reset(self):
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
    
    super(Application, self).reset()
  
  def summary(self):
    return super(Application, self).summary() + """
%d applications, %d system applications. %d activities, %d screen states.""" % (len(self.applications),
                                                                                len(self.system_applications),
                                                                                len(self.activities),
                                                                                len(self.screen_states))
      
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
      activity = Activity(logline)
      if self.device_screen_states.has_key(logline.device):
        self.device_screen_states[logline.device].add(activity)
      self.activities.append(activity)
    elif logline.label == 'screen_on':
      self.device_screen_states[logline.device] = ScreenState(logline.device, logline.datetime)
    elif logline.label == 'screen_off':
      if self.device_screen_states.has_key(logline.device):
        self.device_screen_states[logline.device].end = logline.datetime
        self.screen_states.append(self.device_screen_states[logline.device])
        del(self.device_screen_states[logline.device])

  def process(self):
    self.s = Statistic.load()

    self.process_loop()
              
    for first_application, second_application in itertools.combinations(sorted(self.applications), 2):
      self.coinstalled_applications[first_application][second_application] = 0
    
    for device in self.device_applications.keys():  
      for first_application, second_application in itertools.combinations(sorted(self.device_applications[device]), 2):
        self.coinstalled_applications[first_application][second_application] += 1
    
    self.popular_installs = [app for app in reversed(sorted(list(self.applications), key=lambda k: self.install_counts[k])) if app not in self.PHONELAB_APPS]

class ScreenState(object):
  def __init__(self, device, start):
    self.device = device
    self.start = start
    self.end = None
    self.activities = []
  
  def add(self, activity):
    if activity in self.activities:
      return
    else:
      self.activities.append(activity)
      
class Activity(object):
  def __init__(self, logline):
    self.device = logline.device
    self.package = Application.ACTIVITY_MANAGER_PATTERN.match(logline.log_message).group('cmp').strip()
    self.start = logline.datetime
    
  def __eq__(self, other):
    return isinstance(other, Activity) and self.device == other.device and self.package == other.package and self.start == other.start
  
  def __hash__(self):
    return hash((self.device, self.package, self.start))
  
if __name__=="__main__":
  Application.load(verbose=True)
