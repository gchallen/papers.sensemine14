import os
import json
import numpy as np
from numpy import arange, random
from matplotlib.dates import WeekdayLocator, DateFormatter
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import *
from datetime import datetime
from collections import defaultdict
import re
import decimal

def changeGraph(path):
	d = os.path.join('/home/anudipa/phonelab/Experiment Logs/','graphs')
        if not os.path.exists(d):
                os.makedirs(d)

	
#	mpl.use("agg")
#Define the names and the path of the file where graphs will be stored
        fname1 = os.path.join(d,'chargeleft.pdf')
        fname2 = os.path.join(d,'batterylevel.pdf')
        fname3 = os.path.join(d,'templevel.pdf')
	fname11 = os.path.join(d,'chargingTime.pdf')

	pp1 = PdfPages(fname1)
        pp2 = PdfPages(fname2)
        pp3 = PdfPages(fname3)
	pp11 = PdfPages(fname11)
	c = 0
        cmap1 = mpl.cm.autumn
        cmap2 = mpl.cm.winter
	cmap3 = mpl.cm.hsv

#Debug file plots the time and the correspponding battery level in a separate text file for debugging purposes
        debug = open(os.path.join('/home/anudipa/phonelab/Experiment Logs/','check.txt'), 'w')

	for files in os.listdir(path):
		stats = []
                timestamp = []
                temp = []
                plugged = []

           	fname = os.path.join(path,files)
		print fname
		try:
			log = open(fname, 'r')
		except IOError:
			print 'Cannot open json files'
			break
		for line in log:
			data = line.split()
			if len(data) > 5:
				newdate = data[0] + '-12 ' + data[1]
                                t = datetime.strptime(newdate,'%m-%d-%y %H:%M:%S.%f')
#				jsonStr = "".join(data[6::])
				json_dict = json.loads(data[6])
				stats.append(int(json_dict['BatteryLevel']))
				timestamp.append(t)
				temp.append(int(json_dict['Temparature']))
				plugged.append(json_dict['Plugged'])

#				debug.write('%s %s : %s : %s\n' % (timestamp[-1],json_dict['BatteryLevel'],json_dict['Temparature'],plugged[-1]))
#				debug.write('\n')
		log.close()
		device = os.path.basename(fname)
#Graph for showing charge left before each plugging event
#		print plugged.count(True)
		if plugged.count(True) > 0:
			x = []
			y = []
			flag = 0
			for i in xrange(0, len(plugged)):
				if flag == 0 and plugged[i] == True:
#					print timestamp[i].strftime('%H')
					x.append(timestamp[i].strftime('%H'))
					y.append(stats[i])
					debug.write('%s %s : %s \n' % (device, y[-1],x[-1]))
					flag = 1
				elif flag == 1 and plugged[i] == False:
					flag = 0
			fig1 = figure(c+1, dpi=10)
			hist(y,bins=20, color = cmap3(0.6))
			grid()
                        title('Charge left before plugging in %s' % device, fontsize=20)
                        xlabel('Battery Level',fontsize=15)
                        ylabel('Number of occurrences', fontsize=15)
                        pp1.savefig(fig1)
                       	fig1.clear()
			close()
#Graph for showing the time when device is plugged in
			fig11 = figure(c+2, dpi=10)
			plot(x,y,'o')
#			Xaxis.set_major_locator(HourLocator())
#			Xaxis.set_major_formatter(DateFormatter('%H %M'))	
			title('Charge left before plugging in %s' % device, fontsize=20)
                        ylabel('Battery Level',fontsize=15)
                        xlabel('Time', fontsize=15)
                        pp11.savefig(fig11)
                        fig11.clear()
			close()
		
#Graph for showing battery level over time for each device
                if len(stats) > 0:
                        fig2 = figure(c+3, dpi=10)
                        plot(timestamp,stats,color = cmap1(0.6),marker='o')
                        grid()
                        xlabel('Time',fontsize=15)
                        ylabel('Battery Level',fontsize=15)
                        title('Battery level for %s' % device, fontsize=20)
                        pp2.savefig(fig2)
                        fig2.clear()
			close()

#Graph for showing temperature of battery over time for each device
		if len(temp) > 0:
			fig3 = figure(c+4,dpi=10)
                        plot(timestamp,temp,color = cmap2(0.6),marker='o')
                        grid()
                        xlabel('Time',fontsize=15)
                        ylabel('Temperature Level',fontsize=15)
                        title('Temperature of Battery for %s' % device, fontsize=20)
                        pp3.savefig(fig3)
                        fig3.clear()
			close()

		del fig1
		del fig11
		del fig2
		del fig3
		c = c+5
	pp1.close()
	pp2.close()
	pp3.close()
	pp11.close()
	debug.close()




