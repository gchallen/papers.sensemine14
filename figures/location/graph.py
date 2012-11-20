#!/usr/bin/env python

import re,sys,numpy,pickle,argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('data')
parser.add_argument("--min_count", help="Minimum number of values required for inclusion in plot.", action='store', type=int, default=24)
args = parser.parse_args()

acc_levels = pickle.load(open(args.data, 'rb'))

acc_levels_network = acc_levels['network']
acc_levels_gps = acc_levels['gps']

print acc_levels_network
print acc_levels_gps

figure = plt.figure()
axes = figure.add_subplot(211)

# network
plt.subplot(211)
plt.bar(range(len(acc_levels_network)), acc_levels_network, align='center')
plt.xticks(range(len(acc_levels_network)), ["0-10","10-20","20-30","30-40","40-50","50-60","60-70","70-80","80-90","90-100","100+"], size='small')
plt.ylabel('Distribution (%)')
plt.xlabel('Accuracy intervals of network')


# GPS
plt.subplot(212)
plt.bar(range(len(acc_levels_gps)), acc_levels_gps, align='center')
plt.xticks(range(len(acc_levels_gps)), ["0-10","10-20","20-30","30-40","40-50","50-60","60-70","70-80","80-90","90-100","100+"], size='small')
plt.ylabel('Distribution (%)')
plt.xlabel('Accuracy intervals of GPS')

figure.savefig('simple.pdf')



