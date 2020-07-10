# -*- coding: utf-8 -*-
"""
Created on Thu May 21 21:44:53 2020

@author: Yilu Dai
"""
import os
import pandas as pd
import numpy as np

#combine all sentiment files into one
google = pd.ExcelFile('result_out/google/theme_google.xlsx')
apple = pd.ExcelFile('result_out/apple/theme_apple.xlsx')

metrics='theme'  
bank_list = [
            'ms',
            'etrade',
            'fidelity',
            'schwab',
            'pc',
            'marcus',
            'mymerrill',
            'merrilledge',
            'boa',
            'UBS',
            'power_etrade',
            'robinhood',
            'td'
            ]
journey_order = pd.DataFrame({'journey':['open a new account','access account','plan for investment',
                 'transfer','manage portfolio','check_performance','manage_account',
                 'receive service','resolve an issue','refer to a friend']})
    
theme_order = pd.DataFrame({'theme':['ui/ux','error-proof','charge-free',
                 'informed','trackable','watch out','personalization',
                 'speed']})

if (metrics=='journey'):
    order=journey_order
else:
    order=theme_order

with pd.ExcelWriter('result_out/theme_merged.xlsx', engine='xlsxwriter') as writer:
    for bank_name in bank_list:
        ############################### Load data ###############################
        google_df = pd.read_excel(open(google, 'rb'), sheet_name=bank_name) 
        apple_df = pd.read_excel(open(apple, 'rb'), sheet_name=bank_name) 
        df_merged = pd.concat([google_df,apple_df])
        df_merged =df_merged[[metrics,'count','negative_count','neutral_count','positive_count']]
        df_merged=df_merged.groupby([metrics],as_index=False).sum()
        
        df_merged=order.merge(df_merged, on=metrics,how='left')
        df_merged['count_squareroot'] = df_merged['count']**0.5
    
        # Calculate percentage negative and positive
        df_merged['negative_percentage'] = round(df_merged['negative_count']/df_merged['count'], 2)
        df_merged['positive_percentage'] = round(df_merged['positive_count']/df_merged['count'], 2)
        df_merged.to_excel(writer, sheet_name=bank_name)
