#!/usr/bin/env python

import pickle, argparse, matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('data')
parser.add_argument("--min_count", help="Minimum number of values required for inclusion in plot.", action='store', type=int, default=24)
args = parser.parse_args()

charge_levels = pickle.load(open(args.data, 'rb'))

figure = plt.figure()
axes = figure.add_subplot(111)

for device in charge_levels.keys():
  if len(charge_levels[device]) < args.min_count:
    continue
  axes.plot([i[0] for i in charge_levels[device]], [i[1] for i in charge_levels[device]])

for label in axes.get_xticklabels():
  label.set_rotation(30)

figure.savefig('simple.pdf')
