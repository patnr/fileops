#!/usr/bin/env python3

import os
#import sys
# from subprocess import check_output
from contextlib import contextmanager
import re
#import string 

wd = os.getcwd()
# wd = os.path.expanduser("~/Dropbox/DPhil/DAPPER")

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

def print_c(*kargs,color='blue',**kwargs):
  if   color=='blue':  cc = '\033[94m'
  elif color=='green': cc = '\033[92m'
  elif color=='bold':  cc = '\033[1m' 
  s = ' '.join([str(k) for k in kargs])
  print(cc + s + '\033[0m', **kwargs)

def wc(filename, arg='-l'):
    output = check_output(["wc", arg, filename])
    return int(output.split()[0])

def file_tree_print():
  root_old = None
  for f_full, root, f_rel, f in walk(wd):
    root = os.path.relpath(root,wd)
    if root != root_old:
      root_old = root
      path = root.split(os.sep)
      print((len(path)-2)*'  |'+'  /',end='')
      print_c(os.path.basename(root))
    print(len(path)*'  |', f)


if __name__ == '__main__':
    file_tree_print()
    # wc()




