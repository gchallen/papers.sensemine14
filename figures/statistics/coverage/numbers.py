#!/usr/bin/env python

import argparse

from power.lib import * #@UnusedWildImport
from statistics.lib import * #@UnusedWildImport

parser = argparse.ArgumentParser()
args = parser.parse_args()

s = Statistic.load(verbose=True)
collected, total = s.log_coverage()

print """We estimate that we collected %.0f%% of the logs generated during our experiment.""" % (collected * 100.0 / total,) 
