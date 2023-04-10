
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy import stats

## reading data

cc = pd.read_csv("cc.csv")
cc['date'] = pd.to_datetime(cc['date'], format='%Y-%m-%d %H:%M:%S+00:00')
gw = pd.read_csv("gw.csv")
gw['date'] = pd.to_datetime(gw['date'], format='%Y-%m-%d %H:%M:%S+00:00')
gt = pd.read_csv("gt.csv")
gt['date'] = pd.to_datetime(gt['date'], format='%Y-%m-%d %H:%M:%S+00:00')
f4f = pd.read_csv("f4f.csv")
f4f['date'] = pd.to_datetime(f4f['date'], format='%Y-%m-%d %H:%M:%S+00:00')

## grouping tweets by 2-weeks intervals

tweets_gt = gt.groupby(pd.Grouper(key='date', freq='2W-MON'))['date'].size()
tweets_f4f = f4f.groupby(pd.Grouper(key='date', freq='2W-MON'))['date'].size()
tweets_cc = cc.groupby(pd.Grouper(key='date', freq='2W-MON'))['date'].size()
tweets_gw = gw.groupby(pd.Grouper(key='date', freq='2W-MON'))['date'].size()

x1 = tweets_gt.values
x2 = tweets_f4f.values
y1 = tweets_cc.values
y2 = tweets_gw.values

## fitting

def fit(x, a, b):
    return x*a+b

params = curve_fit(fit, x1, y1)
[a,b] = params[0]
print("cc <-> gt:",a,b)
coeff_1 = stats.pearsonr(x1, y1)
print(coeff_1,"\n")

params = curve_fit(fit, x2, y1[1:])
[c,d] = params[0]
print("cc <-> f4f:",c,d)
coeff_2 = stats.pearsonr(x2, y1[1:])
print(coeff_2,"\n")

params = curve_fit(fit, x1, y2)
[e,f] = params[0]
print("gw <-> gt:",e,f)
coeff_3 = stats.pearsonr(x1, y2)
print(coeff_3,"\n")

params = curve_fit(fit, x2, y2[1:])
[g,h] = params[0]
print("gw <-> f4f:",g,h)
coeff_4 = stats.pearsonr(x2, y2[1:])
print(coeff_4,"\n")

## plotting

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

pearson = 'r='+str(round(coeff_1[0], 4))
pvalue = 'P='+str(round(coeff_1[1], 4))
title = pearson+"\n"+pvalue
ax1.set_title(title, y=1.0, pad=-28, fontsize=13)
ax1.scatter(x1, y1, s=50, marker='o', facecolor='none', edgecolor='deepskyblue')
x_pred = np.arange(0, 145, 0.5)
ax1.plot(x_pred, fit(x_pred,a,b), linestyle='dashed', color='royalblue', linewidth=2)
ax1.xaxis.tick_top()
ax1.set_xlim(-8, 160) # not showing outliers
ax1.set_ylabel("Climate change", fontsize=15)
ax1.tick_params(axis='both', labelsize=12)

pearson = 'r='+str(round(coeff_2[0], 4))
pvalue = 'P='+str(round(coeff_2[1], 4))
title = pearson+"\n"+pvalue
ax2.set_title(title, y=1.0, pad=-28, fontsize=13)
ax2.scatter(x2, y1[1:], s=50, marker='o', facecolor='none', edgecolor='deepskyblue')
x_pred = np.arange(0, 120, 0.5)
ax2.plot(x_pred, fit(x_pred,c,d), linestyle='dashed', color='royalblue', linewidth=2)
ax2.xaxis.tick_top()
ax2.set_xlim(-8, 130) # not showing outliers
ax2.yaxis.tick_right()
ax2.tick_params(axis='both', labelsize=12)

pearson = 'r='+str(round(coeff_3[0], 4))
pvalue = 'P='+str(round(coeff_3[1], 4))
title = pearson+"\n"+pvalue
ax3.set_title(title, y=1.0, pad=-28, fontsize=13)
ax3.scatter(x1, y2, marker='o', facecolor='none', edgecolor='deepskyblue')
x_pred = np.arange(0, 145, 0.5)
ax3.plot(x_pred, fit(x_pred,e,f), linestyle='dashed', color='royalblue', linewidth=2)
ax3.set_xlim(-8, 150)
ax3.tick_params(axis='both', labelsize=12)
ax3.set_xlabel("Greta Thunberg", fontsize=15)
ax3.set_ylabel("Global warming", fontsize=15, labelpad=12)

pearson = 'r='+str(round(coeff_4[0], 4))
pvalue = 'P='+str(round(coeff_4[1], 4))
title = pearson+"\n"+pvalue
ax4.set_title(title, y=1.0, pad=-28, fontsize=13)
ax4.scatter(x2, y2[1:], marker='o', facecolor='none', edgecolor='deepskyblue')
x_pred = np.arange(0, 250, 0.5)
ax4.plot(x_pred, fit(x_pred,g,h), linestyle='dashed', color='royalblue', linewidth=2)
ax4.yaxis.tick_right()
ax4.tick_params(axis='both', labelsize=12)
ax4.set_xlabel("Fridays for Future", fontsize=15)

plt.subplots_adjust(wspace=0.05, hspace=0.05)
plt.savefig("correlation_graphs.pdf")