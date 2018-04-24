# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 10:46:43 2018

@author: ashwin.monpur
"""

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
risk_free_rate=6.9/(365)

ratios_mf={}

# MF Return,var,std


abs_ret_mf=((nav_last2_years[-1]-nav_last2_years[0])/nav_last2_years[0])

ret_mf=pd.to_numeric(data_nav.pct_change(1))
ret_mf_rf=ret_mf*100-risk_free_rate
ret_mf_rf.dropna(inplace=True)
mean_mf=np.mean(ret_mf_rf)
std_mf=ret_mf_rf.std()

return_mf=(((1+abs_ret_mf)**(365/730))-1)*100
ann_std=std_mf*np.sqrt(252)

ratios_mf.update({"Return":np.round(return_mf,4)})

#volatility




# Index return,var,std
ret_indx=pd.to_numeric(data_indx.pct_change(1))
ret_indx_rf=ret_indx*100-risk_free_rate
ret_indx_rf.dropna(inplace=True)
mean_indx=np.mean(ret_indx_rf)
std_indx=np.std(ret_indx_rf)

abs_ret_indx=((index_close_last2_years[-1]-index_close_last2_years[0])/index_close_last2_years[0])
return_indx=(((1+abs_ret_indx)**(365/730))-1)*100


# R square

corr=np.corrcoef(ret_indx_rf.tolist(),ret_mf_rf.tolist())
R_square=np.square(corr[0][1])

# Beta

#beta = (std_mf*R_square)/std_indx

beta = np.cov(ret_mf_rf,ret_indx_rf)[0][1]/np.var(ret_indx_rf)

#m=np.matrix([ret_mf_rf,ret_indx_rf])
#beta= (np.cov(m)[0][1])/np.std(ret_indx_rf)

# Alpha
risk_free_rate_y=6.9
#eff_risk=(((1+(risk_free_rate/2))**2)-1)
alpha =(return_mf-risk_free_rate_y)-beta*(return_indx-risk_free_rate_y)




# Active Risk
#annual=nav_last2_years.asfreq('A','ffill').mean()

active_risk=np.std(ret_mf_rf-ret_indx_rf)





# Sharpe ratio

sharp_ratio=(mean_mf*np.sqrt(253)-risk_free_rate)/(std_mf)

# Treynor ratio

treynor_r=(return_mf-risk_free_rate_y)/beta

# Information Ratio

i_r=(mean_mf*np.sqrt(252)-mean_indx*np.sqrt(252))/(ann_std*100)

# sortino Ratio

#def lpm(returns,threshold,order):
#    threshold_array=np.empty(len(returns))
#    threshold_array.fill(threshold)
#    # Calculate the difference between the threshold and the returns
#    diff = threshold_array - returns
#    # Set the minimum of each to 0
#    diff = np.clip(diff,a_min=0,a_max=None)
#    # Return the sum of the different to the power of order
#    return np.sum(diff ** order) / len(returns)

neg_ret=[]
for i in ret_mf.index:
    if ret_mf[i]<0:
        neg_ret.append(ret_mf[i])
    else:
        continue
#var_neg=np.var(neg_ret)
std_neg=np.std(neg_ret)*100*np.sqrt(252)
#
#std_n_r=np.std(neg_ret)

sortino_ratio=(return_mf-risk_free_rate_y)/std_neg

ratios_mf.update({"Alpha":np.round(alpha,4)})
ratios_mf.update({"R Square":np.round(R_square,4)})
ratios_mf.update({"Active Risk":np.round(active_risk,4)})
ratios_mf.update({"Volatility":np.round(ann_std,4)})
ratios_mf.update({"Beta":np.round(beta,4)})
ratios_mf.update({"Sharpe Ratio":np.round(sharp_ratio,4)})
ratios_mf.update({"Treynor ratio":np.round(treynor_r,4)})
ratios_mf.update({"Information Ratio":np.round(i_r,4)})
ratios_mf.update({"sortino Ratio":np.round(sortino_ratio,4)})

for key in ratios_mf:
    print("{0}:{1}".format(key,ratios_mf[key]))