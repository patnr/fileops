#!/usr/bin/env python3

import os
#import sys
# from subprocess import check_output
from contextlib import contextmanager
import re
#import string 

wd = os.getcwd()
# wd = os.path.expanduser("~/Dropbox/DPhil/DAPPER")

LOCKED = False # failsafe on top of dry_run for replacement

# Search pattern
# pat=r"\bP\b"          # Find M
# pat=r"(?<=\.)\s*M\b"  # Find M     preceeded by .
# pat=r"(?<![\.\s])M\b" # Find M not preceeded by .
pat=r"sector"

rep = None  # No replacement -- only search
rep = r'HECTOR' # replace pattern
# rep = "cfgs+=\1\2" # search pattern

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


def additional_conditions(line,filename,dirname):
  # return "Var4D" not in line
  return True

def replace(dry_run=True,do_print=True):
    for f_full, root, f_rel, f in walk(wd):
        with rewrite(f_full) as lines:
            for i,line in enumerate(lines):

                m = re.search(pat,line,flags)

                if m and additional_conditions(line,root,f):

                    if do_print:
                        print_match(f_rel,i,line,m)

                    if rep is not None:
                        newline = re.sub(pat, rep, line)
                        if dry_run:
                            print_change(newline)
                        else:
                            lines[i] = newline

    # Repeat (recurse once) to effectuate changes
    if dry_run and rep is not None and LOCKED is False:
        print("Are you sure you want these changes?")
        if flags!=0: print_c("Note!: flags are set:",flags)
        print("[y/n]: ",end="")
        if input().lower() in ['y', 'ye', 'yes']:
            replace(dry_run=False,do_print=False)
            print("Changes done.")
        else:
            print("User abort. No changes made.")


pats = {'rms.*observed':1,
        'lorenz.96':0,
        'assimilation':0}

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

@contextmanager
def rewrite(fname):
    """Work with lines as a list, to be modified in-place"""

    # READ
    with open(fname, 'r') as f:
        try:
            lines = [line for line in f]
        except UnicodeDecodeError:
            lines = []

    # TRACK CHANGES (bool) in lines
    def monitor_setitem(cls):
        class Monitored(cls):
            "Keep track of whether setitem has been called."
            def     __init__(self,*args,**kwargs):
                cls.__init__(self,*args,**kwargs); self.were_changed = False
            def     __setitem__(self,key,value):
                cls.__setitem__(self,key,value);   self.were_changed = True
        return Monitored
    lines = monitor_setitem(list)(lines) 

    # OUTSIDE WORK
    yield lines
    
    # WRITE
    if lines.were_changed:
        with open(fname, 'w') as f:
            f.write("".join(lines))

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

def print_change(newline):
    arrow = '--> '
    print(' '*(47-len(arrow)) + arrow + newline, end='')


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
    # file_tree_print()
    # wc()
    # replace()
    grep()



