#!/usr/bin/env python

from applications.lib import Application
from power.lib import Power
from statistics.lib import Statistic
from telephony.lib import Telephony

Application.remove()
a = Application.load(verbose=True)
a.verbose = False
a.store()

Power.remove()
p = Power.load(verbose=True)
p.verbose = False
p.store()

Statistic.remove()
s = Statistics.load(verbose=True)
s.verbose = False
s.store()

Telephony.remove()
t = Telephony.load(verbose=True)
t.verbose = False
t.store()
