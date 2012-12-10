#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from power.lib import * #@UnusedWildImport
from statistics.lib import * #@UnusedWildImport

p = Power.load(verbose=True)
s = Statistic.load(verbose=True)

device_opportunistic = {}

for d in p.devices:
  device_opportunistic[d] = 0

start_time = s.experiment_days()[0]
end_time = s.experiment_days()[0] + datetime.timedelta(hours=24)

for extent in p.charging_extents:
  if extent.start() > end_time:
    break
  if extent.is_opportunistic():
    device_opportunistic[extent.device] += 1
opportunistic_devices = [device for device in device_opportunistic.keys() if device_opportunistic[device] > 0]
opportunistic_devices = sorted(opportunistic_devices, key=lambda k: device_opportunistic[k])

fig = plt.figure()
ax = fig.add_subplot(111)

bottom = len(opportunistic_devices) - 1

print len(opportunistic_devices)

for device in opportunistic_devices:
  for extent in p.filtered_device_extents[device]:
    if not isinstance(extent, ChargingExtent):
      continue
    end = extent.end()
    if end > end_time:
      end = end_time
    bar_start = (extent.start() - start_time).seconds
    bar_width = (end - extent.start()).seconds
    ax.barh(bottom, bar_width, 1.0, bar_start)
  bottom -= 1
  
# ax.set_xlabel('Call Length (min)')
# ax.legend(loc=4)
fig.savefig('graph.pdf')