#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from power.lib import * #@UnusedWildImport
from statistics.lib import * #@UnusedWildImport

p = Power.load(verbose=True)
s = Statistic.load(verbose=True)

overall_time_bins = {}
distribution_time_bins = {}

interval_seconds = 600

start_day = s.experiment_days()[0]
end_day = start_day + datetime.timedelta(hours=24)

max_bin_count = ((end_day - start_day).days * 24 * 60 * 60 + (end_day - start_day).seconds)  / interval_seconds

for bin_count in range(max_bin_count):
  distribution_time_bins[bin_count] = None
  overall_time_bins[bin_count] = []
    
for extent in p.discharging_extents:
  if extent.end() < start_day or extent.start() > end_day:
    continue
  if extent.device not in s.experiment_devices:
    continue
  for state in extent.states:
    if state.datetime < start_day or state.datetime > end_day:
      continue
    time_bin = (state.datetime - start_day).seconds / interval_seconds
    overall_time_bins[time_bin].append(state)

for bin_count in range(max_bin_count):
  overall_time_bins[bin_count] = sorted(overall_time_bins[bin_count], key=lambda k: k.battery_level)


for bin_count in range(max_bin_count):
  bin_length = len(overall_time_bins[bin_count])
  bottom_quartile = int(0.25 * bin_length)
  top_quartile = bin_length - bottom_quartile
  median = int(0.5 * bin_length)
  distribution_time_bins[bin_count] = {'bottom_quartile': overall_time_bins[bin_count][bottom_quartile].battery_level * 100.0,
                                       'median': overall_time_bins[bin_count][median].battery_level * 100.0,
                                       'top_quartile': overall_time_bins[bin_count][top_quartile].battery_level * 100.0}
  
fig = plt.figure()
ax = fig.add_subplot(111)
tops = []
middles = []
bottoms = []

for bin_count in range(max_bin_count):
  time_count = bin_count * interval_seconds / (60.0 * 60.0)
  distribution = distribution_time_bins[bin_count]
  if distribution == None:
    continue
  tops.append((time_count, distribution['top_quartile']))
  middles.append((time_count, distribution['median']))
  bottoms.append((time_count, distribution['bottom_quartile']))
  
  ax.bar(time_count,
         (distribution['top_quartile'] - distribution['bottom_quartile']),
         interval_seconds / (60.0 * 60.0), distribution['bottom_quartile'], linewidth=0.0, color='lightblue')


ax.plot(*zip(*tops), color='blue', linewidth=1.0, label='Top Quartile')
ax.plot(*zip(*middles), color='black', linewidth=1.0, label='Median')
ax.plot(*zip(*bottoms), color='blue', linewidth=1.0, label='Bottom Quartile')

ax.axis(xmax=((max_bin_count * interval_seconds) / (60.0 * 60.0)))
ax.set_xlabel('Time (hours after midnight)')
ax.set_ylabel('% Charged')
ax.legend(loc=1, prop={'size': 9})
fig.subplots_adjust(left=0.10, right=0.97, top=0.97, bottom=0.12)
fig.set_size_inches(7.0, 3.5)
fig.savefig('graph.pdf')
