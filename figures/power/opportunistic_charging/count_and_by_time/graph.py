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
    bar_start = (start - start_time).seconds
    bar_width = (end - start).seconds
    if extent.is_opportunistic():
      if extent.needed:
        ax.barh(bottom, bar_width, 1.0, bar_start, linewidth=0.0, color='red', label='Opportunistic Needed')
      else:
        ax.barh(bottom, bar_width, 1.0, bar_start, linewidth=0.0, color='blue', label='Opportunistic Unneeded')
    else:
      ax.barh(bottom, bar_width, 1.0, bar_start, linewidth=0.0, color='grey', label='Habitual')
  for extent in p.filtered_device_extents[device]:
    if extent.end() < start_time:
      continue
    if extent.start() > end_time:
      continue
    points = []
    for state in extent.states:
      if state.datetime < start_time or state.datetime > end_time:
        continue
      print state.datetime, state.battery_level
      points.append(((state.datetime - start_time).seconds, bottom + state.battery_level))
    ax.plot(*zip(*points), color='black')
  bottom -= 1

ax.set_ylabel("Participants")
ax.set_xlabel("Time")
# fig.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
fig.set_size_inches(3.33, 9.25)
# ax.legend(loc=4)
fig.savefig('graph.pdf')