"""Example:
UID: 10003, UidName: com.android.browser, Rx: 5741122, Tx: 1024283, Packages: [com.android.browser], PerUidPerTypeInfo: [(Type: STATS_SINCE_CHARGED, CpuTime: 529930, CpuFgTime: 528570, WakelockTime: 707, GpsTime: 0, Power: 73351.45900955956, WifiRunningTimeMS: 0), (Type: STATS_SINCE_UNPLUGGED, CpuTime: 1059860, CpuFgTime: 1057140, WakelockTime: 707, GpsTime: 0, Power: 146671.81001911915, WifiRunningTimeMS: 0)]

"""
PACKAGES_PATTERN = re.compile(r"""Packages: \[.*?\]""")

UID_PATTERN=re.compile(r"""^
UID:\s+(?P<uid_num>\d+),\s+(UidName):\s+(?P<uid_name>.+?),\s+(Rx):\s+(?P<rx>\d+),\s+(Packages):\s+\[(?P<package_list>.+)\],\s+
(PerUidPerTypeInfo):\s+\[\(+(Type):\s+(STATS_SINCE_CHARGED),\s+(CpuTime):\s+(?P<cpuTime_charged>\d+),\s+(CpuFgTime):\s+(?P<cpuFgTime_charged>\d+),\s+
(WakelockTime):\s+(?P<wakelock_charged>\d+),\s+(GpsTime):\s+(?P<gpsTime_charged>\d+),\s+(Power):\s+(?P<power_charged>.+?),\s+
(WifiRunningTimeMS):\s+(?P<wifiTime_charged>\d+)\),\s+\(+(Type):\s+(STATS_SINCE_UNPLUGGED),\s+(CpuTime):\s+(?P<cpuTime_unplugged>\d+),\s+
(CpuFgTime):\s+(?P<cpuFgTime_unplugged>\d+),\s+(WakelockTime):\s+(?P<wakelock_unplugged>\d+),\s+(GpsTime):\s+(?P<gpsTime_unplugged>\d+),\s+
(Power):\s+(?P<power_unplugged>.+?),\s+(WifiRunningTimeMS):\s+(?P<wifiTime_unplugged>\d+)\)\]$""",re.VERBOSE)

MESSY = re.compile(r"""(?P<key_name>.*?):\s+(?P<value>(?:\[.*?\]|[\w.\-]*))[,\s]*""",re.VERBOSE)
DRESSUP = re.compile(r"""\(+(?P<items>.*?)\)[,\s]*""",re.VERBOSE)

def checkPattern(gibberish):
	dict_ = {}
	info = MESSY.finditer(gibberish)
	
	if not info == None:
		for match in info:
#		print 'something'
			key = match.group('key_name')
			value = match.group('value')
			dict_[key] = value
#			print key, '----->', value
#	child = DRESSUP.finditer(dict_['PerUidPerTypeInfo'])
#	if not child == None:
#		for match in child:
#               	print 'something'
#			key = match.group('items')
 #               	print key

	return dict_








def perUidPowerStats(path):
	d = os.path.join('/home/anudipa/phonelab/Experiment Logs/graphs/','perUid')
        if not os.path.exists(d):
                os.makedirs(d)

	fname1 = os.path.join(d,'uidpower.pdf')

	pp = PdfPages(fname1)
	c = 1
	
	for files in os.listdir(path):
		old_pow_c = {}
		old_pow_u = {}
		powerCharged = {}
		powerUnplugged = {}

		maxC = decimal.Decimal(0)
		minC = decimal.Decimal(0)
		fname = os.path.join(path,files)
		print fname
                try:
                        log = open(fname, 'r')
                except IOError:
                        print 'Cannot open json files'
                        break
                for line in log:
                        data = line.split()
                        if len(data) > 6:
				json_dict = json.loads(line)
				if json_dict.keys().count('UidInfo') == 1:
					dict_ = checkPattern(json_dict['UidInfo'])
					name = dict_['UidName']
