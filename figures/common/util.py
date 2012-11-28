#!/usr/bin/env python

import os, argparse, hashlib, pickle

def add_md5sum(archive_directory):
  md5sums = {}
  for dirname, unused, filenames in os.walk(archive_directory):
    for filename in filenames:
      md5 = hashlib.md5()
      with open(os.path.join(dirname, filename), 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
          md5.update(chunk)
      md5sums[filename] = md5.hexdigest()
  pickle.dump(md5sums, open(os.path.join(archive_directory, 'md5sums.pickle'), 'wb'), pickle.HIGHEST_PROTOCOL)
          
parser = argparse.ArgumentParser(description="util package for MobiSys'13 graphs")
parser.add_argument('--md5sum', dest='md5sum', action='store', default=None, help='Add md5sum pickle to existing archive.')
args = parser.parse_args()
    
if args.md5sum != None:
  add_md5sum(args.md5sum)
    
