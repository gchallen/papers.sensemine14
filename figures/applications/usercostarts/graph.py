#!/usr/bin/env python

import pydot, argparse
from applications.lib import * #@UnusedWildImport
from collections import defaultdict
from common import lib





appnames = {}

f = open('appnames.txt','r')
for line in f:
    key = line.split('=')[0].strip()
    val = line.split('=')[1].strip()
    appnames[key] = val
f.close()




SANE_SESSION_LENGTH = 3600

#Application.remove()
applications = Application.load()

app_total_start_count = defaultdict(int)

costartedapps = {}

tmp = defaultdict(int)

allapps = []

for a in applications.applications:
    allapps.append(a)

for a in applications.system_applications:
    allapps.append(a)


appstartcount = defaultdict(int)

print len(applications.screen_states)


devicecostarts = {}
deviceappstartcounts = {}

for session in applications.screen_states:
    if (session.end - session.start).total_seconds() > SANE_SESSION_LENGTH:
        continue
    
    device = None
    unique = []

    for activity in session.activities:
        if activity.package == 'com.android.launcher' or activity.package == 'com.gau.go.launcherex' or activity.package == 'android':
            continue
        device = activity.device

        if not deviceappstartcounts.has_key(device):
            x = defaultdict(int)
            deviceappstartcounts[device] = x

        if not devicecostarts.has_key(device):
            y = defaultdict(int)
            devicecostarts[device] = y
        
        if activity.package not in unique:
            unique.append(activity.package)
            deviceappstartcounts[device][activity.package] +=1

    for x in range(0,len(unique)):
        for y in range(x+1,len(unique)):
            ke = unique[x] + ' ' + unique[y]
            devicecostarts[device][ke] += 1

f = open('table.tex','w')

header = '''
\\begin{table}
\\centering
\\begin{tabular}{lllc}
\\toprule[1.5pt]
\\multicolumn{1}{l}{Device} & \\multicolumn{1}{l}{First App} & \\multicolumn{1}{l}{Second App} & \\multicolumn{1}{c}{Percent}\\\\
\\midrule
'''
f.write(header)

c = '''\\bottomrule[1.5pt]
\\end{tabular}
\\caption{Table shows the percentage starts of Second app when First app was already started on a user device.}
\\end{table}
'''

tmplist = []
anothertmp ={}
for device in devicecostarts:
    z = {}
    anothertmp[device] = z

    for w in devicecostarts[device]:
        if devicecostarts[device][w] < 21:
            continue
        if w == 'com.android.contacts com.android.phone':
            continue

        prob = float(devicecostarts[device][w])/deviceappstartcounts[device][w.split()[0]]
        anothertmp[device][w]= prob
        if prob > 0.49:
            print device, '\t', w , '\t' , prob , '\t', devicecostarts[device][w]
            tmplist.append((device,w,prob))
            
for device, w , prob in sorted(tmplist, key=lambda entry: entry[2], reverse=True):
    f.write(device[0:6])
    f.write(' & ')
    app1 = None
    if appnames.has_key(w.split()[0]):
        app1 = appnames[w.split()[0]]
    else:
        app1 = w.split()[0]

    f.write(app1)
    f.write(' & ')

    app2 = None
    if appnames.has_key(w.split()[1]):
        app2 = appnames[w.split()[1]]
    else:
        app2 = w.split()[1]

    f.write(app2)
    f.write(' & ')
    f.write(str(int(prob*100)))
    f.write('\\\\ \n')

f.write(c)
f.close()
