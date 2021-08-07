import scipy.integrate as integrate
from sympy import symbols, solve
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def extract_e(df):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    data = df[df.iloc[:,3] == 22] #photons
    data = data.iloc[:,4] #energies
    return data

def extract_e0(df):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    df = df.drop_duplicates(subset=[11], keep="first") #remove duplicates
    data = df[df.iloc[:,12] == 22] # photons
    data = data.iloc[:,13] # E0
    return data


def spectrum(data, nbins=10000, include_normal=False):
    bins = np.linspace(0.95*min(data),1.05*max(data),nbins)

    if include_normal:
        # plot one: normal
        plt.subplot(121)
        plt.hist(data, bins)
        plt.xlabel('Energy')
        plt.ylabel('# particles')

        # plot two: double log
        plt.subplot(122)

    counts, bins, bars = plt.hist(data, bins)
    plt.cla()
    plt.loglog(bins[0:len(bins)-1],counts)
    plt.xlabel('Energy')
    plt.ylabel('# particles')
    plt.show()
    

def corr_length(lmin, lmax, nB=-5/3):
    # calculate range of k
    kmin = 2 * math.pi / lmax
    kmax = 2 * math.pi / lmin

    # calculate average vertex size
    temp = integrate.quad(lambda k: k**(nB-1), kmin, kmax)
    num = temp[1] - temp[0]
    temp = integrate.quad(lambda k: k**(nB), kmin, kmax)
    denom = temp[1] - temp[0]

    return 2 * math.pi * num / denom


def find_lmax(lc, lmin, nB=-5/3):
    kmax = 2 * math.pi / lmin
    m = lc / (2*math.pi) * (nB/(nB+1))
    kmin = symbols('kmin')
    expr = (kmax**nB - kmin**nB) / (kmax**(nB+1) - kmin**(nB+1)) - m
    kmin = solve(expr)[0]
    lmax = 2 * math.pi / kmin
    return lmax


# make plots with the theta/delta angles taken as parameter
# plot_average: plot average angle binned by the particles' energies
# plot_hist: plot histogram of angles
def plot_angles(df, angles, plot_binned=True, plot_hist=True):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    if plot_binned:
        df['angles'] = angles
        e = extract_e(df)
        bins = np.geomspace(np.min(e), np.max(e), 100)
        data_cut = pd.cut(e, bins) #group by e bins
        grouped = df.groupby(by = data_cut)
        ret = grouped.aggregate(np.mean)

        fig = plt.figure()
        ax = plt.gca()
        ax.scatter(bins[0:len(bins)-1], ret['angles'], edgecolors='none', s=20)
        ax.set_yscale('log')
        ax.set_xscale('log')
        plt.title('Angles Binned by E')
        plt.xlabel('Energy')
        plt.ylabel('Average Angle')
        plt.show()

    if plot_hist:
        plt.hist(angles, bins=np.linspace(0,np.max(angles)*0.2,500))
        plt.xlabel('Angle')
        plt.ylabel('# Particles')
        plt.show()


# returns angles in degrees
def extension_angles(df, print_average=True):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    p = np.array([df.iloc[:,8], df.iloc[:,9], df.iloc[:,10]]) # angle of arrival vector, shape (n,3)
    d = np.array([df.iloc[:,5]-df.iloc[:,14], df.iloc[:,6]-df.iloc[:,15], df.iloc[:,7]-df.iloc[:,16]]) # displacement: x-x0, y-y0, etc; shape (n,3)

    #calculate extension angles
    p_abs = np.linalg.norm(p,axis=0)
    d_abs = np.linalg.norm(d,axis=0)
    dot = np.sum(p*d, axis=0)
    temp = dot/p_abs/d_abs
    temp = np.clip(temp, -1, 1)
    theta = np.arccos(temp)*180/math.pi

    if print_average:
        print('\nThe average extension angle is', np.sum(theta)/len(theta), 'degrees')

    return theta


# returns angles in degrees
def deflection_angles(df, print_average=True):
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)

    p = np.array([df.iloc[:,8], df.iloc[:,9], df.iloc[:,10]]) # angle of arrival vector, shape (n,3)
    p0 = np.array([df.iloc[:,17], df.iloc[:,18], df.iloc[:,19]]) # angle of departure vector, shape (n,3)

    p_abs = np.linalg.norm(p,axis=0)
    p0_abs = np.linalg.norm(p0,axis=0)
    dot = np.sum(p*p0, axis=0)
    temp = dot/p_abs/p0_abs
    temp = np.clip(temp, -1, 1)
    delta = np.arccos(temp)*180/math.pi

    if print_average:
        print('\nThe average deflection angle is', np.sum(delta)/len(delta), 'degrees')

    return delta
