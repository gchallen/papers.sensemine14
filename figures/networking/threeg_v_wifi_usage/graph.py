#!/usr/bin/env python

import sys, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from networking.lib import * #@UnusedWildImport
from common.graphing import cdf

n = Networking.load('../data.dat')

wifi_usage = {}
threeg_usage = {}

for device in n.devices:
  wifi_usage[device] = 0
  threeg_usage[device] = 0

for session in n.data_sessions:
  if isinstance(session, WifiSession):
    wifi_usage[session.device] += (session.end - session.start).seconds
  elif isinstance(session, ThreeGSession):
    threeg_usage[session.device] += (session.end - session.start).seconds

percent_threeg = [(float(threeg_usage[device]) / (wifi_usage[device] + threeg_usage[device]), device) for device in n.devices if wifi_usage[device] + threeg_usage[device] > 0.0]

fig = plt.figure()
ax = plt.subplot(111)

ax.plot(*cdf([percent[0] for percent in percent_threeg]))

fig.savefig('graph.pdf')
