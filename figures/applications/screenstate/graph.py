#!/usr/bin/env python

import pydot, argparse
from applications.lib import * #@UnusedWildImport
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt

app_component_foregroundtime=dict()
app_start_times=dict()
device_transitions=dict()

applications = Application.load()

devlow = ()
devregular = ()
devicedifference = []
THRESHOLD = 10

for dev in applications.device_filtered_logs:
    #print dev
    '''if dev != '3844ad32f0bce2e111d6a063c80d49e6c942955a':
        continue'''
    #print 'processing ',dev, ' ', len(applications.device_filtered_logs[dev])
    plugged = None
    current_battery_level = None

    last_known_updatetime =  applications.device_filtered_logs[dev][0].datetime
    #print last_known_updatetime
    screenontime = None
    screenofftime = None
    
    total_time_below_threshold = 0.0
    last_bt_time = None
    last_at_time = None
    total_time_above_threshold = 0.0


    lowbatteryontime = 0.0
    regularbatteryontime = 0.0

    devicewentbelowthreshold = False
    
    for logline in applications.device_filtered_logs[dev]:
        #print logline
        #print 'below and above thres ',total_time_below_threshold, '\t' ,total_time_above_threshold
        #print 'low and reg times ', lowbatteryontime, '\t',regularbatteryontime

        #print (logline.datetime - last_known_updatetime).total_seconds()
        if (logline.datetime - last_known_updatetime).total_seconds() > 180:
            #discard stale values
            #print (logline.datetime - last_known_updatetime).total_seconds()
            plugged = None
            current_battery_level = None

            screenontime = None
            screenonbatterylevel = None
            screenofftime = None
            last_known_updatetime = logline.datetime
            last_bt_time = None
            last_at_time = None
            if logline.label == 'battery_status':
                current_battery_level = int(logline.json['BatteryLevel'])
                if current_battery_level <= THRESHOLD:
                    last_bt_time = logline.datetime
                else:
                    last_at_time = logline.datetime
            continue

        last_known_updatetime = logline.datetime
        if logline.label == 'battery_status':
            if logline.json['Plugged'] == False:
                plugged = False
                last_level = current_battery_level
                current_battery_level = int(logline.json['BatteryLevel'])
                if current_battery_level <= THRESHOLD:
                    devicewentbelowthreshold = True
                    if screenonbatterylevel > THRESHOLD:
                        regularbatteryontime += (screenontime - logline.datetime).total_seconds()
                        screenontime = logline.datetime
                        screenonbatterylevel = current_battery_level
                    if last_bt_time != None:
                        total_time_below_threshold += (logline.datetime - last_bt_time).total_seconds()
                    if last_level > THRESHOLD and last_at_time != None:
                            total_time_above_threshold += (logline.datetime - last_at_time).total_seconds()
                            last_at_time = None
                    last_bt_time = logline.datetime
                else:
                    if last_at_time != None:
                        total_time_above_threshold += (logline.datetime - last_at_time).total_seconds()

                    last_at_time = logline.datetime

            else:
                plugged = True
                ''' current_battery_level = int(logline.json['BatteryLevel'])
                if current_battery_level < THRESHOLD:
                    if last_bt_time != None:
                        total_time_below_threshold += (logline.datetime - last_bt_time).total_seconds()
                        last_bt_time = None
                    else:
                        if last_at_time != None:
                            total_time_above_threshold += (logline.datetime - last_at_time).total_seconds()
                            last_at_time = None'''

        
        if logline.label == 'screen_on' and plugged == False:
            screenontime = logline.datetime
            screenonbatterylevel = current_battery_level
            #print 'on ',screenontime, ' ', plugged
        if logline.label == 'screen_off' and plugged == False:
            screenofftime = logline.datetime
            #print 'off ',screenofftime, ' level ', current_battery_level, 'on time ', screenontime
            if screenontime != None and current_battery_level <= THRESHOLD:
                lowbatteryontime += (screenofftime - screenontime).total_seconds()
            elif screenontime != None and current_battery_level > THRESHOLD:
                regularbatteryontime += (screenofftime - screenontime).total_seconds()
            screenontime = None
            screenonbatterylevel = -1

    #print dev,'\t',lowbatteryontime/60.0,'\t',total_time_below_threshold/60.0,'\t', regularbatteryontime/60.0,'\t',total_time_above_threshold/60.0
