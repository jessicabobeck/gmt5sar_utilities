# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 19:08:39 2016

@author: user
"""

import os


os.chdir('intf')
path = os.getcwd()

dirs = os.listdir(path)

f = open('snap_all.csh', 'w')
for i in range(len(dirs)):
    if i == 0:
        f.write('cd ' + dirs[i] + '\n')
    else:
        f.write('cd ../' + dirs[i] + '\n')  
    f.write('snaphu.csh 0.01 0\n')
    f.write('geocode.csh 0.01\n')    
    
f.close()
    