import os
import json
import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict


def generateAppsList(path):

    for root, dirs, files in os.walk('.'):
        filelist = []
        deviceapps=defaultdict(int)
        devicelistinstalledapps=[]
        for name in files:
            extension = os.path.splitext(name)[1]
            if not "apps" in extension: continue
            filelist.append(os.path.join(root,name))

        for f in filelist:
            try:
                log = open(f,'r')
            except IOError:
                print 'File doesnot exist'
                break;
            name = os.path.basename(f)
            appnames = []
            installedapps = []
            for line in log:
                deviceapps[line.strip()]+=1
                installedapps.append(line.strip())
            devicelistinstalledapps.append(installedapps)
            log.close()

            for w in sorted(deviceapps, key=deviceapps.get, reverse=True):
                print w, deviceapps[w]

            print 'list size ' + str(len(devicelistinstalledapps))

generateAppsList('/home/ans25/theworks/logdata/test/Apps_Usage/')