#					print name
					child = DRESSUP.finditer(dict_['PerUidPerTypeInfo'])
					for match in child:
						child_ = checkPattern(match.group('items'))
						if child_['Type'] == 'STATS_SINCE_CHARGED':
							charged_power = decimal.Decimal(child_['Power']) / 1000
						if child_['Type'] == 'STATS_SINCE_UNPLUGGED':
							unplugged_power = decimal.Decimal(child_['Power']) / 1000
										
					if old_pow_c[name] == 0:
						old_pow_c[name] = charged_power
					if old_pow_u[name] == 0:
						old_pow_u[name] = unplugged_power
					try:
						if old_pow_c[name] > charged_power:
							diff = charged_power
						else:
							diff = charged_power - old_pow_c[name]
						powerCharged[name] = decimal.Decimal(powerCharged[name]) + diff
						if old_pow_u[name] > unplugged_power:
							diff = unplugged_power
						else:
							diff = unplugged_power - old_pow_u[name]
						powerUnplugged[name] = decimal.Decimal(powerUnplugged[name]) + diff
						
						old_pow_c[name] = charged_power
						old_pow_u[name] = unplugged_power
						if maxC < old_pow_c[name]:
							maxC = old_pow_c[name]
						if minC > old_pow_c[name]:
							minC = old_pow_c[name]
						#uidCount[name]  = int(uidCount[name]) + 1
					except:
						powerCharged[name] = 0
						powerUnplugged[name] = 0
		log.close()
		device = os.path.basename(fname).split('.')[0]
		avg = (maxC + minC)/2
		print '\nMaximum Power Consumption ----> ',maxC,' Limit is = ', avg 
		if len(powerCharged.keys()) > 0:
			uidName = []
			powerC = []
			powerU = []
			count = []
			for keys in powerCharged:
				if powerCharged[keys] > 0 and powerCharged[keys] > avg:
					print keys,'----> ',powerCharged[keys]
#					print keys,'---->',powerUnplugged[keys]
					uidName.append(keys)
					powerC.append(long(powerCharged[keys]))
					powerU.append(long(powerUnplugged[keys]))
			ind = arange(len(uidName))
			print 'total num of x points = ', ind, '\n'
			width = 0.25
			fig = figure(c,dpi = 10)
			ax = fig.add_subplot(111)
			bar1 = ax.bar(ind,powerC,width,color='r')
			bar2 = ax.bar(ind+width,powerU,width,color='b')
			ax.set_ylabel('Total Power', fontsize=10)
			ax.set_title('For %s' % device, fontsize=10)
			ax.set_xticks(ind+width)
			ax.set_xticklabels(uidName,size='x-small' )
			fig.autofmt_xdate()
			box = ax.get_position()
			ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
			ax.legend((bar1, bar2),('SINCE_CHARGED', 'SINCE_UNPLUGGED'),fontsize=8,loc='center left', bbox_to_anchor=(1, 0.5))

			pp.savefig(fig)
			fig.clear()
			close()

		c = c + 1
	pp.close()


def getAllDates(path):
	dates_ = []
	for files in os.listdir(path):
		fname = os.path.join(path,files)
		try:    
			log = open(fname, 'r')
		except IOError:
                        print 'Cannot open json files'
                        break
                for line in log:
			json_dict = json.loads(line)
			if dates_.count(json_dict['Date']) == 0:
				dates_.append(json_dict['Date'])
	
	return dates_


def calculateRatio(numerator_, denominator_):
	result = {}
	for keys in numerator_:
		if denominator_[keys] > 0:
			result[keys] = numerator_[keys]/denominator_[keys]
		else:
			result[keys] = float(0.0)
#	print result
	return result


def getLinearRegress(fname,xtag,ytag,dict_):
	pp = PdfPages(fname)
	c = 0 
	for uid in dict_:
		print max(dict_[uid][xtag])
		print min(dict_[uid][ytag])
		if max(dict_[uid][xtag]) > 0 and max(dict_[uid][ytag]) > 0:
			fit = np.polyfit(np.log(dict_[uid][xtag]),np.log(dict_[uid][ytag]),1)
			fit_fn = np.poly1d(fit)
			fig = figure(c, dpi= 10)
			gca().set_xscale('log', basex = 2)
			gca().set_yscale('log', basey = 2)
			plot(dict_[uid][xtag], dict_[uid][ytag], 'ro', fit_fn, '--k')
			xlabel('CpuFgTime in Second' , fontsize = 10)
                        ylabel('Power in mA-Sec', fontsize = 10)
                        title('Power/CpuFgTime for %s' % uid, fontsize = 10)
                        grid(True,which="both",ls="-")
                        pp.savefig(fig)
                        fig.clear()
                        close()
                        c = c + 1
	pp.close()



