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
     algorithm - all: every possible combination (least selective)
                 baseline: pairs matched by baseline theshold (moderatly selective)
                 leapfrog: GMT5SAR recommended algorithm that splits pairs up
                           into primary, secondary and tertiary pairs (highly selective)
     
OUT:
	intf.in
     align.in

USAGE:

	Use from command line.It can be put in a .csh or .sh file. For example:

	#linking table.gmt file
		ln -s raw/baseline_table.dat .
	#making align.in
		python makeInputFiles.py baseline_table.dat IMG-HH-ALPSRP052541220-H1.0__A 10000 ALOS baseline prim_base=10000
	#running align script
		align_batch.csh ALOS align.in
	#running intf script
		intf_batch.csh ALOS intf.in intf.config
"""
import itertools as it
import sys
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors
import numpy as np


def get_cmap(N):
    '''Returns a function that maps each index in 0, 1, ... N-1 to a distinct 
    RGB color.'''
    color_norm  = colors.Normalize(vmin=0, vmax=N-1)
    scalar_map = cmx.ScalarMappable(norm=color_norm, cmap='hsv') 
    def map_index_to_rgb_color(index):
        return scalar_map.to_rgba(index)
    return map_index_to_rgb_color




table = 'baseline_table.dat'
master = 'IMG-HH-ALPSRP052541220-H1.0__A'
sat = 'ALOS'
algorithm = 'baseline'
prim_base = 10000

def makeInputFiles(table, master, sat, algorithm, prim_base=800, prim_year=2,
                   sec_base=1500, sec_year=1, ter_base=500, ter_year=2):

    #open table
    with open(table) as f:
        lines = f.readlines()
    ids = []
    date = []
    base = []

    
    #prepare data
    for i in range(len(lines)):
        new = lines[i].split()
        ids.append(new[0])
        date.append(int(new[1][0:7]))
        base.append(float(new[4]))
    
    data = zip(date,base)
    #sort by baseline
    data.sort(key=lambda a:a[1])
    
    #--------------------------Algorithm---------------------------------------------
    
    #BASELINE---------------------------------
    if algorithm == 'baseline':
        groups = [[]]
        last_row = None
        for row in data:
            #sort into groups by threshold
            if last_row is not None and row[1] - last_row[1] > prim_base:
                groups.append([])
            last_row = row
            groups[-1].append(row)
            

    comb = []
    for j in range(len(groups)):
        print it.combinations(groups[j], 2)
#        comb.append(list(set(it.combinations(groups[j], 2))))
        
    #plot
    fig1 = plt.figure(figsize=(22,18))
    ax = fig1.add_subplot(111)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    
    cmap = get_cmap(len(groups))
    for j in range(len(groups)):
        ax.plot(
        *zip(*it.chain.from_iterable(it.combinations(groups[j], 2))),
        color=cmap(j), marker = 'o')
    for i in range(len(date)):
        ax.scatter(date[i],base[i])
        plt.annotate(ids[i],(date[i],base[i]))

        
#        for j in range(len(comb[i])):
#            x = comb[i][j][1]
##            ax.plot(comb[i],j[2], c=color(i))
    
#    
#    #LEAPFROG--------------------------------
#    elif algorithm == 'leapfrog':
#        #primary
#        primary = []
#        last_row = None
#        for row in data:
#            #sort primary pairs into groups by threshold distance and year
#            if last_row is not None and abs(row[2]) < prim_base:
#                if abs(int(row[1][0:4]) - int(last_row[1][0:4])) < prim_year and row[2] != 0:
#                    primary.append(row)  
#            last_row = row
#        
#        #secondary        
#        secondary = []
#        last_row = None
#        if len(primary) == 0:
#            sys.exit('makeInputFiles Error: There is only 1 primary image (supermaster). Adjust thresholds.')
#        else:
#            for row in primary:
#                #sort secondary pairs into groups by threshold distance and year   
#                if last_row is not None and abs(row[2]) < sec_base:
#                    if abs(int(row[1][0:4]) - int(last_row[1][0:4])) < sec_year and row[2] != 0:
#                        secondary.append(row) 
#                        
#        #tertiary
#        tertiary = []
#        last_row = None
#        if len(secondary) == 0:
#            sys.exit('makeInputFiles Error: There is only 1 secondary image (submaster). Adjust thresholds.')
#        else:
#            for row in secondary:
#                #sort secondary pairs into groups by threshold distance and year   
#                if last_row is not None and abs(row[2]) > ter_base:
#                    if abs(int(row[1][0:4]) - int(last_row[1][0:4])) > ter_year:
#                        tertiary.append(row) 
#        groups = []
#        groups.append(primary,secondary,tertiary)
#        
#    #ALL------------------------------------------
#    else:
#        for row in data:
#        pass
#            
#    
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
#    #-----------------------Making files---------------------------------------------
#    align = open('align.in', 'w+')
#    for k in range(len(groups)):
#        for line in groups[k]:
#            align.write(stem + line[0] + end + ':' + stem + line[1] + end + ':'
#            + master + '\n')   
#    align.close()
#
#
#    intf = open('intf.in', 'w')
#    for k in range(len(groups)):
#        for line in groups[k]:
#            intf.write(stem + line[0] + end + ':' + stem + line[1] + end + '\n')
#    intf.close()
#    
#
##
##if __name__ == '__main__':
##    table= str(sys.argv[1])
##    master=str(sys.argv[2])
##    threshold=int(sys.argv[3])
##    sat=str(sys.argv[4])
##    makeInputFiles(table, master, threshold, sat)
