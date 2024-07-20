# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 17:21:35 2023

@author: xiao208
"""
#%%
import sys
import os
wd = 'E:\\Code\\simpl5pn_temperature_modeulation' # working directory
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
from scipy.signal import argrelextrema
from datetime import date
from datetime import datetime
import scipy.io as sio
plt.rcParams['svg.fonttype'] = 'none'
from func.l5_biophys import *
import pickle

#%% temperature dependence gating
# c = nad(-75)
# c.dist = 25
# v1 = np.arange(-100,50, 0.1)
# cmap = plt.get_cmap('RdBu')

# temp = np.arange(25,35,1)
# color_idx = np.flip(np.round(256/len(temp)*(np.arange(len(temp))+1)).astype('int32'))
# plt.figure()
# for (k, d) in enumerate(temp):
#     c.qt = 2.3**((d-21)/10)
#     a = c.I1I2_a(v1)
#     b = c.I2I1_a(v1)
#     plt.plot(v1, b/(a+b), color = cmap(color_idx[k]))
# plt.show()

# plt.figure()
# for (k, d) in enumerate(temp):
#     c.qt = 2.3**((d-21)/10)
#     a = c.I1I2_a(v1)
#     b = c.I2I1_a(v1)
#     plt.plot(v1, 1/(a+b), color = cmap(color_idx[k]))
# plt.show()
#%% v-clamp temperature and distance dependence

def nad_vclamp_freq(freq, dist = 25.0, temp = np.asarray([28.0,34.0]),base_dir = os.path.join(wd,'results'), save_dir = 'temp_mod_nad', if_save = 1, if_plot = 0):
    if isinstance(freq, (list, int,float,np.float64, np.int8, np.int16, np.int32)):
        freq = np.asarray(freq)
    if isinstance(dist, (int,float,np.float64, np.int8, np.int16, np.int32)):
        dist = np.asarray(dist)
    t_all = []
    G_all = []
    attenuation = np.zeros([temp.shape[0],freq.shape[0]])
    for n, f in enumerate(freq):
        [t, G_nad] = param_fit.vclamp_nad_test(0.05, freq = f, dist = dist, temp = temp, if_plot = if_plot)
        t_all.append(t)
        G_all.append(G_nad)
        for k, G in enumerate(G_nad):
            idx_temp = argrelextrema(G, np.greater)
            idx_temp = idx_temp[0]
            idx_rmv = np.where(G[idx_temp]-G[idx_temp+1]<0.005)
            idx_temp = np.delete(idx_temp, idx_rmv)
            attenuation[k,n] = G[idx_temp[-1]]/G[idx_temp[0]]
    if if_save:
        datapath = os.path.join(base_dir, save_dir)
        today = date.today()
        now = datetime.now()
        current_date = today.strftime("%m%d%y")
        current_time = now.strftime("%H%M%S")
        if not os.path.exists(datapath):
            os.makedirs(datapath)
        data_temp = {'attnuation':attenuation, 'freq': freq, 'dist':dist, 'temp':temp}
        sio.savemat(os.path.join(datapath, 'nad_%s_%s.mat'%(current_date, current_time)), data_temp)
        results_file = os.path.join(datapath, 'nad_%s_%s_raw'%(current_date, current_time))
        pickle.dump([G_all, t_all], open(results_file, 'wb'))


freq = np.arange(5,27.5,2.5)
dist = np.asarray([25.0])
temp = np.asarray([28.0, 34.0])
nad_vclamp_freq(freq, dist = dist, temp = temp, if_save = 1, if_plot = 0)



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