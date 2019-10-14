#!/usr/bin/env python3

import os
#import sys
# from subprocess import check_output
from contextlib import contextmanager
import re
#import string 

wd = os.getcwd()
# wd = os.path.expanduser("~/Dropbox/DPhil/DAPPER")

# flags = 0
flags = re.IGNORECASE

# Exclude: dirs
dx=["__pycache__",'.git',"other codes"]
# Include (only) dirs
di=[]
# di=["dapper"]
# Exclude: files
fx=[os.path.basename(__file__),'.so',".o"]
# Exclude: compared to full path
ax=[]
# Include (only) files
#fi=[".ipynb"]
fi=[]


def grep():
    for f_full, root, f_rel, f in walk(wd):
        with read(f_full) as F:
            lines = [line for line in F]

            matches = {}
            for pat in pats:
                matches[pat] = any(re.search(pat,line,flags) for line in lines)

            if all(matches.values()):
                for i,line in enumerate(lines):
                    for pat, do_print in pats.items():
                        if do_print:
                            m = re.search(pat,line,flags)
                            if m:
                                print_match(f_rel,i,line,m)


def walk(directory):
  for root, dirs, files in os.walk(wd):               # Walk dirs
    if any([s in root for s in dx]): continue         # exclude dirs
    if any([d in root for d in di]) or di==[]:        # include dirs
      for f in files:                                 # Loop files
        f_full = os.path.join(root,f)                 # add dirpath
        if any([s in f_full for s in ax]): continue   # exclude full path
        if any([s in f      for s in fx]): continue   # exclude files
        if any([s in f for s in fi]) or fi==[]:       # include files
            root, f = os.path.split  (f_full)
            f_rel   = os.path.relpath(f_full,wd)
            yield f_full, root, f_rel, f



@contextmanager
def read(fname):
    with open(fname) as f:
        try:
            yield f
        except UnicodeDecodeError:
            pass
def print_c(*kargs,color='blue',**kwargs):
  if   color=='blue':  cc = '\033[94m'
  elif color=='green': cc = '\033[92m'
  elif color=='bold':  cc = '\033[1m' 
  s = ' '.join([str(k) for k in kargs])
  print(cc + s + '\033[0m', **kwargs)

def print_match(path,i,line,match):
  info = path.ljust(40) + ' '+str(i).ljust(4)+': '
  print(info                         ,end ='')
  print(line[:match.span()[0]]       ,end ='')
  print_c(match.group(),color='green',end ='')
  print(line[match.span()[1]:]       ,end ='')

if __name__ == '__main__':
    grep()




