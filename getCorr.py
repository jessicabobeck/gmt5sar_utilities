# -*- coding: utf-8 -*-
"""
@author: Jessica Bobeck
@date: Nov. 2016
@purpose: Filtering out bad correlation files.
"""
import os
import shutil

os.chdir('intf')
path = os.getcwd()

dirs = os.listdir(path)

for i in dirs:
    print os.getcwd()
    os.chdir('../intf/'+i)
    try:
        size = os.path.getsize('corr.ps')
    except OSError:
        os.chdir('../')
        os.removedirs(i)
    if size/1000000. < 6.25:
        os.chdir('../../corr')
        try:
            os.mkdir(i)
        except OSError:
            os.rmdir(i)
            os.mkdir(i)
        shutil.move('../intf/' +i , '.')
        print os.getcwd()
        os.chdir('../intf')
    else:
        os.chdir('../')
