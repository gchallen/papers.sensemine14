#!/usr/bin/env python

import cPickle, argparse, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from common import graphing

parser = argparse.ArgumentParser()
args = parser.parse_args()

calls = cPickle.load(open('../data.dat', 'rb'))

call_count = {}
for c in calls:
  if not call_count.has_key(c.device):
    call_count[c.device] = 1
  else:
    call_count[c.device] += 1

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.hist([call_count[device] for device in call_count.keys()])

fig.savefig('graph.pdf')