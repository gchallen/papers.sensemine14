#!/usr/bin/env python

import cPickle, argparse, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from common import graphing

parser = argparse.ArgumentParser()
args = parser.parse_args()

calls = cPickle.load(open('data.dat', 'rb'))

received_lengths = [((c.end - c.start).seconds / 60.0) for c in calls if c.placed == False]
placed_lengths = [((c.end - c.start).seconds / 60.0) for c in calls if c.placed == True]

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.plot(*graphing.cdf(received_lengths), label='Received')
ax.plot(*graphing.cdf(placed_lengths), label='Placed')

ax.xlabel('Call Length (min)')
ax.set_xscale('log')
ax.legend(loc=4)

fig.savefig('graph.pdf')