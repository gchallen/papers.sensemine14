#!/usr/bin/env python

import pydot, argparse
from applications.lib import * #@UnusedWildImport
from collections import defaultdict
from common import lib


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

f = open('output.tex','w')

header = '''
\\documentclass{article}
\\usepackage{booktabs}
\\usepackage{graphicx}
\\newcommand{\\head}[1]{\\textnormal{\\textbf{#1}}}
\\begin{document}
\\begin{table}
\\centering
\\scalebox{0.5} {
\\begin{tabular}{lllc}
\\toprule[1.5pt]
\\multicolumn{1}{l}{Device} & \\multicolumn{1}{l}{First App} & \\multicolumn{1}{l}{Second App} & \\multicolumn{1}{c}{Percent}\\\\
\\midrule
'''
f.write(header)

c = '''\\bottomrule[1.5pt]
\\end{tabular}
}
\\caption{Starts of Second app when First app was started}
\\end{table}
\\end{document}'''

tmplist = []
anothertmp ={}
for device in devicecostarts:
    z = {}
    anothertmp[device] = z

    for w in devicecostarts[device]:
        if devicecostarts[device][w] < 11:
            continue
        if w == 'com.android.contacts com.android.phone':
            continue

        prob = float(devicecostarts[device][w])/deviceappstartcounts[device][w.split()[0]]
        anothertmp[device][w]= prob
        if prob > 0.19:
            print device, '\t', w , '\t' , prob , '\t', devicecostarts[device][w]
            tmplist.append((device,w,prob))
            
for device, w , prob in sorted(tmplist, key=lambda entry: entry[2], reverse=True):
    f.write(device[0:6])
    f.write(' & ')
    app1 = None
    if applications.popular_app_names.has_key(w.split()[0]):
        app1 = applications.popular_app_names[w.split()[0]]
    else:
        app1 = w.split()[0]

    f.write(app1)
    f.write(' & ')

    app2 = None
    if applications.popular_app_names.has_key(w.split()[1]):
        app2 = applications.popular_app_names[w.split()[1]]
    else:
        app2 = w.split()[1]

    f.write(app2)
    f.write(' & ')
    f.write(str(int(prob*100)))
    f.write('\\\\ \n')

f.write(c)
f.close()




'''
g = pydot.Dot()
seen_applications = {}

THRESHOLD = 0.0

COUNT_THRESHOLD = 10

applist = applications.popular_installs[0:int(len(applications.popular_installs)*0.3)]

for app_pair in anothertmp.keys():
    first_app = app_pair.split()[0]
    second_app = app_pair.split()[1]

#    if first_app not in applications.system_applications and first_app not in applist:
#        continue
    
#    if second_app not in applications.system_applications and second_app not in applist:
#        continue

    if not seen_applications.has_key(applications.popular_app_names[first_app]):
        seen_applications[applications.popular_app_names[first_app]] = pydot.Node(applications.popular_app_names[first_app])
    if not seen_applications.has_key(applications.popular_app_names[second_app]):
        seen_applications[applications.popular_app_names[second_app]] = pydot.Node(applications.popular_app_names[second_app])

    costarted_count = tmp[app_pair]

    #if costarted_count <= COUNT_THRESHOLD:
     #   continue



    started_app_probability = anothertmp[app_pair]
    #second_app_probability = float(costarted_count)/appstartcount[second_app]
    if started_app_probability >= THRESHOLD:
        g.add_edge(pydot.Edge(seen_applications[applications.popular_app_names[first_app]], seen_applications[applications.popular_app_names[second_app]], weight=costarted_count, label='%.2f' % (started_app_probability,)))
    #if second_app_probability >= THRESHOLD:
    #    g.add_edge(pydot.Edge(seen_applications[second_app], seen_applications[first_app], weight=costarted_count, label='%.2f' % (second_app_probability,)))

'''
