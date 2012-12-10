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

for first_application, second_application in itertools.combinations(sorted(allapps), 2):
    pass


appstartcount = defaultdict(int)

print len(applications.screen_states)



for session in applications.screen_states:
    if (session.end - session.start).total_seconds() > SANE_SESSION_LENGTH:
        continue
    
    
    last_activity = None
    unique = []
    for activity in session.activities:
        
        if activity.package == 'com.android.launcher' or activity.package == 'com.gau.go.launcherex' or activity.package == 'android':
            continue
        if activity.package not in unique:
            unique.append(activity.package)
            appstartcount[activity.package] +=1


    for x in range(0,len(unique)):
        for y in range(x+1,len(unique)):
            ke = unique[x] + ' ' + unique[y]
            tmp[ke] += 1


#for app in applications.activities:
#    appstartcount[app.package] +=1


anothertmp ={}

for w in sorted(tmp, key=tmp.get , reverse=True):
    #print w, '\t', tmp[w],'\t', appstartcount[w.split()[1]], '\t',float(tmp[w])/appstartcount[w.split()[1]]
    if tmp[w] < 50:
        continue
    anothertmp[w]= float(tmp[w])/appstartcount[w.split()[0]]

for w in sorted(anothertmp, key=anothertmp.get , reverse=True):
    print w, '\t',tmp[w],'\t', anothertmp[w],'\t', appstartcount[w.split()[0]]


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
for first_app in costartedapps.keys():
    for second_app in costartedapps[first_app].keys():
        if first_app in Application.PHONELAB_APPS or second_app in Application.PHONELAB_APPS:
            continue

        if costartedapps[first_app][second_app] == 0:
            continue

        if not seen_applications.has_key(first_app):
            seen_applications[first_app] = pydot.Node(first_app)
        if not seen_applications.has_key(second_app):
            seen_applications[second_app] = pydot.Node(second_app)


        costarted_count = costartedapps[first_app][second_app]

        first_app_probability = float(costarted_count)/appstartcount[first_app]
        second_app_probability = float(costarted_count)/appstartcount[second_app]


        if first_app_probability >= THRESHOLD:
            g.add_edge(pydot.Edge(seen_applications[first_app], seen_applications[second_app], weight=costarted_count, label='%.2f' % (first_app_probability,)))

        if second_app_probability >= THRESHOLD:
            g.add_edge(pydot.Edge(seen_applications[second_app], seen_applications[first_app], weight=costarted_count, label='%.2f' % (second_app_probability,)))

'''



g.write_pdf('graph.pdf')
            
