#!/usr/bin/python

import os, pickle

# info.pickle is a dictionary object where a key is a hashed MEID and a value is
# Info class in info.py
# 
# Possible values for Info class are:
# 
# standing: 'Not Affiliated', 'Freshman', 'Sophomore', 'Junior', 'Senior',
#           'Master', 'PhD', 'Professional', 'Faculty', 'Staff'
# gender: 'Male', 'Female'
# ageband: 'Under 18', '18 - 19', '20 - 21', '22 - 24', '25 - 29', '30 - 34',
#          '35 - 39', '40 - 49', '50 - 59', 'Over 60'

class Info:
  hashed_meid = ''
  standing = ''
  gender = ''
  ageband = ''

if __name__ == "__main__":
  file = open('all.out', 'r')
  output = open('info.pickle', 'w')  

  map = {}
  for line in file:
    info = Info()

    line = line.strip()
    values = line.split(',')

    id = values[0].strip().lower()
    email = values[1].strip().lower()
    meid = values[2].strip()
    info.hashed_meid = values[3].strip()

    standing = values[4].strip()
    if 'Master' in standing:
      standing = 'Master'
    elif 'Doctoral' in standing:
      standing = 'PhD'
    elif 'Professional' in standing:
      standing = 'Professional'
    info.standing = standing

    info.gender = values[5].strip()
    info.ageband = values[6].strip()

    map[info.hashed_meid] = info

  pickle.dump(map, output)
  file.close()
  output.close()
