#!/usr/bin/env python

import argparse

from statistics.lib import * #@UnusedWildImport

parser = argparse.ArgumentParser()
args = parser.parse_args()

s = Statistic.load(verbose=True)

unused = ['PhoneStatusBar', 'LockPatternKeyguardView', 'SurfaceFlinger', 'NfcService']

sorted_tags = sorted(s.tag_counts.keys(), key=lambda k: s.tag_counts[k], reverse=True)
sorted_tags = [tag for tag in sorted_tags if tag not in unused]
total = sum([s.tag_counts[t] for t in sorted_tags])

f = open("table.tex", 'w')

print >>f, r"""\multicolumn{1}{c}{\textbf{Tag Name}} & """
print >>f, r"""\multicolumn{1}{c}{\textbf{Tag Count}} & """
print >>f, r"""\multicolumn{1}{c}{\textbf{\%}} & """
print >>f, r"""\multicolumn{1}{c}{\textbf{Description}} \\"""

for tag in sorted_tags:
  print >>f, "%s & \\num{%d} & %.1f & \\\\" % (tag, s.tag_counts[tag], s.tag_counts[tag] * 100.0 / total)
print >>f, "%% %d tags total, %d days, %d users" % (total, int(s.experiment_length_days), len(s.active_devices))
  