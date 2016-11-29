# -*- coding: utf-8 -*-
"""
@author: Jessica Bobeck
@date: Nov. 2016
@purpose: Utility for making align.in and intf.in files for GMT5SAR
"""
import itertools as it
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import argparse


parser = argparse.ArgumentParser(description='Utility for creating align.in and intf.in files.')
parser.add_argument('table', help='GMT Baseline Table (ex. baseline_table.dat)', type=str)
parser.add_argument('master', help='Name of master or super master that image will align to', type=str)
parser.add_argument('sat', type=str, help='Satellite Type', choices=['ALOS', 'ERS', 'ENVI'])
parser.add_argument('algorithm', type=str, help='Algorithm, specific descriptions are found in README', choices=['baseline', 'leapfrog', 'all'])
parser.add_argument('prim_base', type=int, help='Baseline Threshold. Default=800 [m]. (Primary Baseline threshold for leap frog algorithm)' ,default=800)
parser.add_argument('--py', help='Primary Year Threshold. Default=2 [y]. Required for leapfrog algorithm only.', type=int, default=2)
parser.add_argument('--sb', help='Secondary Year Threshold. Default=1500 [m]. Required for leapfrog algorithm only.', type=int, default=1500)
parser.add_argument('--sy', type=int, help='Secondary Year Threshold. Default=2 [y]. Required for leapfrog algorithm only.', default=2)
parser.add_argument('--tb', type=int, help='Tertiary Baseline Threshold. Default=5000 [m] Required for leapfrog algorithm only.', default=5000)
parser.add_argument('--ty', type=int, help='Tertiary Year Threshold. Default=1 [y]. Required for leapfrog algorithm only.', default=1)

args = parser.parse_args()

table = args.table
master = args.master
sat = args.sat
algorithm = args.algorithm
prim_base = args.prim_base
prim_year = args.py
sec_base = args.sb
sec_year = args.sy
ter_base = args.tb
ter_year = args.ty

'''*****************************-sat type-**********************************'''
if sat == 'ALOS':
    stem = master[0:13]
    end = master[18:]

elif sat == 'ENVI':
    pass
#not done yet
    
elif sat == 'ERS':
    pass
#not done yet

else:
    sys.exit('Not a valid sat input: Please choose from ALOS, ENVI, or ERS')

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
    date.append(new[1][0:7])
    base.append(float(new[4]))
data = zip(date,base,ids)

#sort by baseline
data.sort(key=lambda a:a[1])

for row in data:
    if row[1] == 0:
        m = row

'''****************************-Algorithm-**********************************'''

#-----------------------------BASELINE-----------------------------------------
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
        comb.append(list(set(it.combinations(groups[j], 2))))

    #____________________________plot__________________________________________ 
    rc('xtick', labelsize=20) 
    rc('ytick', labelsize=20)
    rc('lines', linewidth=3)
    fig1 = plt.figure(figsize=(22,18))
    ax = fig1.add_subplot(111)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.scatter(date,base,s=200, zorder=2)
    ax.set_xlabel('Year',fontsize=25)
    ax.set_ylabel('Baseline (m)',fontsize=25)
    ax.set_title('Baseline Method', fontsize=32)
    
    labels = []
    for i in range(len(comb)):
        for j in range(len(comb[i])):
            x = []
            y = []
            x.append(comb[i][j][0][0])
            x.append(comb[i][j][1][0])
            
            y.append(comb[i][j][0][1])
            y.append(comb[i][j][1][1])
            
            if comb[i][j][0][2] not in labels:
                plt.annotate(comb[i][j][0][2], (x[0], y[0]),
                             fontsize=16,horizontalalignment='right',
                             verticalalignment='bottom')
            labels.append(comb[i][j][0][2])
                
            if comb[i][j][1][2] not in labels:
                plt.annotate(comb[i][j][1][2], (x[1], y[1]),fontsize=16,
                             horizontalalignment='left',
                             verticalalignment='top') 
            labels.append(comb[i][j][1][2])
            
            ax.plot(x,y, c=np.random.rand(3,1), zorder=1)   
            
    
    plt.savefig('baseline_alignPairs.png', dpi=300)
    
    #_________________________Making files_____________________________________
    align = open('align.in', 'w')
    intf = open('intf.in', 'w')
    
    out = []
    for i in range(len(comb)):
        for pair in comb[i]:
            align.write(stem + pair[0][2] + end + ':' + stem + pair[1][2] + end + ':' + master + '\n')  
            intf.write(stem + pair[0][2] + end + ':' + stem + pair[1][2] + end + '\n')
            out.append(pair)
    align.close()       
    intf.close()
    
    print 'Number of pairs generated: ', len(out)  
    
    
              
