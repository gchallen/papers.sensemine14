#!/usr/bin/env python

import argparse

from statistics.lib import * #@UnusedWildImport

parser = argparse.ArgumentParser()
args = parser.parse_args()

s = Statistic.load(verbose=True)

unused = ['PhoneStatusBar', 'LockPatternKeyguardView', 'SurfaceFlinger', 'NfcService', 'PhoneLabSystemAnalysis', 'PhoneLabSystemAnalysis-UidInfo', 'GoogleVoice']

sorted_tags = sorted(s.tag_counts.keys(), key=lambda k: s.tag_counts[k], reverse=True)
sorted_tags = [tag for tag in sorted_tags if tag not in unused]
total = sum([s.tag_counts[t] for t in sorted_tags])

f = open("table.tex", 'w')

print >>f, r"""\begin{table*}[t]
\begin{threeparttable}
{\small
\begin{tabularx}{\textwidth}{rrrX}"""

print >>f, r"""\multicolumn{1}{c}{\normalsize{\textbf{Tag Name}}} & """
print >>f, r"""\multicolumn{1}{c}{\normalsize{\textbf{Tag Count}}} & """
print >>f, r"""\multicolumn{1}{c}{\normalsize{\textbf{\%}}} & """
print >>f, r"""\multicolumn{1}{c}{\normalsize{\textbf{Description}}} \\"""
print >>f, r"""\toprule"""

tag_descriptions = {'PhoneLabSystemAnalysis-Snapshot': "Snapshots battery breakdown across components and applications. Polled every 15 minutes.",
                    'ActivityManager': "Records when applications are started.",
                    'PhoneLabSystemAnalysis-Wifi': "Logs connection state, scan information and signal strength.",
                    'PhoneLabSystemAnalysis-Telephony': "Records phone call state and radio signal strength.",
                    'PhoneLabSystemAnalysis-BatteryChange': "Logs every change to the battery level.",
                    'LocationManagerService': "Records when GPS is enabled and disabled.",
                    'PhoneLabSystemAnalysis-Location': "Passively logs all location updates.",
                    'PhoneLabSystemAnalysis-Misc': "Logs when the screen turns on and off.",
                    'SmsReceiverService': "Used to count text messages sent and received.",
                    'PhoneLabSystemAnalysis-Packages': "Records when applications and installed and removed."}

for tag in sorted_tags:
  print >>f, "\\texttt{%s} & \\num{%d} & %.1f & %s \\\\" % (tag, s.tag_counts[tag], s.tag_counts[tag] * 100.0 / total, tag_descriptions[tag])
  
print >>f, r"""\end{tabularx}
}
\caption{Log tag statistics for our experiment. \textnormal{\num{%d} log tags
were collected over %d days from %d users. In the interest of space, not all tags logged are included.}}
\end{threeparttable}
\end{table*}""" % (total, int(s.experiment_length_days), len(s.active_devices))