#!/usr/bin/env python

import sys, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from networking.lib import * #@UnusedWildImport
from location.lib import * #@UnusedWildImport
from location.maps import SUNYNorthSpine as Map

n = Networking.load()

print >>sys.stderr, "Starting."

long_device_sessions = {}

for d in n.devices:
  long_device_sessions[d] = []

for s in n.data_sessions:
  if (s.end - s.start).seconds >= 60 and len(s.locations) > 0:
    long_device_sessions[s.device].append(s)

fig = plt.figure()
map = Map()

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
      start = map.m(l_1.locations[0].lon, l_1.locations[0].lat)
      end = map.m(l_0.locations[-1].lon, l_0.locations[-1].lat)
      if isinstance(l_0, WifiSession):
        lines.append([[start[0], end[0]], [start[1], end[1]]])
      else:
        lines.append([[start[1], end[1]], [start[0], end[0]]])
      count += 1

print >>sys.stderr, count

map.m.imshow(map.background, origin='upper')
for line in lines:
  map.m.plot(*line, color='black')
  map.m.plot(*line[0], color='red', marker='o')
  map.m.plot(*line[1], color='blue', marker='x')

fig.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
width, height = 7.0, 7.0 * ((map.height * 1.0) / map.width)
print width, height
fig.set_size_inches(width, height)
fig.savefig('graph.pdf')