def getUidScatter(fname,xtag,ytag,xname,yname,scatter_):
	pp2 = PdfPages(fname)
	c = 0
        for uid in scatter_:
                if max(scatter_[uid][ytag]) > 0 and max(scatter_[uid][xtag]) > 0 and len(scatter_[uid][ytag]) > 0:
                        fig = figure(c, dpi=10)
                        loglog(scatter_[uid][xtag],scatter_[uid][ytag],'o',basex = 2, basey = 2)
                        xlabel('%s in Second' % xname, fontsize = 10)
                        ylabel('Power in mA-Sec', fontsize = 10)
                        title('Power/%s for %s' % (xname, uid), fontsize = 10)
			grid(True,which="both",ls="-")
                        pp2.savefig(fig)
                        fig.clear()
                        close()
                        c = c + 1


        pp2.close()






def summaryByUid(path,time, opt):
	d = os.path.join('/home/anudipa/phonelab/Experiment Logs/graphs/','perUid')
        if not os.path.exists(d):
                os.makedirs(d)

        fname1 = os.path.join(d,'uidSummary.pdf')
	if opt == 'hist':
		variableName = 'PowerBy'+time+'Hist.pdf'
	elif opt == 'scatter1':
		variableName = 'PowerBy'+time+'Scatter.pdf'
	elif opt == 'fitting':
		variableName = 'PowerBy'+time+'Fitting.pdf'
	fname2 = os.path.join(d,variableName)
#        pp = PdfPages(fname1)
#	pp2 = PdfPages(fname2)

	date_ = getAllDates(path)
	print date_
	powerMax = defaultdict(list)
	powerMin = defaultdict(list)
	dataset = defaultdict(list)
	hist_ = defaultdict(lambda : defaultdict(list))
	scatter_ = defaultdict(lambda : defaultdict(list))	
	fitting_ = defaultdict(lambda : defaultdict(list))
	for files in os.listdir(path):
		now = '0-0-0'
		oldPower = {}
		totalPower = {}
		totalTime = {}
		oldTime = {}
                fname = os.path.join(path,files)
                print fname
                try:
                        log = open(fname, 'r')
                except IOError:
                        print 'Cannot open json files'
                        break
                for line in log:
                        data = line.split()
                        if len(data) > 6:
                                json_dict = json.loads(line)
                                if json_dict.keys().count('UidInfo') == 1:
					dict_ = checkPattern(json_dict['UidInfo'])
                                        name = dict_['UidName']
#					print name, ' ------- ', now
					if now == '0-0-0':
						now = json_dict['Date']
#						print now
					if now !=json_dict['Date']:
						index = date_.index(now)
						print index, now
						for keys in totalTime:
							if totalTime[keys] > 0:
								if totalPower[keys] == 0:
									print 'WTF!--------->', keys,' ',totalTime[keys]
								fitting_[keys]['power'].append(float(totalPower[keys])/1000)
								fitting_[keys]['time'].append(float(totalTime[keys])/1000)

						for keys in totalPower:
							if totalPower[keys] > 0:
								scatter_[keys]['power'].append(float(totalPower[keys])/1000)
								scatter_[keys]['time'].append(float(totalTime[keys])/1000)
							if totalPower[keys] < 0 or totalTime[keys] < 0:
								print keys,'   ',totalPower[keys],'  ',totalTime[keys]
						temp = calculateRatio(totalPower,totalTime)
						
						for keys in temp:
							if temp[keys] > 0.0 :
								hist_[now][keys].append(temp[keys])
								dataset[keys].append(float(temp[keys]))
							if temp[keys] < 0:
								print keys, '   ', temp[keys]
							if keys not in powerMax:
								for i in xrange(0,len(date_)):
									powerMax[keys].append(float(0.0))
									powerMin[keys].append(float(0.0))
							if temp[keys] > powerMax[keys][index]:
								powerMax[keys][index] = temp[keys]
							elif temp[keys] < powerMin[keys][index] or powerMin[keys][index] == 0.0:
								powerMin[keys][index] = temp[keys]
						
						now = json_dict['Date']
						for keys in totalTime:
							oldTime[keys] = 0
							oldPower[keys] = 0
							totalTime[keys] = 0
							totalPower[keys] = 0
					
                                        child_ = DRESSUP.finditer(dict_['PerUidPerTypeInfo'])
                                        for match in child_:
                                                child = checkPattern(match.group('items'))
                                                if child['Type'] == 'STATS_SINCE_CHARGED':
							new_t = float(child[time])
							new_p = float(child['Power'])
#							print new_t, new_p
							try:
								if oldPower[name] < new_p and oldTime[name] < new_t:
									totalTime[name] = totalTime[name] + (new_t-oldTime[name])
									totalPower[name] = totalPower[name] + (new_p - oldPower[name])
								else:
									totalTime[name] = totalTime[name] + new_t
									totalPower[name] = totalPower[name] + new_p
							except:
								oldTime[name] = new_t
								oldPower[name] = new_p
								totalTime[name] = new_t
								totalPower[name] = new_p
		log.close()
		index = date_.index(now)
		print index, now
