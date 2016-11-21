# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 13:01:41 2016

@author: user
"""

from itertools import combinations
import sys

table = 'baseline_table.dat'
base_thresh = 1000

with open(table) as f:
        lines = f.readlines()
ids = []
date = []
base = []

#prepare data
for i in range(len(lines)):
    new = lines[i].split()
    ids.append(new[0])
    date.append(new[1][0:7])
    base.append(float(new[4]))

data = zip(ids,date,base)
#sort by baseline
data.sort(key=lambda a:a[2])

#primary
primary = []
last_row = None
for row in data:
    #sort primary pairs into groups by threshold distance and year
    if last_row is not None and abs(row[2]) < 800:
        if abs(int(row[1][0:4]) - int(last_row[1][0:4])) < 2 and row[2] != 0:
            primary.append(row)  

#secondary        
secondary = []
last_row = None
for row in primary:
    try:
        if last_row is not None and abs(row[2]) < 800:
            if abs(int(row[1][0:4]) - int(last_row[1][0:4])) < 2 and row[2] != 0:
                primary.append(row) 
    
#sort secondary pairs into groups by threshold distance and year        


#        primary.append([])
    last_row = row
#    primary[-1].append(row)
       
    