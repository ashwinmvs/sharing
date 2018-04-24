# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 12:57:09 2018

@author: ashwin.monpur
"""


import pandas as pd
import math
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta
import datetime
import numpy as np

MF_Data=pd.read_csv('Book1.csv')
nav=MF_Data['Net Asset Value']

nav.index=pd.to_datetime(MF_Data['Date'])

# Get index Data from csv
index_data = pd.read_csv('nif50ty.csv')

#index_open=index_data['Open']
index_close=pd.to_numeric(index_data['Close'])
#index_avg=(index_open+index_close)/2
index_close.index=pd.to_datetime(index_data['Date'])

date_data=np.max(pd.to_datetime(MF_Data['Date']))
fdat_a=pd.to_datetime(date_data - relativedelta(months=24))

start=pd.to_datetime(datetime.datetime.strftime(fdat_a,'%Y-%m-%d'))
end=pd.to_datetime(datetime.datetime.strftime(date_data,'%Y-%m-%d'))
step=datetime.timedelta(days=1)

nav_last2_years=nav[start:end]
index_close_last2_years=index_close[start:end]


#plt.subplot(1,2,1)
#plt.plot(nav)
#plt.plot(index_close)

list_av_mf=[]
list_match_indx=[]
#list_mf_d_date=[]
#list_indx_d_date=[]
#
#
for i in pd.to_datetime(nav_last2_years.index):
    for j in pd.to_datetime(index_close_last2_years.index):
#        print(i)
#        print(j)
        list_mf=[]
        list_indx=[]
        list_mf_d=[]
        list_indx_d=[]
        if i==j:
            list_mf.append(j)
            list_mf.append(nav_last2_years[j])
            list_indx.append(i)
            list_indx.append(index_close_last2_years[i])
            
            list_av_mf.append(list_mf)
            list_match_indx.append(list_indx)
#            list_mf_d_date.append(list_mf_d)
#            list_indx_d_date.append(list_indx_d)
#            print('index: {0} {1}'.format(i,index_ret[i]))
#            print('MF   : {0} {1}'.format(j,ret_d[j]))
        else:
            continue
#
#
nav_spd_data=pd.DataFrame(list_av_mf)
indx_spd_data=pd.DataFrame(list_match_indx)

nav_spd_data.columns=['Date','NAV']
indx_spd_data.columns=['Date','Close']
nav_spd_data.index=nav_spd_data['Date']
indx_spd_data.index=indx_spd_data['Date']

data_nav=nav_spd_data['NAV']
data_indx=indx_spd_data['Close']
#
#
ratios_mf={}

# MF Return,var,std
ret_mf=pd.to_numeric(data_nav.diff(1))

ret_mf.dropna(inplace=True)
mean_mf=np.mean(ret_mf)
std_mf=ret_mf.std()


ratios_mf.update({"Return":np.round(mean_mf,4)})

# Index return,var,std
ret_indx=pd.to_numeric(data_indx.diff(1))
ret_indx.dropna(inplace=True)
mean_indx=np.mean(ret_indx)
std_indx=np.std(ret_indx)


# R square

corr=np.corrcoef(ret_indx.tolist(),ret_mf.tolist())
R_square=np.square(corr[0][1])

# Beta

beta = (std_mf*R_square)/std_indx
m=np.matrix([ret_mf,ret_indx])
#beta= np.cov(m)[0][1]/np.std(ret_indx)

# Alpha
risk_free_rate=0.069
eff_risk=(((1+(risk_free_rate/2))**2)-1)
alpha = (mean_mf-risk_free_rate)-beta*(mean_indx-risk_free_rate)

# Active Risk

active_risk=np.std(ret_mf-ret_indx)
#active_risk=np.sqrt(active_ret)



# Sharpe ratio

sharp_ratio=(mean_mf-risk_free_rate)/std_mf

# Treynor ratio

treynor_r=(mean_mf-risk_free_rate)/beta

# Information Ratio

i_r=(mean_mf-mean_indx)/active_risk

# sortino Ratio

def lpm(returns,threshold,order):
    threshold_array=np.empty(len(returns))
    threshold_array.fill(threshold)
    # Calculate the difference between the threshold and the returns
    diff = threshold_array - returns
    # Set the minimum of each to 0
    diff = np.clip(diff,a_min=0,a_max=None)
    # Return the sum of the different to the power of order
    return np.sum(diff ** order) / len(returns)

#neg_ret=[]
#for i in ret_mf.index:
#    if ret_mf[i]<risk_free_rate:
#        neg_ret.append(ret_mf[i])
#    else:
#        continue
#
#std_n_r=np.std(neg_ret)

sortino_ratio=(mean_mf-risk_free_rate)/math.sqrt(lpm(ret_mf,0,2))

ratios_mf.update({"Alpha":np.round(alpha,4)})
ratios_mf.update({"R Square":np.round(R_square,4)})
ratios_mf.update({"Active Risk":np.round(active_risk,4)})
ratios_mf.update({"Volatility":np.round(std_mf,4)})
ratios_mf.update({"Beta":np.round(beta,4)})
ratios_mf.update({"Sharpe Ratio":np.round(sharp_ratio,4)})
ratios_mf.update({"Treynor ratio":np.round(treynor_r,4)})
ratios_mf.update({"Information Ratio":np.round(i_r,4)})
ratios_mf.update({"sortino Ratio":np.round(sortino_ratio,4)})

for key in ratios_mf:
    print("{0}:{1}".format(key,ratios_mf[key]))