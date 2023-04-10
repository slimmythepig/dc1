
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from scipy.optimize import curve_fit
from scipy import stats

## reading from file

df_cc = pd.read_csv("2013-2021.csv")
df_twitter_users = pd.read_csv("tw_users.csv") ## users numbers are in milions

## converting to datetime

df_cc['date'] = pd.to_datetime(df_cc['date'], format='%Y-%m-%d %H:%M:%S+00:00')

## grouping number of tweets by quarter since 2013 to 2021

quarters = [g for n, g in df_cc.groupby(pd.Grouper(key='date',freq='3M', closed='left'))] ## list of dataframes
dates = []
n_tweets = []
for i in quarters:
    middle = int(len(i)/2)
    j = i.index[middle]
    n_tweets.append(len(i.index))
    dates.append(df_cc.iloc[j, 0])

## considering time as number of quarters since beginning and normalizing based on users

df_twitter_users['date'] = dates
df_twitter_users['tweets'] = n_tweets
df_twitter_users['normalized tweets'] = df_twitter_users['tweets'] / df_twitter_users['users'] 
df_twitter_users['# quarters'] = df_twitter_users.index + 1 

## arrays for fitting and plotting

q = np.asarray(df_twitter_users['# quarters'])
q2 = q[:21]
q3 = q[20:]
tweets = np.asarray(df_twitter_users['normalized tweets'])
tweets2 = tweets[:21]
tweets3 = tweets[20:]
users = np.asarray(df_twitter_users['users'])

## fitting

def fit(x, a, b):
    return a*x+b 
params = curve_fit(fit, q2, tweets2)
[a,b] = params[0]
print("PARAMETERS:")
print("a =",a,"// b =",b)

## testing goodness of fit

print("TESTS:")
chi2 = stats.chisquare(tweets2, fit(q2, a, b))
ks = stats.kstest(tweets2, fit(q2, a, b))
print("chi-test for fitted data:",chi2)
print("ks-test for fitted data:",ks)

## ks-test for extrapolation

ks_test = stats.kstest(tweets3, fit(q3, a, b))
print("ks-test for extrapolated trend:",ks_test)

## plotting 

xticks = df_twitter_users.iloc[::2, 5] 
xtickslabels = df_twitter_users.iloc[::2, 0]

### 1st plot

plt.figure(num=1)
plt.xticks(xticks, labels=xtickslabels, rotation=60, fontsize=13)
plt.yticks(fontsize=13)
plt.xlabel("time", fontsize=15)
plt.ylabel("tweets (normalized)", fontsize=15)
plt.scatter(q2, tweets2, color='deepskyblue', label="tweets", s=50)
plt.plot(q2, fit(q2, a, b), color='mediumblue', linestyle='solid', label="linear fit")
plt.legend(fontsize=15)
plt.savefig("fitting.pdf", bbox_inches = "tight")

### 2nd plot

plt.figure(num=2)
plt.xticks(xticks, labels=xtickslabels, rotation=60, fontsize=13)
plt.yticks(fontsize=13)
plt.xlabel("time", fontsize=15)
plt.ylabel("tweets (normalized)", fontsize=15)
plt.bar(q, tweets, color='deepskyblue', width=1.3, label="tweets")
plt.plot(q2, fit(q2, a, b), color='mediumblue', linestyle='solid', label="Q1'13-Q2'18 trend")
plt.plot(q3, fit(q3, a, b), color='mediumblue', linestyle='dashed', label="trend extrapolation")
plt.ylim(0,15)
plt.legend(fontsize=13, loc='upper left')

greta_thunberg = 23 # 8/20/2018
first_global_strike = 25 # 3/15/2019
second_global_strike = 26 # 5/24/2019
third_global_strike = 27 # 9/20-27/2019
first_strike_after_covid = 35 # 9/24/2021
ls = 'dotted'
lw = 1
c = 'black'
plt.axvline(x=greta_thunberg, ymax=0.55, linestyle=ls, linewidth=lw, color=c)
plt.axvline(x=first_global_strike, ymax=0.8, linestyle=ls, linewidth=lw, color=c)
plt.axvline(x=second_global_strike, ymax=0.875, linestyle=ls, linewidth=lw, color=c)
plt.axvline(x=third_global_strike, ymax=0.95, linestyle=ls, linewidth=lw, color=c)
plt.axvline(x=first_strike_after_covid, ymax=0.7, linestyle=ls, linewidth=lw, color=c)

plt.savefig("question1_plot.pdf", bbox_inches = "tight")

