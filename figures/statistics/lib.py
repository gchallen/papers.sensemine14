#!/usr/bin/env python

import os, cPickle, argparse, datetime
from common import lib

class Statistic:
  
  BATTERY_USAGE_THRESHOLD = 0.5;
  DATA_USAGE_THRESHOLD_BYTES = 1024;
  PHONE_USAGE_THRESHOLD_MIN = 5;
  SMS_USAGE_THRESHOLD_COUNT = 25;
  
  @classmethod
  def load(cls, path=None):
    if path == None:
      path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.dat')
    else:
      path = path
    return cPickle.load(open(path, 'rb'))
  
  def __init__(self, path=None):
    if path == None:
      self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data.dat')
    else:
      self.path = path
    self.tags = ['PhoneLabSystemAnalysis', ]
    self.devices = set([])
    self.start_time = None
    self.end_time = None
    
    self.active_devices = set([])
    self.experiment_devices = set([])
    
  def process(self, time_limit=None):
    for logline in lib.LogFilter(self.tags).generate_loglines(time_limit):
      if logline.log_tag == 'PhoneLabSystemAnalysis':
        if self.start_time == None:
          self.start_time = logline.datetime
        self.end_time = logline.datetime
        self.experiment_devices.add(logline.device)

  def num_devices(self):
    return len(self.experiment_devices)
  
  def experiment_length_days(self):
    time_diff = self.end_time - self.start_time
    return round(time_diff.days + time_diff.seconds / (60.0 * 60.0 * 24.0), 2) 
                                                         
  def dump(self):
    cPickle.dump(self, open(self.path, 'wb'), cPickle.HIGHEST_PROTOCOL)

if __name__=="__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--time_limit_hours", help="Hours to process.",
                    action='store', type=int, default=None)
  parser.add_argument("--experiment_count", help="Print number of devices in experiment.",
                    action='store_true', default=False)
  parser.add_argument("--experiment_length_days", help="Print length of experiment in days.",
                    action='store_true', default=False)
  args = parser.parse_args()
  
  time_limit = None
  if args.time_limit_hours != None:
    time_limit = datetime.timedelta(hours=args.time_limit_hours)

  if args.experiment_count:
    print Statistic.load().num_devices()
  elif args.experiment_length_days:
    print Statistic.load().experiment_length_days()
  else:
    t = Statistic()
    t.process(time_limit=time_limit)
    t.dump()
