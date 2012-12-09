#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from power.lib import * #@UnusedWildImport
from statistics.lib import * #@UnusedWildImport

p = Power.load(verbose=True)
s = Statistic.load(verbose=True)

time_bins = []

active_devices = p.devices.intersection(s.active_devices)
start_day = s.experiment_days()[0]

for extent in p.discharging_extents:
  if extent.device not in active_devices:
    continue
    
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

fig.savefig('graph.pdf')