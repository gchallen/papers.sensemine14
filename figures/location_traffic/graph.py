#!/usr/bin/env python

import re,sys,numpy,pickle,argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('data')
parser.add_argument("--min_count", help="Minimum number of values required for inclusion in plot.", action='store', type=int, default=10)
args = parser.parse_args()

traffics = pickle.load(open(args.data, 'rb'))

figure = plt.figure()
axes = figure.add_subplot(111)

for device in traffics.keys():
  if len(traffics[device]) < args.min_count:
    continue
  axes.plot([i[0] for i in traffics[device]], [(i[1]/1000) for i in traffics[device]], label='Mobile')
  axes.plot([i[0] for i in traffics[device]], [(i[2]/1000) for i in traffics[device]], linestyle='--', color='r', label='Wifi')

  for label in axes.get_xticklabels():
    label.set_rotation(30)
  axes.set_xlabel('Time')
  axes.set_ylabel('KBytes')
  axes.legend(loc='upper left')

  figure.savefig(device+'.pdf')
  axes.clear()

#figure.savefig('graph.pdf')
