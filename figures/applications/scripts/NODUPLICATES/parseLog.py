import os
import json

def getLinesForTag(path, tag):
	dname = 'perdevicelogs'
	result_path = 'perdevicelogs'
	d = os.path.join('..',dname)
	if not os.path.exists(d):
		os.makedirs(d)

	
	try:
		logFile = open(path,'r')
	except IOError:
		print 'Cannot open logfile'
		return 0
	device_id = '0'
	for line in logFile:
		data = line.split();
		if device_id == '0':
			device_id = data[0]
			fname  = os.path.join(d,data[0])
                        try:
                                targetFile = open(fname,'a')
                        except IOError:
                                print 'Cannot open'
                                print fname
                                print 'Parsing Aborted'
                                return 0

		if not device_id == data[0]:
			targetFile.close()
			device_id = data[0]
			fname  = os.path.join(d,data[0])
			try:
				targetFile = open(fname,'a')
			except IOError:
				print 'Cannot open'
				print fname
				print 'Parsing Aborted'
				return 0
		if len(data) < 6:
			pass
		else:
			if (data[6].startswith(tag) or data[6].startswith('ActivityManager')):
				n = len(data)+1
				new_line = " ".join(data[1:n])
				#print new_line
				targetFile.write(new_line)
				targetFile.write('\n')
	targetFile.close()
	print '--------------Done Parsing---------------'
	logFile.close()		



def getBatteryUsageJson(path):
	result_path = '/home/ans25/theworks/logdata/test/'
	d = os.path.join(result_path,'Apps_Usage')
        if not os.path.exists(d):
                os.makedirs(d)
	
	for root, dirs, files in os.walk(path):
		print root
		print dirs
		print files
		filelist = []
		for name in files:
			filelist.append(os.path.join(root,name))
		for f in filelist:
			try:
				log = open(f,'r')
			except IOError:
				print 'File doesnot exist'
				break;
			name = os.path.basename(f)
			fname = os.path.join(d,name.split('.')[0]+'.json')
			print fname
			jsonFile = open(fname,'w')
			for line in log:
				data = line.split()
				if len(data) > 10 and data[5].startswith('PhoneLabSystemAnalysis-Snapshot') and data[6].startswith('{'):
					new_line = " ".join(data[6::])
					#print new_line
					jsonObj = json.loads(new_line)
					for key in jsonObj:
						if key == 'InstalledUserApp':
							jsonObj['Timestamp']=data[1]
							jsonObj['Date'] = data[0]
							jsonFile.write(json.dumps(jsonObj))
							jsonFile.write('\n')
							#print json.dumps(jsonObj)
							break
			jsonFile.close()
			log.close()


 
	
getLinesForTag('bigdump','PhoneLabSystemAnalysis')
#getBatteryUsageJson('/home/ans25/theworks/logdata/test/PhoneLabSystemAnalysis')
