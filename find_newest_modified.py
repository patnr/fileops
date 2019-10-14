#!/usr/bin/python 3


import os
import datetime
import sys
#import re
#import time

remember_tm = 0
stamps = list()

for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    for fname in filenames:
        fullname = os.path.join(dirpath, fname)
        tm = os.path.getmtime(fullname)
        #stamps = stamps.append(tm)
        if tm > remember_tm:
            remember_tm = tm
            remember_name = fullname
            #print(fullname)
            #print(remember_tm)

remember_tm = datetime.datetime.fromtimestamp(remember_tm)
print(datetime.datetime.now().strftime("%Y-%m-%d"))
print(remember_name)

#print("------------")
#print("------------")

#for i in range(0,5):
    #print(filenames[i])
    #print(stamps[i])
