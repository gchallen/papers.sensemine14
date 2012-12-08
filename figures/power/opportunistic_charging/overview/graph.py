#!/usr/bin/env python

import sys, matplotlib, argparse

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from power.lib import * #@UnusedWildImport

parser = argparse.ArgumentParser()
parser.add_argument("--date_offset", help="Offset from the first day of the trace to use.", action='store', type=int, default=0)
args = parser.parse_args()

p = Power.load()

start_day = datetime.datetime(year=p.start_time.year, month=p.start_time.month, day=p.start_time.day) + datetime.timedelta(days=args.date_offset)
end_day = start_day + datetime.timedelta(days=1)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)


ax.set_xlabel('Call Length (min)')
ax.set_xscale('log')
ax.legend(loc=4)

fig.savefig('graph.pdf')