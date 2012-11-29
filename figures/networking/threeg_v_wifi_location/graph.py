#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from networking.lib import * #@UnusedWildImport
from location.lib import * #@UnusedWildImport
from location.maps import SUNYNorth, DAVIS_HALL

n = Networking.load('../data.dat')

wifi_locations = []
threeg_locations = []

for session in n.data_sessions:
  if isinstance(session, WifiSession):
    wifi_locations += session.locations
  elif isinstance(session, ThreeGSession):
    threeg_locations += session.locations

fig = plt.figure()
suny_north = SUNYNorth()

wifi_locations = [suny_north.m(l.lon, l.lat) for l in wifi_locations]
threeg_locations = [suny_north.m(l.lon, l.lat) for l in threeg_locations]

suny_north.m.imshow(suny_north.background, origin='upper')
suny_north.m.plot(*suny_north.m(DAVIS_HALL.lon, DAVIS_HALL.lat), color='b', marker='o')
suny_north.m.scatter(*zip(*wifi_locations), color='r')
suny_north.m.scatter(*zip(*threeg_locations), color='g')

fig.savefig('graph.pdf')