#----------------------------LEAPFROG------------------------------------------
elif algorithm == 'leapfrog':
    
    #primary
    primary = []
    for row in data:
        #sort primary pairs into groups by threshold distance and year
        if abs(row[1]) < prim_base:
            if abs(int(row[0][0:4]) - int(m[0][0:4])) < prim_year and row[1] != 0:
                primary.append(row)  

    
    #secondary        
    secondary = []
    if len(primary) == 0:
        sys.exit('makeInputFiles Error: There is only 1 primary image (supermaster). Adjust thresholds.')
    else:
        for img in primary:
            temp = []
            for row in data:
                #sort secondary pairs into groups by threshold distance and year   
                if row[1] > (img[1] - sec_base) and row[1] < (img[1] + sec_base):
                    if abs(int(row[0][0:4]) - int(img[0][0:4])) <= sec_year and row[1] != img[1] and row[1] != 0:
                        if row not in primary:
                            temp.append(row) 
            secondary.append(temp)
                    
    #tertiary
    tertiary = []
    if len(secondary) == 0:
        sys.exit('makeInputFiles Error: There is only 1 secondary image (submaster). Adjust thresholds.')
    else:
        for s in range(len(secondary)):
            for img in range(len(secondary[s])):
                temp = []
                for row in data:
                    #sort secondary pairs into groups by threshold distance and year
                    if row[1] > (secondary[s][img][1] - ter_base) and row[1] < (secondary[s][img][1] + ter_base) and row[1] != 0:
                        if abs(int(row[0][0:4]) - int(secondary[s][img][0][0:4])) <= ter_year:
                            if row not in primary and row not in secondary[s]:
                                temp.append(row)
                tertiary.append(temp)             

    mx = m[0]
    my = m[1] 

        
    px = []
    py = []
    for data in primary:
        px.append(data[0])
        py.append(data[1])
        
    sx = []
    sy = []
    for data in secondary:
        for row in range(len(data)):
            sx.append(data[row][0])
            sy.append(data[row][1])
    
    tx = []
    ty = []
    for data in tertiary:
        for row in range(len(data)):
            tx.append(data[row][0])
            ty.append(data[row][1])
            
    #______________________________plot________________________________________
    rc('xtick', labelsize=20) 
    rc('ytick', labelsize=20)
    rc('lines', linewidth=3)
    fig1 = plt.figure(figsize=(22,18))
    ax = fig1.add_subplot(111)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.set_xlabel('Year',fontsize=25)
    ax.set_ylabel('Baseline (m)',fontsize=25)
    ax.set_title('Leapfrog Method', fontsize=32)
        
    for p in range(len(primary)):
        x=[]
        y=[]
        
        x.append(mx)
        x.append(primary[p][0])        
        
        y.append(my)
        y.append(primary[p][1])
        
        ax.plot(x,y, c='r', zorder=3)
        
        plt.annotate(m[2], (x[0], y[0]), fontsize=16,
                     horizontalalignment='right',
                     verticalalignment='bottom')
        plt.annotate(primary[p][2], (x[1], y[1]), fontsize=16,
                     horizontalalignment='right',
                     verticalalignment='bottom')
        
        count = 0
        for s in range(len(secondary)):
            if s == p:
                for i in range(len(secondary[s])):
                    x=[]
                    y=[]
                    x.append(primary[p][0])
                    x.append(secondary[s][i][0])
                    
                    y.append(primary[p][1])
                    y.append(secondary[s][i][1])
                    
                    ax.plot(x,y, c='y', zorder=2)
                    
                    plt.annotate(secondary[s][i][2], (x[1], y[1]),
                                 fontsize=16,horizontalalignment='right',
                                 verticalalignment='bottom')
                    
                    for t in range(len(tertiary)):
                        if count == t:
                            for j in range(len(tertiary[t])):
                                x=[]
                                y=[]
                                x.append(secondary[s][i][0])
                                x.append(tertiary[t][j][0])
                                
                                y.append(secondary[s][i][1])
                                y.append(tertiary[t][j][1])
                                
                                ax.plot(x,y, c='g', zorder=1)
                                
                                plt.annotate(tertiary[t][j][2], (x[1], y[1]), 
                                             fontsize=16,
                                             horizontalalignment='right',
                                             verticalalignment='bottom')
                    count = count + 1
    
    ax.scatter(tx,ty, s=150, c='g', zorder=4)
    ax.scatter(sx,sy,s=150, c='y', zorder=4)
    ax.scatter(px,py,s=150, c='r', zorder=4)
    ax.scatter(mx,my,s=300, c='b', marker='*' , zorder=4)
    
    plt.savefig('leapfrog_alignPairs.png', dpi=300)
    
    #_________________________Making files_____________________________________
    count = 0 
    check = []
    align = open('align.in', 'w')
    intf = open('intf.in', 'w')
    for i in range(len(primary)):
        align.write(master + ':' + stem + primary[i][2] + end + ':'
        + master + '\n')  
        intf.write(master + ':' + stem + primary[i][2] + end + '\n')
        
        for j in range(len(secondary[i])):
            align.write(stem + primary[i][2] + end + ':' + stem + secondary[i][j][2] + end + ':'
            + master + '\n')  
            intf.write(stem + primary[i][2] + end + ':' + stem + secondary[i][j][2] + '\n')
            if secondary[i][j] not in check:
                check.append(secondary[i][j])
                
    for k in range(len(check)):
        for l in range(len(tertiary[k])):
            align.write(stem + check[k][2] + end + ':' + stem + tertiary[k][l][2] + end + ':' + master + '\n') 
            intf.write(stem + check[k][2] + end + ':' + stem + tertiary[k][l][2] + end + '\n') 
            
    align.close()       
    intf.close()

    print 'Number of pairs generated: ', len(check)  
    
