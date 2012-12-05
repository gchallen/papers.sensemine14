import os
import json
import numpy as np
import matplotlib.pyplot as plt
import datetime
from collections import defaultdict
from pylab import plot, show

import statsmodels.api as sm 

def generateAppsList(path):
	ontimes=dict()
        tmparray=[]
        filelist=[]
        output = open('output.txt','w')
	root, dirs, files = os.walk('.').next()
	for name in files:
	    extension = os.path.splitext(name)[1]
	    if "filtered" in name: 
                filelist.append(os.path.join(root,name))
		
	for f in filelist:
            componentforgroundtime = dict()
            componentstarttimes = defaultdict(int)
	    log = open(f,'r')
	    name = os.path.basename(f)
            print '\nProcessing, ', name
            currentfgapp=None
            newfgapp=None
            screenontime=None
            screenofftime=None
            cumulativeontime=0
            newfgappontime=None
            appstartedstate = False
            screenonstate= False
            screenoffstate= False
	    for line in log:
                        #print line
                if 'android.intent.action.SCREEN_ON' in line:
                    ss = line.split()
                    screenontime=datetime.datetime.strptime(ss[0]+ss[1], '%Y-%m-%d%H:%M:%S.%f')
                    screenonstate = True
                    screenoffstate = False
                    appstartedstate = False
                                #print screenontime
                            #print 'current active fg app is ', currentfgapp
                                
                elif 'START' in line:
                                #print 'screenoffstate ',screenoffstate
                    ss = line.split()
                    tmpappstarttime = datetime.datetime.strptime(ss[0]+ss[1], '%Y-%m-%d%H:%M:%S.%f')

                    clms = line.split()
                    appstr = ' '.join(clms[7:])
                    tmpappstr=appstr[1:appstr.find('}')]
                    tmpappstrsplits=tmpappstr.split()
                    for jj in tmpappstrsplits:
                        if jj.startswith('cmp'):
                            appcmp=jj.split('=')
                            newfgapp=appcmp[1][0:appcmp[1].find('/')]
                            componentstarttimes[newfgapp]+=1
                                    #print 'new fg app ',newfgapp

                    tmptimeactive=0.0
                                # update for current app
                    if currentfgapp != None:
                                    #print 'replacing current fg app ', currentfgapp
                        if appstartedstate:
                            tmptimeactive = (tmpappstarttime - newfgappontime).total_seconds()
                        elif screenonstate:
                                    #print 'scr on state'
                            tmptimeactive = (tmpappstarttime - screenontime).total_seconds()
                                

                                # account for incoming calls alarms etc, .
                        if screenoffstate:
                                    #print 'setting tmpactive time to 0'
                            tmptimeactive = 0.0;
                                
                                #print 'time between screen on and new app = ', tmptimeactive
                        if currentfgapp in componentforgroundtime:
                            cumutime = componentforgroundtime[currentfgapp]
                                    #print currentfgapp , ' fg time so far ', cumutime
                            cumutime += tmptimeactive
                            componentforgroundtime[currentfgapp] = cumutime
                                    #print 'new cumu time ', cumutime
                        else:
                            componentforgroundtime[currentfgapp] = tmptimeactive
                                    #print 'made an entry for new app'
                            #print 'screenoffstate= ', screenoffstate   
                        if screenonstate==True:    
                                #print 'newfgapp is replacing currentfgapp', newfgapp , ' current fgapp is ', currentfgapp
                            currentfgapp = newfgapp# this is done to account for notifications like incoming messages etc.
                            newfgappontime = tmpappstarttime
                            appstartedstate=True

                elif 'android.intent.action.SCREEN_OFF' in line:
                    if screenontime == None: continue
                    if screenoffstate == True:continue
                                #if ontime==None or appontime==None:continue
                    screenoffstate = True
                    screenonstate = False
                    ss  =line.split()
                    offtime=datetime.datetime.strptime(ss[0]+ss[1], '%Y-%m-%d%H:%M:%S.%f')
                                #duration = offtime - ontime
                    if newfgapp!=None:
                        if appstartedstate:
                                    #print 'app was started time started = ', str(newfgappontime)
                            appfgtime = (offtime-newfgappontime).total_seconds()
                        else:
                                    #print 'using screen on time = ', str(screenontime)
                            appfgtime = (offtime-screenontime).total_seconds()
                                       
                                    #print ' active time for app before screen off is ', newfgapp , ' time ', appfgtime    
                        if newfgapp in componentforgroundtime:
                            cumutime = componentforgroundtime[newfgapp]
                            cumutime += appfgtime
                            componentforgroundtime[newfgapp] = cumutime
                                        #print 'new accumulated active time for app ', cumutime
                        else:
                                        #print 'adding to dict for the first time'
                            componentforgroundtime[newfgapp] = appfgtime
                                #ontime=None
                                #offtime=None

            log.close()
                       # print componentforgroundtime
                       # print '----------------------'
                       # print componentstarttimes
                       # print '----------------------'
            output.write('\n' + os.path.basename(f))
            output.write('\n')
            for w in sorted(componentforgroundtime, key=componentforgroundtime.get, reverse=True):
                output.write(w)
                output.write('\t')
                output.write(str(componentforgroundtime[w]))
                output.write('\n')
            output.write('\n # of starts \n')
            for w in sorted(componentstarttimes, key=componentstarttimes.get, reverse=True):
                output.write(w)
                output.write('\t')
                output.write(str(componentstarttimes[w]))
                output.write('\n')
        output.close()

        '''#print ontimes
        for w in sorted(ontimes, key=ontimes.get, reverse=True):
            print w, ontimes[w]
        print 'MIN = ' , min(tmparray)
        print 'MAX = ' , max(tmparray)
        print len(tmparray)
        

        sortedtmp = sorted(tmparray)
        dsum = sum(tmparray)
        
        normalized_data = []
        iii =0
        for ii in sortedtmp:
            normalized_data.append(sortedtmp[iii]/dsum)
            iii+=1

        cdf = []

        #for i in range(0,len(sortedtmp)):
        #    cdf.append( sum(normalized_data[0:i]))

        
        for i in range(1,len(sortedtmp)+1):
            cdf.append(i*1.0/len(sortedtmp))
        
        print cdf
        print len(sortedtmp)
        plt.plot(sortedtmp,cdf)
        plt.xlabel('Time the screen was on over a day')
        plt.ylabel('Fraction of devices')
        plt.title('CDF of Screen ON times')
        show()'''
		
generateAppsList('/home/ans25/theworks/logdata/test/Apps_Usage/')
