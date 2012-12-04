#!/usr/bin/env python

from common import lib

def label_line(logline):
  if logline.log_tag == 'PhoneLabSystemAnalysis':
    return 'in_experiment'
  return None

class Statistic(lib.LogFilter):
  
  TAGS = ['PhoneLabSystemAnalysis',]
  
  BATTERY_USAGE_THRESHOLD = 0.5;
  DATA_USAGE_THRESHOLD_BYTES = 1024;
  PHONE_USAGE_THRESHOLD_MIN = 5;
  SMS_USAGE_THRESHOLD_COUNT = 25;
  
  def __init__(self, **kwargs):
    
    self.active_devices = set([])
    self.experiment_devices = set([])
    self.num_experiment_devices = None
    self.experiment_length_days = None
    self.label_line = label_line
    
    super(Statistic, self).__init__(self.TAGS, **kwargs)
  
  def process_line(self, logline):
    if logline.label == 'in_experiment':
      self.experiment_devices.add(logline.device)
      
  def process(self):
    self.process_loop()
    self.num_experiment_devices = len(self.experiment_devices)
    time_diff = self.end_time - self.start_time
    self.experiment_length_days = round(time_diff.days + time_diff.seconds / (60.0 * 60.0 * 24.0), 2) 

if __name__=="__main__":
  Statistic.load(verbose=True)