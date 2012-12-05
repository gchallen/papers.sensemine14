import os

directory = os.path.join('..','logswithexp')
if not os.path.exists(d):
    os.makedirs(d)

for root,dirs,files in os.walk('.'):
    for f in files:
        log = open(f,'r')
        for line in log:
            if 'SystemAnalysis-Snapshot' in line:
                print os.path.basename(f)
                os.system('cp os.path.basename(f) ../logswithexp')
                break
