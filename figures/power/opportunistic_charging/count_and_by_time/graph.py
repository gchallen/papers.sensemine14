#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from power.lib import * #@UnusedWildImport

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

ax.set_xlabel('Call Length (min)')
ax.set_xscale('log')
ax.legend(loc=4)

fig.savefig('graph.pdf')