# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 17:21:35 2023

@author: xiao208
"""
#%%
import sys
import os
wd = 'E:\\Code\\simplified_l5pn' # working directory
sys.path.insert(1, wd)

import numpy as np
import pickle
import sys
import time
import os
from func import comp_model
from func import parameters_two_com
from func import parameters_three_com
from func import sequences
from func import param_fit
from func import post_analysis
P = parameters_three_com.init_params(wd)
import matplotlib.pyplot as plt
from scipy.stats import norm
from numpy.random import RandomState
plt.rcParams['svg.fonttype'] = 'none'
from func.l5_biophys import *

#%% temperature dependence gating
c = nad(-75)
c.dist = 25
v1 = np.arange(-100,50, 0.1)
cmap = plt.get_cmap('RdBu')

temp = np.arange(25,35,1)
color_idx = np.flip(np.round(256/len(temp)*(np.arange(len(temp))+1)).astype('int32'))
plt.figure()
for (k, d) in enumerate(temp):
    c.qt = 2.3**((d-21)/10)
    a = c.I1I2_a(v1)
    b = c.I2I1_a(v1)
    plt.plot(v1, b/(a+b), color = cmap(color_idx[k]))
plt.show()

plt.figure()
for (k, d) in enumerate(temp):
    c.qt = 2.3**((d-21)/10)
    a = c.I1I2_a(v1)
    b = c.I2I1_a(v1)
    plt.plot(v1, 1/(a+b), color = cmap(color_idx[k]))
plt.show()
#%% v-clamp temperature and distance dependence
freq = 5
# dist = np.asarray([10.0,20.0,30.0])
dist = np.asarray([25.0])
temp = np.asarray([28.0, 34.0])
param_fit.vclamp_nad_test(0.05, freq = freq, dist = dist, temp = temp)


#%% Nav1.6 gating dynamic

# from func.l5_biophys import *

# c = nad(-75)
# c.dist = 300
# v1 = np.arange(-100,50, 0.1)
# plt.figure()
# ax = plt.gca()
# ax.plot(v1, c.I1I2_a(v1), color = colors[1], linewidth = 1)
# ax2 = ax.twinx()
# ax2.plot(v1, c.I2I1_a(v1), color = colors[0], linewidth = 1)
# ax.set_ylabel("I1-I2",color=colors[1])
# ax2.set_ylabel("I2-I1",color=colors[0])

# plt.figure()
# ax = plt.gca()
# ax.plot(v1, c.I1C1_a(v1), color = colors[1], linewidth = 1)
# ax2 = ax.twinx()
# ax2.plot(v1, c.C1I1_a(v1), color = colors[2], linewidth = 1)
# ax.set_ylabel("I1-C1",color=colors[1])
# ax2.set_ylabel("C1-I1",color=colors[2])

# plt.figure()
# ax = plt.gca()
# ax.plot(v1, c.I1O1_a(v1), color = colors[1], linewidth = 1)
# ax2 = ax.twinx()
# ax2.plot(v1, c.O1I1_a(v1), color = colors[3], linewidth = 1)
# ax.set_ylabel("I1-O1",color=colors[1])
# ax2.set_ylabel("O1-I1",color=colors[3])

# plt.figure()
# ax = plt.gca()
# ax.plot(v1, c.C1O1_a(v1), color = colors[2], linewidth = 1)
# ax2 = ax.twinx()
# ax2.plot(v1, c.O1C1_a(v1), color = colors[3], linewidth = 1)
# ax.set_ylabel("C1-O1",color=colors[2])
# ax2.set_ylabel("O1-C1",color=colors[3])