#!/usr/bin/env python

import argparse

from power.lib import * #@UnusedWildImport
from statistics.lib import * #@UnusedWildImport

parser = argparse.ArgumentParser()
args = parser.parse_args()

p = Power.load()
s = Statistic.load()

device_opportunistic = {}
opportunistic_per_day = {}

for d in p.devices:
  device_opportunistic[d] = 0
  opportunistic_per_day[d] = {}
  for day in s.experiment_days():
    opportunistic_per_day[d][day] = 0

total_charging = 0
total_opportunistic = 0
needed_opportunistic = 0

for extent in p.charging_extents:
  if extent.is_opportunistic():
    device_opportunistic[extent.device] += 1
    total_opportunistic += 1
    if extent.needed:
      needed_opportunistic += 1
    opportunistic_datetime = extent.start()
    opportunistic_day = datetime.datetime(opportunistic_datetime.year, opportunistic_datetime.month, opportunistic_datetime.day)
    opportunistic_per_day[extent.device][opportunistic_day] += 1
  total_charging += 1

opportunistic_devices = [device for device in device_opportunistic.keys() if device_opportunistic[device] > 0]
all_days = []
for device in opportunistic_per_day.keys():
  for day in s.experiment_days():
    all_days.append(opportunistic_per_day[device][day])
    
opportunistic_median_per_day = sorted(all_days)[len(all_days) / 2]
opportunistic_average_per_day = (sum(all_days) * 1.0) / len(all_days)
  
print """Of %d total charging cycles, %d (%d%%) were opportunistic, and %d (%d%%) of those opportunistic charges were needed.
%d participants engaged in opportunistic charging behavior an median of %d and average of %.1f times per day.""" % \
(total_charging,
total_opportunistic, int((total_opportunistic * 100.0) / total_charging),
needed_opportunistic, int((needed_opportunistic * 100.0) / total_opportunistic),
len(opportunistic_devices), opportunistic_median_per_day, opportunistic_average_per_day)