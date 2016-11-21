# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 21:31:19 2016

@author: user
"""

import matplotlib.pyplot as plt
import netCDF4 as nc
import os

path = os.getcwd()

data = open('disp_001.xyz')

#print data.variables.keys()
#topo = data.variables['z']
#
#plt.figure(figsize=(10,10))
#plt.imshow(topo,origin='lower') 
#plt.title(data.title)
#plt.savefig('image.png', bbox_inches=0)