#                print totalPower
		for keys in totalTime:
			if totalTime[keys] > 0:
                        	fitting_[keys]['power'].append(float(totalPower[keys])/1000)
                                fitting_[keys]['time'].append(float(totalTime[keys])/1000)

		for keys in totalPower:
                	if totalPower[keys] > 0:
                        	scatter_[keys]['power'].append(float(totalPower[keys])/1000)
                                scatter_[keys]['time'].append(float(totalTime[keys])/1000)
                        if totalPower[keys] < 0 or totalTime[keys] < 0:
                        	print keys,'   ',totalPower[keys],'  ',totalTime[keys]


		temp = calculateRatio(totalPower,totalTime)
               	for keys in temp:
			if temp[keys] > 0.0:
				hist_[now][keys].append(temp[keys])
				dataset[keys].append(temp[keys])
			if keys not in powerMax:
                        	for i in xrange(0,len(date_)):
                                	powerMax[keys].append(float(0.0))
                                        powerMin[keys].append(float(0.0))

			if temp[keys] > powerMax[keys][index]:
               	       	        powerMax[keys][index] = temp[keys]
                       	elif temp[keys] < powerMin[keys][index] or powerMin[keys][index]==0.0:
                               	powerMin[keys][index] = temp[keys]

			

#	print powerMax
	
#	for dates in hist_:
#		c = 0
#		for uid in hist_[dates]:
#			if max(hist_[dates][uid]) > 0 and len(hist_[dates][uid]) > 2:
#				print uid, '--->',hist_[dates][uid]
#				rubbish = 1
#				fig = figure(c, dpi=10)
#				hist(hist_[dates][uid],bins=25,rwidth = 0.25)
#				xlabel('Ratio = Power / %s ' % time, fontsize = 10)
#				title('Power/%s for %s on %s' % (time, uid , dates), fontsize = 10)
#				pp2.savefig(fig)
#				fig.clear()
#				close()
#			c = c + 1
#	for uid in dataset:
#		if max(dataset[uid]) > 0 and len(dataset[uid]) > 6:
#			avg = (max(dataset[uid]) + min(dataset[uid])) / 2
#			low = 0
#			high = 0
#			for i in xrange(0,len(dataset[uid])):
#				if dataset[uid][i] < avg:
#					low = low+1
#				else:
#					high = high+1
#			fig = figure(c, dpi=10)
#			if low > high:
#				dataset[uid].sort()
#				print uid, '    ',low, '        ', dataset[uid][:low]
#				hist(dataset[uid][:low],bins=25,rwidth = 0.25)
#			else:
#				dataset[uid].sort()
#				dataset[uid].reverse()
#				print uid, '     ', high, '       ', dataset[uid][:high]
#				hist(dataset[uid][:high],bins=25,rwidth = 0.25)
				
#			fig = figure(c, dpi=10)
#			hist(new_list,bins=25,rwidth = 0.25)
#			xlabel('Ratio = Power / %s ' % time, fontsize = 10)
#			title('Power/%s for %s' % (time, uid), fontsize = 10)
#			pp2.savefig(fig)
#			fig.clear()
#			close()
#			c = c + 1

	if opt == 'scatter1':
		getUidScatter(fname2,'time','power',time, 'power',scatter_)
	if opt == 'fitting':
		getLinearRegress(fname2,'time','power',fitting_)

#	pp2.close()
			

#	for i in xrange(0,len(date_)):
#		X = []
#		Y = []
#		uidName = []
#		count = 10
#		for key, val in sorted(powerMax.iteritems(),key=lambda (k,v): v[i], reverse=True):
#			if count > 0:
#				uidName.append(key)
#				X.append(powerMax[key][i])
#				Y.append(powerMin[key][i])
#				count = count - 1
#		print X
#		print Y	
#		fig = figure(i, dpi=10)
#		N = arange(len(uidName))
#
#		bar(N, +X, facecolor='#9999ff', edgecolor='white')
#		bar(N, -Y, facecolor='#ff9999', edgecolor='white')
#		for x,y in zip(N,X):
#			text(x+0.4, y+0.05, '%.2f' % y, ha='center', va= 'bottom')
#
#		for x,y in zip(N,Y):
#			text(x+0.4, -y-0.05, '%.2f' % y, ha='center', va= 'top')

#		xticks[uidName]
#		title('Over whole testbed on %s' % date_[i])
#		pp.savefig(fig)
#        	fig.clear()
#        	close()

#	pp.close()

#	pp.close()

