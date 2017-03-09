#! /usr/bin/env python3
'''
Niema Moshiri 2016

Plot missing links fraction vs. s/n for different simulation parameters.
'''
import sys,os
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import cycle
from math import log
from matplotlib import rcParams
from numpy import linspace
from statistics import mean,stdev
sns.set_style("ticks")
rcParams['font.family'] = 'serif'
data = {} # data[cn_model][tn_model][exp_edges][num_seeds][s_over_n]

# parse subsample missing links simulation data
for f in os.listdir('.'):
    if f[-3:] in {'.py','.PY','.pyc','.PYC'}:
        continue
    parts = f.strip().split('_')
    cn_model = parts[1]
    tn_model = parts[2]
    n = int(parts[3][1:])
    exp_edges = int(parts[4][1:])
    num_seeds = int(parts[5].split('.')[0][1:])
    s_over_n = float(parts[6])
    it = int(parts[7][2:])
    vals = [float(i) for i in open(f).read().strip().split(',')]
    if cn_model not in data:
        data[cn_model] = {}
    if tn_model not in data[cn_model]:
        data[cn_model][tn_model] = {}
    if exp_edges not in data[cn_model][tn_model]:
        data[cn_model][tn_model][exp_edges] = {}
    if num_seeds not in data[cn_model][tn_model][exp_edges]:
        data[cn_model][tn_model][exp_edges][num_seeds] = {}
    if s_over_n in data[cn_model][tn_model][exp_edges][num_seeds]:
        print("ERROR: Duplicate s/n value of " + str(s_over_n) + " encountered")
        exit(-1)
    data[cn_model][tn_model][exp_edges][num_seeds][s_over_n] = vals

# set up colors and markers
num_plots = 0
for cn_model in data:
    for tn_model in data[cn_model]:
        for exp_edges in data[cn_model][tn_model]:
            for num_seeds in data[cn_model][tn_model][exp_edges]:
                num_plots += 1
colors = plt.cm.jet(linspace(0, 1, num_plots))
markers = cycle((',', '+', '.', 'o', '*'))

# generate plots
p = 0
plt.figure()
for cn_model in data:
    for tn_model in data[cn_model]:
        for exp_edges in data[cn_model][tn_model]:
            for num_seeds in data[cn_model][tn_model][exp_edges]:
                x = []
                y = []
                yerr = []
                label = cn_model + '_' + tn_model + '_e' + str(exp_edges) + '_i' + str(num_seeds)
                color = colors[p]
                p += 1
                linestyle = '--'
                marker = next(markers)
                for s_over_n in data[cn_model][tn_model][exp_edges][num_seeds]:
                    vals = data[cn_model][tn_model][exp_edges][num_seeds][s_over_n]
                    x.append(log(s_over_n,2))
                    y.append(mean(vals))
                    yerr.append(stdev(vals))
                plt.errorbar(x, y, yerr=yerr, label=label, color=color, linestyle=linestyle, marker=marker)
plt.title(r"Missing Link Fraction vs. Log-2 Subsample Fraction $\left(\frac{s}{n}\right)$")
plt.xlabel(r"Log-2 Subsample Fraction $\left(\frac{s}{n}\right)$")
plt.ylabel("Missing Link Fraction")
plt.legend(bbox_to_anchor=(0.7, 0.23), borderaxespad=0., frameon=True, ncol=3)
plt.tight_layout()
plt.show()