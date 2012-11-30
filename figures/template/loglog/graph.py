#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

figure = plt.figure()
axes = figure.add_subplot(111)

xs = range(20)

def y(x, a, b):
  return x * a + b

for b in range(-5, 6):
  axes.plot(xs, [y(x, 1, b) for x in xs])

axes.axis(xmin=0, xmax=10, ymin=-5, ymax=15)

axes.set_xscale('log')
axes.set_yscale('log')

figure.savefig('graph.pdf')