#    total_time= lowbatteryontime/60.0 + regularbatteryontime/60.0
    normlowbat=0.0
    normregbat=0.0
    if total_time_below_threshold != 0.0:
        normlowbat = lowbatteryontime/total_time_below_threshold
        #print dev,' ',normlowbat, ' ', lowbatteryontime, ' ',total_time_below_threshold
    if total_time_above_threshold != 0.0:
        normregbat=regularbatteryontime/total_time_above_threshold

    if devicewentbelowthreshold:
        devlow = devlow + (normlowbat,)
        devregular = devregular + (normregbat,)
        devicedifference.append(normlowbat - normregbat)
    else:
        print 'This device never went below ', dev

ind = np.arange(len(devlow))
width = 0.30
#p1 = plt.bar(ind, devlow,width, color='r')
p1 = plt.bar(ind, sorted(devicedifference),width, color='r')
#p2 = plt.bar(ind+width, devregular,width, color='g')

plt.ylabel('Total time')
plt.xlabel('Device')
plt.title('Normalized Screen on times for low and regular battery levels')
D=()
for i in range(1,len(devlow)+1):
    D=D+('D'+str(i),)

plt.xticks(ind+width/2., D )
#plt.yticks(np.arange(0,81,10))
#plt.legend( (p1[0], p2[0]), ('<15%', '>15%') )

plt.show()



