# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:50:20 2023

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
from func import parameters_temp_mod
from func import sequences
from func import post_analysis
P = parameters_temp_mod.init_params(wd)
import matplotlib.pyplot as plt
plt.rcParams['svg.fonttype'] = 'none'
from func.l5_biophys import *
from func.param_fit import *
from scipy.stats import norm
from numpy.random import RandomState

def spon_spiking_temp_mod(P, dt, T, temp = np.asarray([34.0,34.0,34.0,34.0]), if_plot = 1, if_save = 1, base_dir = os.path.join(wd,'results'), save_dir = 'temp_mod'):
    P['temp'] = temp
    cell = comp_model.CModel(P, verbool = False)
    mu = 0.5
    mu_i = 1
    sigma = 2

    v_init = -70.0

    rates_e, temp = sequences.lognormal_rates(1, P['N_e'], P['N_i'], mu, sigma)
    temp, rates_i = sequences.lognormal_rates(1, P['N_e'], P['N_i'], mu_i, 3)

    rates_e = [np.zeros(P['N_e'])]
    rates_i =[ np.zeros(P['N_i'])]
    S_e = sequences.build_rate_seq(rates_e[0], 0, T)
    S_i = sequences.build_rate_seq(rates_i[0], 0, T)

    t, soln, stim = cell.simulate(0, T, dt, v_init, S_e, S_i, I_inj=[-0.02], inj_site = [0])
    v = soln[0]
    t_spike = spike_times(dt, v)
    t_dspike = d_spike_times(dt,v, t_spike)

    if if_plot:
        colors = np.asarray([[128,128,128],[61,139,191], [119,177,204], [6,50,99]])
        colors = colors/256
        plt.figure()
        ax = plt.subplot(211)
        for i in [0,2,3]:
            ax.plot(t, soln[0][i], color = colors[i], linewidth=0.75)
        ax.scatter(t_spike, v[0, np.floor(t_spike/dt).astype(np.int32)])
        ax.scatter(t_dspike.T[0], v[2, np.floor(t_dspike.T[0]/dt).astype(np.int32)])
        ax.scatter(t_dspike.T[1], v[3, np.floor(t_dspike.T[1]/dt).astype(np.int32)])
        ax.set_xlim([0,500])
        comp = 2
        ax = plt.subplot(212)
        for i in [0,2,3]:
            ax.plot(t, soln[1][7+i,comp,:].T, color = colors[i,:])
        ax.set_xlim([0,500])
        ax.set_ylim([0,1])
        plt.show()
    
    if if_save:
        datapath = os.path.join(base_dir, save_dir)
        today = date.today()
        now = datetime.now()
        current_date = today.strftime("%m%d%y")
        current_time = now.strftime("%H%M%S")
        if not os.path.exists(datapath):
            os.makedirs(datapath)
        spike_num = len(t_spike)
        isi = np.diff(t_spike)
        edges = np.arange(0,3,0.1)
        isi_hist = np.histogram(isi/(T/spike_num), edges)
        burstiness = np.sum(isi_hist[0][:5])/len(isi)
        data_temp = {'v':v, 'P': cell.P,'gates':soln[1], 'T': T, 'dt': dt, 'burstiness': burstiness}
        sio.savemat(os.path.join(datapath, 'temp%d_%s_%s.mat'%(cell.P["temp"][-1],current_date, current_time)), data_temp)

def spon_spiking_temp_mod_paramjitter(P, dt, T, temp = np.asarray([34.0,34.0,34.0,34.0]), if_plot = 1, if_save = 1, base_dir = os.path.join(wd,'results'), save_dir = 'temp_mod'):
    rand_norm = norm
    rand_norm.random_state=RandomState(seed=None)
    Zm = rand_norm.rvs(0,1, size = 4)
    P['dist'][2:] = P['dist'][2:] + 0.05*P['dist'][2:]*Zm[:2] # jitter distance between the proximal/distal apical dendrite to soma by +/- 5% (SD)
    # P['dist'][2:] = P['dist'][2:]+1
    # if P['dist'][2]< 24:
    #     P['dist'][2] = 24
    # if P['dist'][2]> 33:
    #     P['dist'][2] = 33
    P['rho_d'] = P['rho_d'] + P['rho_d']*0.05*Zm[2]
    P['rho_p'] = P['rho_p'] + P['rho_p']*0.05*Zm[3]
    for t in temp:
        P['temp'][2] = t
        P['temp'][3] = t

        cell = comp_model.CModel(P, verbool = False)
        mu = 0.5
        mu_i = 1
        sigma = 2

        v_init = -70.0

        rates_e, temp = sequences.lognormal_rates(1, P['N_e'], P['N_i'], mu, sigma)
        temp, rates_i = sequences.lognormal_rates(1, P['N_e'], P['N_i'], mu_i, 3)

        rates_e = [np.zeros(P['N_e'])]
        rates_i =[ np.zeros(P['N_i'])]
        S_e = sequences.build_rate_seq(rates_e[0], 0, T)
        S_i = sequences.build_rate_seq(rates_i[0], 0, T)

        t, soln, stim = cell.simulate(0, T, dt, v_init, S_e, S_i, I_inj=[-0.02], inj_site = [0])
        v = soln[0]
        t_spike = spike_times(dt, v)
        t_dspike = d_spike_times(dt,v, t_spike)

        if if_plot:
            colors = np.asarray([[128,128,128],[61,139,191], [119,177,204], [6,50,99]])
            colors = colors/256
            plt.figure()
            ax = plt.subplot(211)
            for i in [0,2,3]:
                ax.plot(t, soln[0][i], color = colors[i], linewidth=0.75)
            ax.scatter(t_spike, v[0, np.floor(t_spike/dt).astype(np.int32)])
            ax.scatter(t_dspike.T[0], v[2, np.floor(t_dspike.T[0]/dt).astype(np.int32)])
            ax.scatter(t_dspike.T[1], v[3, np.floor(t_dspike.T[1]/dt).astype(np.int32)])
            ax.set_xlim([0,500])
            comp = 2
            ax = plt.subplot(212)
            for i in [0,2,3]:
                ax.plot(t, soln[1][7+i,comp,:].T, color = colors[i,:])
            ax.set_xlim([0,500])
            ax.set_ylim([0,1])
            plt.show()
        
        if if_save:
            datapath = os.path.join(base_dir, save_dir)
            today = date.today()
            now = datetime.now()
            current_date = today.strftime("%m%d%y")
            current_time = now.strftime("%H%M%S")
            if not os.path.exists(datapath):
                os.makedirs(datapath)
            spike_num = len(t_spike)
            isi = np.diff(t_spike)
            edges = np.arange(0,3,0.1)
            isi_hist = np.histogram(isi/(T/spike_num), edges)
            burstiness = np.sum(isi_hist[0][:5])/len(isi)
            data_temp = {'v':v, 'P': cell.P,'gates':soln[1], 'T': T, 'dt': dt, 'burstiness': burstiness, 't_spike':t_spike}
            sio.savemat(os.path.join(datapath, 'temp%d_%s_%s.mat'%(cell.P["temp"][-1],current_date, current_time)), data_temp)

dt = 0.05
T = 5000
for i in range(20):
    temp = np.asarray([34.0,28.0])
    spon_spiking_temp_mod_paramjitter(P, dt, T, temp, if_plot = 0)



