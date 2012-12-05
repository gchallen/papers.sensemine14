import os

d='../NODUPLICATES'
if not os.path.exists(d):
    os.makedirs(d)

for root, dirs, files in os.walk('.'):
    #print root
    #print dirs
    #print files
    filelist = []
    for name in files:
        if 'out' in name: 
            filelist.append(os.path.join(root,name))
    print filelist
    for f in filelist:
        log = open(f,'r')
        fname = os.path.join(d,os.path.basename(f))
        print 'parsing ', os.path.basename(f)
        w = open(fname,'w')
        s=[]
        tmpmap = {}
        for line in log:
            if line not in tmpmap:
                tmpmap[line]=1
                s.append(line)
        print 'finished, len = ', len(s)
        #ss = set(s) 
        #print 'removed duplicates, len = ', len(ss)
        for strr in s:
            w.write(strr)
        log.close()
        w.close()

