#!/usr/bin/env python

from common import lib
from telephony.lib import Telephony

t = Telephony('data.dat')
t.process(lib.LogFilter(['PhoneLabSystemAnalysis-Telephony', 'SmsReceiverService']))
t.dump()