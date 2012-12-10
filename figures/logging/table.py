#!/usr/bin/env python

import re, sys, argparse, cPickle

parser = argparse.ArgumentParser()
parser.add_argument('data', type=str, help='Pickle file to procses.')
args = parser.parse_args()

f = open(args.data, 'rb')

total_counts = cPickle.load(f)
counts = cPickle.load(f)

sorted_tags = sorted(counts.keys(), key=lambda k: counts[k], reverse=True)
cutoff = 20

f = open("table.tex", 'w')

print >>f, r"""\begin{table}[t]
\begin{threeparttable}
{\small
\begin{tabularx}{\columnwidth}{Xrr}"""

print >>f, r"""\multicolumn{1}{c}{\normalsize{\textbf{Tag Name}}} & """
print >>f, r"""\multicolumn{1}{c}{\normalsize{\textbf{Tag Count}}} & """
print >>f, r"""\multicolumn{1}{c}{\normalsize{\textbf{\%}}} \\"""
print >>f, r"""\toprule"""

count = 0
for tag in sorted_tags:
  if tag.startswith("PhoneLab") or tag.startswith("PHONELAB"):
    continue
  print_tag = re.sub("_", "\_", tag)
  print >>f, r"\texttt{%s} & \num{%d} & %.1f \\" % (print_tag, counts[tag], 100.0 * counts[tag] / total_counts)
  count += 1
  if count > cutoff:
    break

print >>f, r"""\end{tabularx}
}
\caption{Top %d log tags generated by Android. \textnormal{\PhoneLab{} has
collected \num{%d} log messages, of \num{%d} different types. Tags generated
by \PhoneLab{} tools and our usage experiment are ommitted.}}
\end{threeparttable}
\end{table}""" % (cutoff, total_counts, len(sorted_tags))
