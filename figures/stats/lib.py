#!/usr/bin/env python

import cPickle, argparse, datetime
from common import lib

class Statistic:
  
  BATTERY_USAGE_THRESHOLD = 0.5;
  DATA_USAGE_THRESHOLD_BYTES = 1024;
  PHONE_USAGE_THRESHOLD_MIN = 5;
  SMS_USAGE_THRESHOLD_COUNT = 25;
  
  @classmethod
  def load(cls, path):
    return cPickle.load(open(path, 'rb'))
  
  def __init__(self, path):
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
        self.experiment_devices.add(logline.device)
                                                         
  def dump(self):
    cPickle.dump(self, open(self.path, 'wb'), cPickle.HIGHEST_PROTOCOL)

if __name__=="__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--time_limit_hours", help="Hours to process.",
                    action='store', type=int, default=None)
  args = parser.parse_args()
  
  time_limit = None
  if args.time_limit_hours != None:
    time_limit = datetime.timedelta(hours=args.time_limit_hours)
  
  t = Statistic('data.dat')
  t.process(time_limit=time_limit)
  t.dump()
