#!/usr/bin/python

from info import *
import os, pickle

if __name__ == "__main__":
  file = open('info.pickle')
  map = pickle.load(file)

  standing_cnt = {}
  gender_cnt = {}
  ageband_cnt = {}

  for k, v in map.iteritems():
    hashed_meid = k
    standing = v.standing
    gender = v.gender
    ageband = v.ageband

    if standing in standing_cnt:
      standing_cnt[standing] = standing_cnt[standing] + 1
    else:
      standing_cnt[standing] = 1

    if gender in gender_cnt:
      gender_cnt[gender] = gender_cnt[gender] + 1
    else:
      gender_cnt[gender] = 1

    if ageband in ageband_cnt:
      ageband_cnt[ageband] = ageband_cnt[ageband] + 1
    else:
      ageband_cnt[ageband] = 1

  print standing_cnt
  print gender_cnt
  print ageband_cnt
