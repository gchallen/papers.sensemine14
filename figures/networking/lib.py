#!/usr/bin/env python

from common import lib
import cPickle

class Networking:
  @classmethod
  def load(cls, path):
    return cPickle.load(open(path, 'rb'))
  
  def __init__(self, path):
    self.path = path
    self.tags = ['PhoneLabSystemAnalysis-Telephony', 'SmsReceiverService']
    self.devices = set([])
    
  def process(self):
    for logline in lib.LogFilter(self.tags).generate_loglines():
      if logline.log_tag == 'PhoneLabSystemAnalysis-Telephony' and logline.json.has_key('State'):
        c.add(logline)
      elif logline.log_tag == 'SmsReceiverService' and logline.log_message == "onStart: #1 mResultCode: -1 = Activity.RESULT_OK":
        t.add(Text(logline.device, logline.datetime))
      self.devices.add(logline.device)

  def dump(self):
    cPickle.dump(self, open(self.path, 'wb'), cPickle.HIGHEST_PROTOCOL)
    
if __name__=="__main__":
  t = Networking('data.dat')
  t.process()
  t.dump()
