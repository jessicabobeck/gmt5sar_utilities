# -*- coding: utf-8 -*-
"""
@author: Jessica Bobeck
Utility for creating align.in and intf.in files.

IN:
	table - table.gmt file (found in raw dir)
	master - name of master or super master that image will align too
	threshold - threshold for small baseline subsets, set to 0 if you do not want a  threshold.
                  It will separate out subgroups based on your threshhold and create all possible
                  combinations for that subset.
	sat - satellite (ALOS, ENVI, ERS, S1A)
OUT:
	intf.in
     align.in

USAGE:

	Use from command line.It can be put in a .csh or .sh file. For example:

	#linking table.gmt file
		ln -s raw/baseline_table.dat .
	#making align.in
		python makeInputFiles.py table.gmt IMG-HH-ALPSRP052541220-H1.0__A 10000 ALOS align
	#running align script
		align_batch.csh ALOS align.in
	#making intf.in
		python makeInputFiles.py table.gmt IMG-HH-ALPSRP052541220-H1.0__A 10000 ALOS intf
	#running intf script
		intf_batch.csh ALOS intf.in intf.config
"""
from itertools import combinations
import sys

def makeInputFiles(table, master, threshold, sat):
    
    #open file
    with open(table) as f:
        lines = f.readlines()
        
    #prepare data
    data = []
    for i in range(len(lines)):
        new = lines[i].split()
        new[1] = float(new[1])
        data.append(new)
#     
#        
#    #sort by baseline
#    data.sort(key=lambda a:a[1])
#    groups = [[]]
#    last_row = None
#    for row in data:
#        #sort into groups by threshold
#        if last_row is not None and row[1] - last_row[1] > threshold:
#            groups.append([])
#        last_row = row
#        groups[-1].append(row)
#        
#    #grab just ids and sort combinations
#    img = []
#    for j in range(len(groups)):
#        ids = []
#        for id in groups[j]:
#            ids.append(id[-1])
#        img.append(list(set(combinations(ids, 2))))
#    
#    #---------------------sat type-------------------------------------------------
#    if sat == 'ALOS':
#        stem = master[0:13]
#        end = master[18:]
#    
#    elif sat == 'ENVI':
#        pass
#    #not done yet
#        
#    elif sat == 'S1A':
#        pass
#    #not done yet
#    
#    else:
#        sys.exit('Not a valid sat input: Please choose from ALOS, ENVI, or S1A')
#        
#
#    align = open('align.in', 'w+')
#    for k in range(len(img)):
#        for line in img[k]:
#            align.write(stem + line[0] + end + ':' + stem + line[1] + end + ':'
#            + master + '\n')   
#    align.close()
#
#
#    intf = open('intf.in', 'w')
#    for k in range(len(img)):
#        for line in img[k]:
#            intf.write(stem + line[0] + end + ':' + stem + line[1] + end + '\n')
#    intf.close()
#
#if __name__ == '__main__':
#    table= str(sys.argv[1])
#    master=str(sys.argv[2])
#    threshold=int(sys.argv[3])
#    sat=str(sys.argv[4])
#    makeInputFiles(table, master, threshold, sat)
