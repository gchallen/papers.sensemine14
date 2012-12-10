#!/usr/bin/env python

import argparse

from power.lib import * #@UnusedWildImport
from statistics.lib import * #@UnusedWildImport

parser = argparse.ArgumentParser()
args = parser.parse_args()

p = Power.load(verbose=True)
s = Statistic.load(verbose=True)

total = p.total(devices=s.active_devices)
experiment_total = p.total(devices=s.experiment_devices)

harness_total = p.package_total('android.uid.system', devices=s.active_devices) * 100.0 / total
experiment_total = p.package_total('edu.buffalo.cse.phonelab.systemanalysis', devices=s.experiment_devices) * 100.0 / experiment_total

harness_all = []
for device in s.active_devices:
  device_total = p.total(devices=[device])
  if device_total == 0.0:
    continue
  harness_all.append(p.package_total('android.uid.system', devices=[device]) * 100.0 / device_total)
harness_all = sorted(harness_all)
print harness_all[0], harness_all[-1]

experiment_all = []
for device in s.experiment_devices:
  device_total = p.total(devices=[device])
  if device_total == 0.0:
    continue
  experiment_all.append(p.package_total('edu.buffalo.cse.phonelab.systemanalysis', devices=[device]) * 100.0 / device_total)
experiment_all = sorted(experiment_all)
print experiment_all[0], experiment_all[-1]

print """Our experiment consumed on overall average of %.1f%% of the total power consumed by all phones that participated in our experiment.
The maximum consumed by any one device was %.1f%%.""" % (experiment_total, experiment_all[-1])

print """A conservative estimate of the energy consumed by our experimental harness is %.1f%% of the device total.
The maximum consumed by any one device was %.1f%%.""" % (harness_total, harness_all[-1])
