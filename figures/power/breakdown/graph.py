#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from power.lib import * #@UnusedWildImport
from statistics.lib import * #@UnusedWildImport

colors = {'Display': 'coral',
          'Sleep': 'white',
          'Idle CPU': 'lightgrey',
          'Active CPU': 'darkgrey',
          'Idle Data': 'lightgreen',
          'Active Data': 'green',
          'Phone': 'yellow',
          'Idle Wifi': 'orange',
          'GPS': 'red',
          'Bluetooth': 'purple'}

p = Power.load(verbose=True)
s = Statistic.load(verbose=True)

breakdown = p.component_breakdown()
sorted_keys = sorted(breakdown.keys(), key=lambda k: breakdown[k], reverse=True)

fig = plt.figure()
ax = fig.add_subplot(111)

overall_bottom = 0.0
for key in sorted_keys:
  key_total = breakdown[key]
  if colors[key] == 'white':
    linewidth = 0.1
  else:
    linewidth = 0.0
  ax.bar(0.0, key_total, width=8.0, bottom=overall_bottom, linewidth=linewidth, color=colors[key], label="%s (%.1f%%)" % (key, key_total))
  overall_bottom += key_total

left = 10.0
for device in s.experiment_devices:
  overall_bottom = 0.0
  breakdown = p.component_breakdown(device)
  for key in sorted_keys:
    key_total = breakdown[key]
    if colors[key] == 'white':
      linewidth = 0.1
    else:
      linewidth = 0.0
    ax.bar(left, key_total, width=1.0, bottom=overall_bottom, linewidth=linewidth, color=colors[key], label="__none__")
    overall_bottom += key_total
  left += 1.0

ax.axis(ymin=0.0, ymax=100.0, xmin=0.0, xmax=len(s.experiment_devices) + 10.0)

ax.set_xticks([4,])
ax.set_xticklabels(["Entire Testbed"])
ax.legend(loc=6, bbox_to_anchor=(-0.6, 0.5), prop={'size': 10})
fig.subplots_adjust(left=0.4, right=0.95, top=0.9, bottom=0.1)
fig.set_size_inches(7.0, 3.5)
fig.savefig('graph.pdf')