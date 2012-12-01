import os
import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import *
from datetime import datetime
from collections import defaultdict
import re


MESSY = re.compile(r"""(?P<key_name>.*?):\s+(?P<value>(?:\[.*?\]|[\w.\-]*))[,\s]*""",re.VERBOSE)
DRESSUP = re.compile(r"""\(+(?P<items>.*?)\)[,\s]*""",re.VERBOSE)

def checkPattern(gibberish):
        dict_ = {}
        info = MESSY.finditer(gibberish)

        if not info == None:
                for match in info:
                        key = match.group('key_name')
                        value = match.group('value')
                        dict_[key] = value

        return dict_




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
                        if len(line) > 0:
                                json_dict = json.loads(line)
                                if dates_.count(json_dict['Date']) == 0:
                                        dates_.append(json_dict['Date'])

        return dates_



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




def getLinearRegressWithLog(path,fname,xtag,ytag,xname,yname,dict_):
        pp = PdfPages(fname)
        c = 0
        target = open(path,'w')

        for uid in dict_:
                if max(dict_[uid][xtag]) > 0 and max(dict_[uid][ytag]) > 0 and len(dict_[uid][ytag]) > 100:
                        logx = np.log2(dict_[uid][xtag])
                        logy = np.log2(dict_[uid][ytag])
                        k,b = np.polyfit(logx,logy,1)
                        x = arange(min(dict_[uid][xtag]),len(dict_[uid][xtag]),100)
                        fig = figure(c, dpi= 10)
                        gca().set_xscale('log', basex = 2)
                        gca().set_yscale('log', basey = 2)
                        plot(dict_[uid][xtag],dict_[uid][ytag],'ro')

                        plot(dict_[uid][xtag],pow(2,b)*pow(dict_[uid][xtag],k),'b')

                        yhat = [k*z+b for z in np.log2(dict_[uid][xtag])]
                        ybar = sum(np.log2(dict_[uid][ytag]))/len(dict_[uid][ytag])
                        ssreg = sum([ (yihat - ybar)**2 for yihat in yhat])
                        sstot = sum([ (yi - ybar)**2 for yi in np.log2(dict_[uid][ytag])])
                        r_sq = ssreg / sstot

                        target.write('Uid = %s k = %s b = %s r^2 = %s\n' % (uid,k,b,r_sq))

                        xlabel('%s in Second' % xname, fontsize = 10)
                        ylabel('%s in mA-Sec' % yname, fontsize = 10)
                        title('%s/%s for %s ' % (yname,xname,uid), fontsize = 10)
                        annotate('k = {0:.3f}'.format(k), (0.9, 0.09), xycoords='axes fraction',fontsize = 8)
                        annotate('b = {0:.3f}'.format(b), (0.9,0.07), xycoords='axes fraction',fontsize = 8)
                        annotate('r^2 = {0:.3f}'.format(r_sq), (0.8,0.05), xycoords='axes fraction',fontsize = 8)
                        grid(True,which="both",ls="-")
                        pp.savefig(fig)
                        fig.clear()
                        close()
                        c = c + 1
        pp.close()
        target.close()

def getLinearRegressWithoutLog(data,fname,xtag,ytag,xname,yname,dict_):
	pp = PdfPages(fname)
        c = 0
        target = open(data,'w')

        for uid in dict_:
                if max(dict_[uid][xtag]) > 0 and max(dict_[uid][ytag]) > 0 and len(dict_[uid][ytag]) > 100:
                        k,b = np.polyfit(dict_[uid][xtag],dict_[uid][ytag],1)                    
                        fig = figure(c, dpi= 10)
                        gca().set_xscale('log', basex = 2)
                        gca().set_yscale('log', basey = 2)

                        yhat = [k*z+b for z in dict_[uid][xtag]]
                        ybar = sum(dict_[uid][ytag])/len(dict_[uid][ytag])
                        ssreg = sum([ (yihat - ybar)**2 for yihat in yhat])
                        sstot = sum([ (yi - ybar)**2 for yi in dict_[uid][ytag]])
                        r_sq = ssreg / sstot

			print len(dict_[uid][xtag]),len(yhat)
                        plot(dict_[uid][xtag],dict_[uid][ytag],'ro')
                        plot(dict_[uid][xtag],yhat,'bo')

                        target.write('Uid = %s k = %s b = %s r^2 = %s\n' % (uid,k,b,r_sq))

                        xlabel('%s in Second' % xname, fontsize = 10)
                        ylabel('%s in mA-Sec' % yname, fontsize = 10)
                        title('%s/%s for %s ' % (yname, xname, uid), fontsize = 10)
                        annotate('k = {0:.3f}'.format(k), (0.9, 0.09), xycoords='axes fraction',fontsize = 8)
                        annotate('b = {0:.3f}'.format(b), (0.9,0.07), xycoords='axes fraction',fontsize = 8)
                        annotate('r^2 = {0:.3f}'.format(r_sq), (0.8,0.05), xycoords='axes fraction',fontsize = 8)
                        grid(True,which="both",ls="-")
                        pp.savefig(fig)
                        fig.clear()
                        close()
                        c = c + 1
        pp.close()
        target.close()



#example:summaryByUid('/home/anudipa/phonelab/Experiment Logs/Subset','CpuFgTime','fitting','/home/anudipa/phonelab/Experiment Logs')

def summaryByUid(path,time, opt,out_path):
        d = os.path.join(out_path,'graphs/perUid')
        if not os.path.exists(d):
                os.makedirs(d)

	if opt == 'scatter':
                variableName = 'PowerBy'+time+'Scatter.pdf'
        elif opt == 'fitting':
                variableName = 'PowerBy'+time+'Fitting.pdf'
        fname1 = os.path.join(d,variableName)

	date_ = getAllDates(path)
        print date_

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
                        if len(line) == 0:
                                continue
                        data = line.split()
                        if len(data) > 6:
                                json_dict = json.loads(line)
                                if json_dict.keys().count('UidInfo') == 1:
                                        dict_ = checkPattern(json_dict['UidInfo'])
                                        name = dict_['UidName']
					if now == '0-0-0':
                                                now = json_dict['Date']
					if now !=json_dict['Date']:
                                                index = date_.index(now)
                                                print index, now
                                                for keys in totalTime:
                                                        if totalTime[keys] > 0 and totalPower[keys] > 0:
                                                                fitting_[keys]['power'].append(float(totalPower[keys])/1000)
                                                                fitting_[keys]['time'].append(float(totalTime[keys])/1000)

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
#                                                       print new_t, new_p
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
                try:
                        index = date_.index(now)
                except:
                        continue
                print index, now
		for keys in totalTime:
                        if totalTime[keys] > 0 and totalPower[keys] > 0:
                                fitting_[keys]['power'].append(float(totalPower[keys])/1000)
                                fitting_[keys]['time'].append(float(totalTime[keys])/1000)


	if opt == 'scatter':
                getUidScatter(fname2,'time','power',time, 'Power',scatter_)
        if opt == 'fitting':
		filename = os.path.join(out_path,'coefficients.txt')
                getLinearRegressWithoutLog(filename,fname1,'time','power',time,'Total Power',fitting_)
#		getLinewRegressWithLog(filename,fname1,'time','power',time,'Total Power',fitting_)	
	
