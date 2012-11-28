#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from telephony.lib import * #@UnusedWildImport

t = Telephony.load('../data.dat')
calls, texts = t.calls, t.texts

call_counts = {}
text_counts = {}

for device in t.devices:
  call_counts[device] = 0
  text_counts[device] = 0
  
for call in calls:
  call_counts[call.device] += (call.end - call.start).seconds

for text in texts:
  text_counts[text.device] += 1

calls_by_device, texts_by_device = [], []

for device in t.devices:  
  calls_by_device.append(call_counts[device])
  texts_by_device.append(text_counts[device])

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.scatter(calls_by_device, texts_by_device)
ax.axis(xmin=-10, ymin=-10, xmax=1000, ymax=200)
ax.set_xlabel('Call Count')
ax.set_ylabel('Text Count')

fig.savefig('graph.pdf')