'''
for dev in applications.device_filtered_logs:
	componentforgroundtime = dict()
    	componentstarttimes = defaultdict(int)
    	currentfgapp=None
    	newfgapp=None
    	screenontime=None
    	screenofftime=None
    	cumulativeontime=0
    	newfgappontime=None
    	appstartedstate = False
    	screenonstate= False
    	screenoffstate= False
	for lgline in applications.device_filtered_logs[dev]:
		if 'android.intent.action.SCREEN_ON' in lgline:
			ss = lgline.split()
        		screenontime=datetime.datetime.strptime(ss[1]+ss[2], '%Y-%m-%d%H:%M:%S.%f')
        		screenonstate = True
        		screenoffstate = False
        		appstartedstate = False
    		elif 'START' in lgline:
        		ss = lgline.split()
        		tmpappstarttime = datetime.datetime.strptime(ss[1]+ss[2], '%Y-%m-%d%H:%M:%S.%f')
        		clms = lgline.split()
        		appstr = ' '.join(clms[8:])
        		tmpappstr=appstr[1:appstr.find('}')]
        		tmpappstrsplits=tmpappstr.split()
        		for jj in tmpappstrsplits:
            			if jj.startswith('cmp'):
                			appcmp=jj.split('=')
                			newfgapp=appcmp[1][0:appcmp[1].find('/')]
                			componentstarttimes[newfgapp]+=1
        		tmptimeactive=0.0
        		if currentfgapp != None:
            			if appstartedstate:
                			tmptimeactive = (tmpappstarttime - newfgappontime).total_seconds()
            			elif screenonstate:
                			tmptimeactive = (tmpappstarttime - screenontime).total_seconds()

            			if screenoffstate:
                			tmptimeactive = 0.0;

            			if currentfgapp in componentforgroundtime:
                			cumutime = componentforgroundtime[currentfgapp]
                			cumutime += tmptimeactive
                			componentforgroundtime[currentfgapp] = cumutime
            			else:
                			componentforgroundtime[currentfgapp] = tmptimeactive

        		if screenonstate==True:
            			currentfgapp = newfgapp
            			newfgappontime = tmpappstarttime
            			appstartedstate=True

    		elif 'android.intent.action.SCREEN_OFF' in lgline:
        		if screenontime == None: continue
        		if screenoffstate == True:continue
        		screenoffstate = True
        		screenonstate = False
        		ss  =lgline.split()
        		offtime=datetime.datetime.strptime(ss[1]+ss[2], '%Y-%m-%d%H:%M:%S.%f')
        		if newfgapp!=None:
            			if appstartedstate:
                			appfgtime = (offtime-newfgappontime).total_seconds()
            			else:
                			appfgtime = (offtime-screenontime).total_seconds()

            			if newfgapp in componentforgroundtime:
                			cumutime = componentforgroundtime[newfgapp]
                			cumutime += appfgtime
                			componentforgroundtime[newfgapp] = cumutime
            			else:
                			componentforgroundtime[newfgapp] = appfgtime

	app_component_foregroundtime[dev]=componentforgroundtime
	app_start_times[dev]=componentstarttimes

f=open('foregroundtimes','w')
for kk in (app_component_foregroundtime):
	f.write(kk)
	f.write('\n\n')
	for w in sorted(app_component_foregroundtime[kk], key=app_component_foregroundtime[kk].get, reverse=True):
    		f.write(w)
    		f.write('\t')
    		f.write(str(app_component_foregroundtime[kk][w]))
    		f.write('\n')


	f.write('\n\nNumber of Starts\n')

	for w in sorted(app_start_times[kk], key=app_start_times[kk].get, reverse=True):
    		f.write(w)
    		f.write('\t')
    		f.write(str(app_start_times[kk][w]))
   		f.write('\n')
f.close()




#processing for app transitions
HOME='HOME'
device_app_transtition_count = dict()
for dev in applications.device_filtered_logs:
 	newfgapp=None
        current_transition=[]
        device_transitons_list=[]
        app_transition_count=defaultdict(int)
        for lgline in applications.device_filtered_logs[dev]:
            if 'START' in lgline:
                ss = lgline.split()
                clms = lgline.split()
                appstr = ' '.join(clms[8:])
                tmpappstr=appstr[1:appstr.find('}')]
                tmpappstrsplits=tmpappstr.split()

                if 'android.intent.category.HOME' in tmpappstr and 'cmp=com.android.launcher/com.android.launcher2.Launcher' in tmpappstr:
                    newfgapp=HOME
                    if len(current_transition) > 0:
                        current_transition.append(HOME)
                        device_transitons_list.append(current_transition)
                        current_transition=[]
                else:
                    for jj in tmpappstrsplits:
                        if jj.startswith('cmp'):
                            appcmp=jj.split('=')
                            newfgapp=appcmp[1][0:appcmp[1].find('/')]

                if 'act=android.intent.action.MAIN' in tmpappstr and 'cat=[android.intent.category.LAUNCHER]' in tmpappstr:
                    if newfgapp != HOME:
                        current_transition.append('HOME_USING_BACK')
                        device_transitons_list.append(current_transition)
                        current_transition=[]
                        current_transition.append(HOME)
                        current_transition.append(newfgapp)
                else:
                    if newfgapp !=None:
                        current_transition.append(newfgapp)
        
        device_transitions[dev] = device_transitons_list
	#print device_transitons_list
        for transl in device_transitons_list:
            if len(transl) <= 1 : continue
            startapp=transl[0]
            for t in range(1,len(transl)):
                appendstr = transl[t]
                if 'HOME_USING_BACK' == appendstr:
                    appendstr = HOME
                if startapp == appendstr:continue
                keystr = startapp + ' ' + appendstr
                app_transition_count[keystr]+=1
        device_app_transtition_count[dev]=app_transition_count


f = open('apptransitions','w')
for d in device_app_transtition_count:
    f.write('\n\n')
    f.write(d)
    f.write('\n\n')
    for w in sorted(device_app_transtition_count[d], key=device_app_transtition_count[d].get, reverse=True):
        strline = w + ' ' + str(device_app_transtition_count[d][w])
	f.write(strline)
	f.write('\n')
f.close()
'''
