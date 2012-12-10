#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from power.lib import * #@UnusedWildImport
from statistics.lib import * #@UnusedWildImport

p = Power.load(verbose=True)
s = Statistic.load(verbose=True)

device_opportunistic = {}
devices = s.experiment_devices

for d in devices:
  device_opportunistic[d] = 0.0

start_time = s.experiment_days()[0]
end_time = s.experiment_days()[0] + datetime.timedelta(hours=24)

for extent in p.charging_extents:
  if extent.end() < start_time:
    continue
  if extent.start() > end_time:
    continue
  if extent.is_opportunistic():
    device_opportunistic[extent.device] += (extent.end() - extent.start()).seconds

opportunistic_devices = [device for device in device_opportunistic.keys() if device_opportunistic[device] > 0]
opportunistic_devices = sorted(opportunistic_devices, key=lambda k: device_opportunistic[k], reverse=True)

fig = plt.figure()
ax = fig.add_subplot(111)

bottom = len(opportunistic_devices) - 1

legend_done = {'Opportunistic Needed': False,
               'Opportunistic Unneeded': False,
               'Habitual': False,
               'Charge Level': False}
               
for device in opportunistic_devices:
  for extent in p.filtered_device_extents[device]:
    if not isinstance(extent, ChargingExtent):
      continue
    if extent.end() < start_time:
      continue
    if extent.start() > end_time:
      continue
    start = extent.start()
    if start < start_time:
      start = start_time
    end = extent.end()
    if end > end_time:
      end = end_time
    bar_start = (start - start_time).seconds / 60.0 / 60.0
    bar_width = (end - start).seconds / 60.0 / 60.0
    if extent.is_opportunistic():
      if extent.needed:
        legend = 'Opportunistic Needed'
        if not legend_done[legend]:
          legend_done[legend] = True
        else:
          legend = '__none__'
        ax.barh(bottom, bar_width, 1.0, bar_start, linewidth=0.0, color='red', label=legend)
      else:
        legend = 'Opportunistic Unneeded'
        if not legend_done[legend]:
          legend_done[legend] = True
        else:
          legend = '__none__'
        ax.barh(bottom, bar_width, 1.0, bar_start, linewidth=0.0, color='blue', label=legend)
    else:
      legend = 'Habitual'
      if not legend_done[legend]:
        legend_done[legend] = True
      else:
        legend = '__none__'
      ax.barh(bottom, bar_width, 1.0, bar_start, linewidth=0.0, color='grey', label=legend)
  for extent in p.filtered_device_extents[device]:
    if extent.end() < start_time:
      continue
    if extent.start() > end_time:
      continue
    points = []
    for state in extent.states:
      if state.datetime < start_time or state.datetime > end_time:
        continue
      points.append(((state.datetime - start_time).seconds / 60.0 / 60.0, bottom + state.battery_level))
    legend = 'Charge Level'
    if not legend_done[legend]:
      legend_done[legend] = True
    else:
      legend = '__none__'
    ax.plot(*zip(*points), color='black', label=legend)
  bottom -= 1

ax.axis(ymin=0, ymax=(len(opportunistic_devices) + 1), xmax=24.0)
ax.set_yticks([])
ax.set_ylabel("Participants")
ax.set_xlabel("Time (hours after midnight)")
fig.subplots_adjust(left=0.10, right=0.98, top=0.99, bottom=0.06)
fig.set_size_inches(3.33, 9.25)
ax.legend(loc=9, prop={'size': 10})
fig.savefig('graph.pdf')