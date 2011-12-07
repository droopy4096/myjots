#!/usr/bin/python

import os
from os.path import join, getsize
for root, dirs, files in os.walk('/home/dimon/Notes'):
    print (root,str(dirs),files)
