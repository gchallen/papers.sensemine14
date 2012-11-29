#!/usr/bin/env python
import os,sys,gzip,re,json,pickle
from datetime import datetime

"""Example of the log lines we are looking for:
3bfcc1ecaa7b79a1f8ab596ecb0b59b89d08560e  2012-11-18 00:00:56.578 21767 21767 I PhoneLabSystemAnalysis-Location: {"Action":"edu.buffalo.cse.phonelab.LOCATION_UPDATE","Location":"Location[mProvider=network,mTime=1353214856559,mLatitude=43.008654,mLongitude=-78.8087041,mHasAltitude=0.0,mHasSpeed=false,mSpeed=0.0,mHasBearing=false,mBearing=0.0,mHasAccuracy=true,mAccuracy=2033.0,mExtras=Bundle[mParcelledData.dataSize=212]]","LogFormatVersion":"1.0"}
7d27bc4cea99ce72041b14640511c6b233fab832  2012-11-18 00:01:05.843  6805  6805 I PhoneLabSystemAnalysis-Telephony: {"State":"DATA_DISCONNECTED","Action":"onDataConnectionStateChanged","LogFormatVersion":"1.0"}
6c0ef8dc70de4238bb59c545cf15d1b07d46de0a  2012-11-18 00:00:25.801  1098  1098 I PhoneLabSystemAnalysis-Wifi: {"State":"CONNECTING","Action":"android.net.wifi.STATE_CHANGE","LogFormatVersion":"1.0"}"""
LOGLINE_PATTERN = re.compile(r"""^
   (?P<hashed_ID>\w{40})\s+
   (?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)\s+(?P<hour>\d+):(?P<minute>\d+):(?P<second>\d+)\.(?P<millisecond>\d+)\s+
   (?P<process_id>\d+)\s+(?P<thread_id>\d+)\s+(?P<log_level>\w)\s+
   (?P<log_tag>.+?):\s+(?P<json>.*?)$""", re.VERBOSE)

# Example of location info: 
# "Location[mProvider=network,mTime=1353214856559,mLatitude=43.008654,mLongitude=-78.8087041,mHasAltitude=0.0,mHasSpeed=false,mSpeed=0.0,mHasBearing=false,mBearing=0.0,mHasAccuracy=true,mAccuracy=2033.0,mExtras=Bundle[mParcelledData.dataSize=212]]"
LOCATION_PATTERN = re.compile(r"""^Location\[(?P<loc_data>.*?),mExtras.*?\]$""", re.VERBOSE)

if len(sys.argv) <= 1:
  print >>sys.stderr, "Please define a DATA environment variable that points to a compressed PhoneLab output archive."
  sys.exit(-1)

# locations[device] = (start_time, end_time, geo_code)
locations = {}

# Just consider connected time for Wifi and Mobile
# Save time while changing CONNECTING to DISCONNECTED for Wifi
# Save time while changing DATA_CONNECTED to DATA_DISCONNECTED for mobile
# mobiles[device] = (start_time, end_time)
# wifies[device] = (start_time, end_time)
mobiles = {}
wifies = {}
for line in set(gzip.open(sys.argv[1], 'rb')):
  line = line.strip()
  logline_match = LOGLINE_PATTERN.match(line)
  if logline_match == None:
    continue

  if logline_match.group('log_tag') != 'PhoneLabSystemAnalysis-Location' and \
     logline_match.group('log_tag') != 'PhoneLabSystemAnalysis-Telephony' and \
     logline_match.group('log_tag') != 'PhoneLabSystemAnalysis-Wifi':
    continue

  try: 
    device_time = datetime(int(logline_match.group('year')),
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

  if logline_match.group('log_tag') == 'PhoneLabSystemAnalysis-Location':
    if not 'Location' in log_json:
      continue
    location_match = LOCATION_PATTERN.match(log_json['Location'])

    if location_match == None:
      continue

    location = dict(u.split("=") for u in location_match.group('loc_data').split(","))
    
    if not locations.has_key(device):
      locations[device] = []
    locations[device].append((device_time, location['mLatitude'], location['mLongitude']))

  elif logline_match.group('log_tag') == 'PhoneLabSystemAnalysis-Telephony':
    if not 'State' in log_json or log_json['Action'] != "onDataConnectionStateChanged":
      continue
    if not mobiles.has_key(device):
      mobiles[device] = []
    state = log_json['State']
    mobiles[device].append((device_time, state))

  elif logline_match.group('log_tag') == 'PhoneLabSystemAnalysis-Wifi':
    if not 'State' in log_json or log_json['Action'] != "android.net.wifi.STATE_CHANGE":
      continue
    if not wifies.has_key(device):
      wifies[device] = []
    state = log_json['State']
    wifies[device].append((device_time, state))
  else:
   continue


#sorting by date for manipulating mobiles and wifies
for device in locations.keys():
  locations[device] = sorted(locations[device], key=lambda i: i[0])
for device in mobiles.keys():
  mobiles[device] = sorted(mobiles[device], key=lambda i: i[0])
for device in wifies.keys():
  wifies[device] = sorted(wifies[device], key=lambda i: i[0])

#change format of mobiles and wifies data set
#mid_mobiles[device] = (start_time, end_time)
#mid_wifies[device] = (start_time, end_time)
mid_mobiles = {}
for device in mobiles.keys():
  if not mid_mobiles.has_key(device):
    mid_mobiles[device] = []
  set_record = False
  for d in mobiles[device]:
    if d[1] == 'DATA_CONNECTED':
      set_record = True
      start_time = d[0]
      continue
    elif d[1] == 'DATA_DISCONNECTED':
      if set_record:
        end_time = d[0]
        mid_mobiles[device].append((start_time, end_time))
        set_record = False
      continue
    else:
      continue

mid_wifies = {}
for device in wifies.keys():
  if not mid_wifies.has_key(device):
    mid_wifies[device] = []
  set_record = False
  for d in wifies[device]:
    if d[1] == 'CONNECTING':
      set_record = True
      start_time = d[0]
      continue
    elif d[1] == 'DISCONNECTED':
      if set_record:
        end_time = d[0]
        mid_wifies[device].append((start_time, end_time))
        set_record = False
      continue
    else:
      continue

#network_location[device] = (time, geocode, network_type)
network_locations = {}
for device in mid_mobiles.keys():
  if not locations.has_key(device):
    continue

  if not network_locations.has_key(device):
    network_locations[device] = []
  
  for time in mid_mobiles[device]:
    for location in locations[device]:
      if time[0] <= location[0] <= time[1]:
         network_locations[device].append((location[0], location[1], location[2], "mobile"))
      else:
        continue

for device in mid_wifies.keys():
  if not locations.has_key(device):
    continue

  if not network_locations.has_key(device):
    network_locations[device] = []
  
  for time in mid_wifies[device]:
    for location in locations[device]:
      if time[0] <= location[0] <= time[1]:
         network_locations[device].append((location[0], location[1], location[2], "wifi"))
      else:
        continue

#sorting by date for manipulating mobiles and wifies
for device in network_locations.keys():
  network_locations[device] = sorted(network_locations[device], key=lambda i: i[0])

#save dictionary to file
#pickle.dump(final_traffics, open('data.dat', 'wb'), -1)
