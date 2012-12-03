#!/usr/bin/env python

import argparse, pickle
from common.lib import hash_logs, ARCHIVE_MD5SUM_PICKLE_FILENAME

def add_md5sum(archive_directory):
  pickle.dump(hash_logs(archive_directory),
              open(os.path.join(archive_directory, ARCHIVE_MD5SUM_PICKLE_FILENAME), 'wb'),
              pickle.HIGHEST_PROTOCOL)
          
parser = argparse.ArgumentParser(description="util package for MobiSys'13 graphs")
parser.add_argument('--md5sum', dest='md5sum', action='store', default=None, help='Add md5sum pickle to existing archive.')
args = parser.parse_args()
    
if args.md5sum != None:
  add_md5sum(args.md5sum)
    
