#!/usr/bin/env python

from common import lib
from power.lib import Power
from telephony.lib import Telephony

def label_line(logline):
  if logline.log_tag == 'PhoneLabSystemAnalysis':
    return 'in_experiment'
  return None

class Statistic(lib.LogFilter):
  
  TAGS = ['PhoneLabSystemAnalysis',]
  
  BATTERY_USAGE_THRESHOLD = 0.7;
  DATA_USAGE_THRESHOLD_BYTES = 1024;
  PHONE_USAGE_THRESHOLD_SEC = 300;
  SMS_USAGE_THRESHOLD_COUNT = 25;
  
  def __init__(self, **kwargs):
    
    self.active_devices = set([])
    self.experiment_devices = set([])
    self.num_experiment_devices = None
    self.experiment_length_days = None
    self.active_devices = set([])
    
    self.label_line = label_line
    super(Statistic, self).__init__(self.TAGS, **kwargs)
  
  def process_line(self, logline):
    if logline.label == 'in_experiment':
      self.experiment_devices.add(logline.device)
  
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
    self.process_loop()
    self.num_experiment_devices = len(self.experiment_devices)
    time_diff = self.end_time - self.start_time
    self.experiment_length_days = round(time_diff.days + time_diff.seconds / (60.0 * 60.0 * 24.0), 2)
    
    self.set_active_devices() 

if __name__=="__main__":
  Statistic.load(verbose=True)