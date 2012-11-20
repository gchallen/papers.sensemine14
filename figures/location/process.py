#!/usr/bin/env python

import os,sys,gzip,re,json,pickle,math
from datetime import datetime

"""Example of the log lines we are looking for:
3ddb921496c26db81aa7022893f07656e996b6e4  11-13 00:11:39.082 25378 25378 I PhoneLabSystemAnalysis-BatteryChange: {"Action":"android.intent.action.BATTERY_CHANGED","Temparature":260,"BatteryLevel":95,"Plugged":true}"""
  
LOGLINE_PATTERN = re.compile(r"""^
   (?P<hashed_ID>\w{40})\s+
   (?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)\s+(?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+)\.(?P<millisecond>\d+)\s+
   (?P<process_id>\d+)\s+(?P<thread_id>\d+)\s+(?P<log_level>\w)\s+
   (?P<log_tag>.+?):\s+(?P<json>.*?)$""", re.VERBOSE)

LOCATION_PATTERN = re.compile(r"""^Location\[(?P<loc_data>.*?),mExtras.*?\]$""", re.VERBOSE)

if len(sys.argv) <= 1:
  print >>sys.stderr, "Please define a DATA environment variable that points to a compressed PhoneLab output archive."
  sys.exit(-1)

f = gzip.open(sys.argv[1], 'rb')

charge_levels = {}

acc_levels_network = [];
acc_levels_gps = [];

for i in range(11):
    acc_levels_network.append(0)
    acc_levels_gps.append(0)

for line in f.readlines():
  line = line.strip()
  logline_match = LOGLINE_PATTERN.match(line)
  if logline_match == None:
    continue
  if logline_match.group('log_tag') != 'PhoneLabSystemAnalysis-Location':
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

  if log_json["Action"] == "edu.buffalo.cse.phonelab.LOCATION_UPDATE":
      location = log_json['Location']
      location_match = LOCATION_PATTERN.match(location)
      if location_match == None:
          print "no match"
          continue
    
      parsed_loc = dict(u.split("=") for u in location_match.group('loc_data').split(","))
      #print parsed_loc['mProvider'], " ", parsed_loc['mAccuracy']

      acc = float(parsed_loc['mAccuracy'])
      if parsed_loc['mProvider'] == 'gps':
        if acc >= 100:
            acc_levels_gps[10] += 1
        else:
            quotient = int(acc / 10)
            acc_levels_gps[quotient] += 1
      elif parsed_loc['mProvider'] == 'network':
          if (acc >= 100):
              acc_levels_network[10] += 1
          else:
              quotient = int(acc/10)
              acc_levels_network[quotient] += 1


      
print acc_levels_gps
print acc_levels_network

total_gps = sum(acc_levels_gps)
total_network = sum(acc_levels_network)
for i in range(11):
    acc_levels_gps[i] = math.ceil(float(acc_levels_gps[i]) * 100/total_gps)
    acc_levels_network[i] = math.ceil(float(acc_levels_network[i]) * 100/total_network)

data = {'gps': acc_levels_gps, 'network':acc_levels_network}

pickle.dump(data, open('data.dat', 'wb'), -1)


