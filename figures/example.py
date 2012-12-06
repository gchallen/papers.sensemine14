from statistics.lib import *
import os

os.environ['MOBISYS13_DATA'] = '/home/sonali/Desktop/ALL'

s = Statistic.load() # this may take a while on the first iteration
print("done")
