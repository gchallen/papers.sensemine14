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

both = []
texts_only = []
calls_only = []

for device in t.devices:
  if call_counts[device] == 0 and text_counts[device] == 0:
    continue
  elif call_counts[device] != 0 and text_counts[device] != 0:
    both.append((call_counts[device], text_counts[device],))
  elif call_counts[device] == 0:
    texts_only.append((call_counts[device], text_counts[device],))
  elif text_counts[device] == 0:
    calls_only.append((call_counts[device], text_counts[device],))                                                    
 
fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.scatter(*zip(*both), label='Calls and Texts (%d)' % (len(both)))
ax.scatter(*zip(*texts_only), color='green', label='Texts Only (%d)' % (len(texts_only)))
ax.scatter(*zip(*calls_only), color='red', label='Calls Only (%d)' % (len(calls_only)))

ax.axis(xmin=-10, ymin=-10, xmax=1000, ymax=200)
ax.legend(loc='upper right')
ax.set_xlabel('Call Usage (min)')
ax.set_ylabel('Text Usage (count)')

fig.savefig('graph.pdf')
