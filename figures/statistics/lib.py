#!/usr/bin/env python

import datetime, math #@UnusedImport

from common import lib #@UnusedImport
from power.lib import * #@UnusedWildImport
from telephony.lib import * #@UnusedWildImport

def label_line(logline):
  if logline.log_tag == 'PhoneLabSystemAnalysis':
    return 'in_experiment'
  elif logline.log_tag == 'SurfaceFlinger' and logline.log_message.startswith("Boot is finished"):
    return 'boot'
  elif logline.log_tag == 'ActivityManager' and logline.log_message.startswith("START {act=android.intent.action.ACTION_REQUEST_SHUTDOWN"):
    return 'shutdown'
  if logline.log_tag == 'ActivityManager':
    return 'log_count'
  return 'all'

class Statistic(lib.LogFilter):
  
  TAGS = ["PhoneLabSystemAnalysis", "PhoneLabSystemAnalysis-Wifi",
          "PhoneLabSystemAnalysis-Telephony", "PhoneLabSystemAnalysis-BatteryChange",
          "PhoneLabSystemAnalysis-Misc", "PhoneLabSystemAnalysis-Snapshot",
          "PhoneLabSystemAnalysis-Location", "PhoneLabSystemAnalysis-UidInfo",
          "PhoneLabSystemAnalysis-Packages", "PhoneLabSystemAnalysis-LocationTask",
          "PhoneLabSystemAnalysis-Apps", "PhoneLabSystemAnalysis-Storage",
          "PhoneLabSystemAnalysis-Traffic", "PhoneLabSystemAnalysis-SensorInfo",
          "PhoneLabSystemAnalysis-Media", "PhoneLabSystemAnalysis-ProcInfo", "ActivityManager",
          "SmsReceiverService", "GoogleVoice", "LocationManagerService",
          "LockPatternKeyguardView", "NfcService",
          "SurfaceFlinger", "PhoneStatusBar"]
  
  BATTERY_USAGE_THRESHOLD = 0.7;
  DATA_USAGE_THRESHOLD_BYTES = 1024;
  PHONE_USAGE_THRESHOLD_SEC = 300;
  SMS_USAGE_THRESHOLD_COUNT = 25;
  
  def __init__(self, **kwargs):
    
    self.reset()
    
    self.label_line = label_line
    super(Statistic, self).__init__(self.TAGS, **kwargs)
  
  def reset(self):
    self.active_devices = set([])
    self.experiment_devices = set([])
    self.num_experiment_devices = None
    self.experiment_length_days = None
    self.active_devices = set([])
    self.device_intervals = {}
    self.device_counts = {}
    self.tag_counts = {}
    self.total_count = 0
    
  def process_line(self, logline):
    if logline.label == 'in_experiment':
      self.experiment_devices.add(logline.device)
      self.online_state.add(logline)
    elif logline.label == 'boot' or logline.label == 'shutdown' or logline.label == 'log_count':
      self.online_state.add(logline)
    
    self.total_count += 1
    if not self.device_counts.has_key(logline.device):
      self.device_counts[logline.device] = 0
    if not self.tag_counts.has_key(logline.log_tag):
      self.tag_counts[logline.log_tag] = 0
    
    self.device_counts[logline.device] += 1
    self.tag_counts[logline.log_tag] += 1
    
  def set_active_devices(self):
    p = Power.load(verbose=self.verbose)
    battery_active_devices = set([])
    for device in self.experiment_devices:
      if p.battery_below_threshold(device, self.BATTERY_USAGE_THRESHOLD):
        battery_active_devices.add(device)
    
    t = Telephony.load(verbose=self.verbose)
    calls, texts = t.get_call_counts(), t.get_text_counts()
    
    telephony_active_devices = set([])
    for device in self.experiment_devices:
      if ( calls.has_key(device) and calls[device] > self.PHONE_USAGE_THRESHOLD_SEC * self.experiment_length_days ) or \
         ( texts.has_key(device) and texts[device] > self.SMS_USAGE_THRESHOLD_COUNT * self.experiment_length_days ):
        telephony_active_devices.add(device)
    
    self.active_devices = battery_active_devices.union(telephony_active_devices)
    self.store()
    
  def process(self):
    if self.processed:
      return
    
    self.reset()
    
    self.online_state = OnlineState()
    
    self.process_loop()
    
    self.device_intervals = self.online_state.device_intervals
    
    self.num_experiment_devices = len(self.experiment_devices)
    
    time_diff = self.end_time - self.start_time
    self.experiment_length_days = round(time_diff.days + time_diff.seconds / (60.0 * 60.0 * 24.0), 2)
    
    self.set_active_devices() 
  
  def experiment_days(self):
    day = datetime.datetime(self.start_time.year, self.start_time.month, self.start_time.day)
    days = [day,]
    while True:
      day += datetime.timedelta(days=1)
      if day >= self.end_time:
        break
      days.append(day)
    return days
  
class OnlineState(object):
  def __init__(self):
    self.devices = set([])
    self.current_intervals = {}
    self.device_intervals = {}
    
  def add(self, logline):
    if logline.device not in self.devices:
      self.device_intervals[logline.device] = []
      self.devices.add(logline.device)
    
    if logline.label == 'boot':
      self.current_intervals[logline.device] = DeviceOnline(logline.device)
      self.current_intervals[logline.device].boot = logline.datetime
    elif logline.label == 'shutdown' and self.current_intervals.has_key(logline.device):
      self.current_intervals[logline.device].shutdown = logline.datetime
      self.device_intervals[logline.device].append(self.current_intervals[logline.device])
      del(self.current_intervals[logline.device])
    elif ( logline.label == 'in_experiment' or logline.label == 'log_count' ) and self.current_intervals.has_key(logline.device):
      self.current_intervals[logline.device].add(logline.datetime, (logline.label == 'in_experiment'))
      
class DeviceOnline(object):
  LOG_INTERVAL = datetime.timedelta(seconds=30*60)
  
  def __init__(self, device):
    self.device = device
    self.boot = None
    self.shutdown = None
    self.experiment_intervals = set([])
    self.intervals = set([])
    
  def add(self, datetime, experiment):
    if datetime < self.boot:
      return
    minutes_since_boot = (datetime - self.boot).days * 24 * 60.0 + (datetime - self.boot).seconds / 60.0
    intervals_since_boot = int((minutes_since_boot) / (DeviceOnline.LOG_INTERVAL.seconds / 60.0))
    
    if experiment:
      self.experiment_intervals.add(intervals_since_boot)
    self.intervals.add(intervals_since_boot)
  
  def total_intervals(self):
    return math.ceil(((self.shutdown - self.boot).days * 24 * 60.0 + (self.shutdown - self.boot).seconds / 60.0) / (DeviceOnline.LOG_INTERVAL.seconds / 60.0))
  
  def experiment_coverage(self):
    return len(self.experiment_intervals) / self.total_intervals()
  
  def log_coverage(self):
    return len(self.intervals) / self.total_intervals()
    
if __name__=="__main__":
  Statistic.load(verbose=True)