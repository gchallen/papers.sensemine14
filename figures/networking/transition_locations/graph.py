#!/usr/bin/env python

import sys, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from networking.lib import * #@UnusedWildImport
from location.lib import * #@UnusedWildImport
from location.maps import SUNYNorth, DAVIS_HALL

n = Networking.load()

print >>sys.stderr, "Starting."

long_device_sessions = {}

for d in n.devices:
  long_device_sessions[d] = []

for s in n.data_sessions:
  if (s.end - s.start).seconds >= 60 and len(s.locations) > 0:
    long_device_sessions[s.device].append(s)

fig = plt.figure()
suny_north = SUNYNorth()

count = 0
lines = []
for d in n.devices:
  for i in range(len(long_device_sessions[d])):
    try:
      l_0 = long_device_sessions[d][i]
      l_1 = long_device_sessions[d][i + 1]
    except:
      continue
    if l_0.__class__.__name__ == l_1.__class__.__name__:
      continue
    
    if (l_1.locations[0].datetime - l_0.locations[-1].datetime).seconds < 60 and \
        l_1.locations[0].dist(l_0.locations[-1]) * 1000.0 < 100.0:
      start = suny_north.m(l_1.locations[0].lon, l_1.locations[0].lat)
      end = suny_north.m(l_0.locations[-1].lon, l_0.locations[-1].lat)
      lines.append([[start[0], end[0]], [start[1], end[1]]])
      count += 1

print >>sys.stderr, count

# wifi_locations = [suny_north.m(l.lon, l.lat) for l in wifi_locations]
# threeg_locations = [suny_north.m(l.lon, l.lat) for l in threeg_locations]

suny_north.m.imshow(suny_north.background, origin='upper')
suny_north.m.plot(*suny_north.m(DAVIS_HALL.lon, DAVIS_HALL.lat), color='b', marker='o')
for line in lines:
  suny_north.m.plot(*line, color='b', marker='o')
fig.savefig('graph.pdf')
