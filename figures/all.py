#!/usr/bin/env python
import sys, argparse

from applications.lib import Application
from power.lib import Power
from statistics.lib import Statistic
from telephony.lib import Telephony

parser = argparse.ArgumentParser()
parser.add_argument('--clean', action='store_true', default=False)
parser.add_argument('--reparse', action='store_true', default=False)
args = parser.parse_args()

if args.clean or args.reparse:
  Application.remove()
  Power.remove()
  Statistic.remove()
  Telephony.remove()

if args.clean:
  sys.exit(0)

try:
  a = Application.load(verbose=True)
  a.verbose = False
  a.store()
except Exception, e:
  print >>sys.stderr, "Application processing caused an exception: %s" % (e,)
  
try:
  p = Power.load(verbose=True)
  p.verbose = False
  p.store()
except Exception, e:
  print >>sys.stderr, "Power processing caused an exception: %s" % (e,)

try:
  s = Statistic.load(verbose=True)
  s.verbose = False
  s.store()
except Exception, e:
  print >>sys.stderr, "Statistic processing caused an exception: %s" % (e,)

try:
  t = Telephony.load(verbose=True)
  t.verbose = False
  t.store()
except Exception, e:
  print >>sys.stderr, "Telephony processing caused an exception: %s" % (e,)
