import os
import json
import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict


def generateAppsList(path):
	
	for root, dirs, files in os.walk('.'):
		filelist = []
		deviceapps=defaultdict(int)
		for name in files:
			extension = os.path.splitext(name)[1]
			if not "apps" in name: continue
			filelist.append(os.path.join(root,name))
		
		for f in filelist:
			try:
				log = open(f,'r')
			except IOError:
				print 'File doesnot exist'
				break;
			name = os.path.basename(f)
			appnames = []
			
			for line in log:
				deviceapps[line.strip()]+=1
			log.close()
				
		for w in sorted(deviceapps, key=deviceapps.get, reverse=True):
			print w, deviceapps[w]
	
generateAppsList('/home/ans25/theworks/logdata/test/Apps_Usage/')
