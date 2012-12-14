#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from power.lib import * #@UnusedWildImport
from statistics.lib import * #@UnusedWildImport

p = Power.load(verbose=True)
s = Statistic.load(verbose=True)

low_threshold = 0.15

device_under_time = {}
device_over_time = {}
device_gps_over_power = {}
device_gps_under_power = {}

for uidpower in p.all_uidpowers:
  if uidpower.get_gps_power() == 0.0:
    continue
  if not device_under_time.has_key(uidpower.device):
    device_under_time[uidpower.device] = 0
    device_over_time[uidpower.device] = 0
    device_gps_over_power[uidpower.device] = 0.0
    device_gps_under_power[uidpower.device] = 0.0
  
  if uidpower.under_threshold(low_threshold):
    device_under_time[uidpower.device] += (uidpower.end - uidpower.start).seconds
    device_gps_under_power[uidpower.device] += uidpower.get_gps_power()
  else:
    device_over_time[uidpower.device] += (uidpower.end - uidpower.start).seconds
    device_gps_over_power[uidpower.device] += uidpower.get_gps_power()

for device in device_under_time.keys():
  if device_under_time[device] == 0:
    continue
  device_gps_under_power[device] /= 1.0 * device_under_time[device]
  
for device in device_over_time.keys():
  if device_over_time[device] == 0:
    continue
  device_gps_over_power[device] /= 1.0 * device_over_time[device]

print device_gps_over_power
print device_gps_under_power