#---------------------------------ALL------------------------------------------
elif algorithm == 'all':
    comb = list(set(it.combinations(data, 2)))
    
    #____________________________________plot__________________________________
    rc('xtick', labelsize=20) 
    rc('ytick', labelsize=20)
    rc('lines', linewidth=3)
    fig1 = plt.figure(figsize=(22,18))
    ax = fig1.add_subplot(111)
    ax.get_xaxis().get_major_formatter().set_useOffset(False)
    ax.set_xlabel('Year',fontsize=25)
    ax.set_ylabel('Baseline (m)',fontsize=25)
    ax.set_title('All Method', fontsize=32)
    
    labels = []
    for i in range(len(comb)):
        x=[]
        y=[]
        
        x.append(comb[i][0][0])
        x.append(comb[i][1][0])
        
        y.append(comb[i][0][1])
        y.append(comb[i][1][1])        
        
        if comb[i][0][2] not in labels:
                plt.annotate(comb[i][0][2], (x[0], y[0]),fontsize=16,
                             horizontalalignment='left',
                             verticalalignment='top')      
        labels.append(comb[i][0][2])        
        
        if comb[i][1][2] not in labels:
                plt.annotate(comb[i][1][2], (x[1], y[1]),fontsize=16,
                             horizontalalignment='left',
                             verticalalignment='top') 
        labels.append(comb[i][1][2])
        
        ax.plot(x,y, c=np.random.rand(3,1), zorder=1)
    
    ax.scatter(date,base, s=200, zorder=2)
    plt.savefig('all_alignPairs.png', dpi=300)
    
          
        
    #_________________________Making files_____________________________________
    align = open('align.in', 'w')
    intf = open('intf.in', 'w')
    for pair in comb:
        align.write(stem + pair[0][2] + end + ':' + stem + pair[1][2] + end + ':'
        + master + '\n')  
        intf.write(stem + pair[0][2] + end + ':' + stem + pair[1][2] + end + '\n')
    align.close()       
    intf.close()
    
    print 'Number of pairs generated: ', len(comb)  
    
    
    
else:
    sys.exit('makeInoutFiles Error: Please use valid Algorithm (baseline, leapfrog, all)')


