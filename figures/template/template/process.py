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

if len(sys.argv) <= 1:
  print >>sys.stderr, "Please define a DATA environment variable that points to a compressed PhoneLab output archive."
  sys.exit(-1)

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
    charge_levels[device] = []
  charge_levels[device].append((device_time, charge_level))

for device in charge_levels.keys():
  charge_levels[device] = sorted(charge_levels[device], key=lambda i: i[0])

pickle.dump(charge_levels, open('data.dat', 'wb'), -1)
