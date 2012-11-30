#!/usr/bin/env python

import pydot, argparse
from applications.lib import * #@UnusedWildImport

parser = argparse.ArgumentParser()
parser.add_argument("--install_count_threshold", help="Minimum number of application installs required for inclusion in plot.",
                    action='store', type=int, default=10)
parser.add_argument("--probability_threshold", help="Joint probability thresholding required for inclusion in plot.",
                    action='store', type=float, default=0.9)
args = parser.parse_args()

applications = Application.load('../data.dat')

g = pydot.Dot()

seen_applications = {}
for first_app in applications.coinstalled_applications.keys():
  for second_app in applications.coinstalled_applications[first_app].keys():
    if first_app in Application.PHONELAB_APPS or second_app in Application.PHONELAB_APPS:
      continue
    if not seen_applications.has_key(first_app):
      seen_applications[first_app] = pydot.Node(first_app)
    if not seen_applications.has_key(second_app):
      seen_applications[second_app] = pydot.Node(second_app)
      
    first_app_count = applications.install_counts[first_app]
    second_app_count = applications.install_counts[second_app]
    coinstall_count = applications.coinstalled_applications[first_app][second_app]
    
    if first_app_count < args.install_count_threshold or second_app_count < args.install_count_threshold:
      continue
    
    first_app_probability = float(coinstall_count) / first_app_count
    second_app_probability = float(coinstall_count) / second_app_count
    
    if first_app_probability > args.probability_threshold: 
      g.add_edge(pydot.Edge(seen_applications[first_app], seen_applications[second_app],
                            weight=coinstall_count,
                            label='%.2f' % (first_app_probability,)))
    
    if second_app_probability > args.probability_threshold: 
      g.add_edge(pydot.Edge(seen_applications[second_app], seen_applications[first_app],
                            weight=coinstall_count,
                            label='%.2f' % (second_app_probability,)))

g.write_pdf('graph.pdf')