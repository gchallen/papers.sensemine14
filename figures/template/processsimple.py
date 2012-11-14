#!/usr/bin/env python

import os,sys,gzip,re,json,pickle
from datetime import datetime

"""Example of the log lines we are looking for:
3ddb921496c26db81aa7022893f07656e996b6e4  11-13 00:11:39.082 25378 25378 I PhoneLabSystemAnalysis-BatteryChange: {"Action":"android.intent.action.BATTERY_CHANGED","Temparature":260,"BatteryLevel":95,"Plugged":true}"""
  
LOGLINE_PATTERN = re.compile(r"""^
   (?P<hashed_ID>\w{40})\s+
   (?P<month>\d+)-(?P<day>\d+)\s+(?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+)\.(?P<millisecond>\d+)\s+
   (?P<process_id>\d+)\s+(?P<thread_id>\d+)\s+(?P<log_level>\w)\s+
   (?P<log_tag>.+?):\s+(?P<json>.*?)$""", re.VERBOSE)

f = gzip.open(sys.argv[1], 'rb')

charge_levels = {}

for line in f.readlines():
  line = line.strip()
  logline_match = LOGLINE_PATTERN.match(line)
  if logline_match == None:
    continue
  if logline_match.group('log_tag') != 'PhoneLabSystemAnalysis-BatteryChange':
    continue

  try:
    device_time = datetime(datetime.now().year,
                           int(logline_match.group('month')),
                           int(logline_match.group('day')),
                           int(logline_match.group('hour')),
                           int(logline_match.group('minute')),
                           int(logline_match.group('second')),
                           int(logline_match.group('millisecond')) * 1000)
    log_json = json.loads(logline_match.group('json'))
  except Exception, e:
    print >>sys.stderr, "Error processsing %s: %s" % (line, e)
    continue

  device = logline_match.group('hashed_ID')
  charge_level = log_json['BatteryLevel']

  if not charge_levels.has_key(device):
    charge_levels[device] = {}
  charge_levels[device][device_time] = charge_level
pickle.dump(charge_levels, 'simple.dat', -1)
