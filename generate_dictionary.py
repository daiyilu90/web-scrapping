# -*- coding: utf-8 -*-
"""
Created on Tue May 19 16:23:53 2020

@author: Yilu Dai
"""
import os
import pandas as pd
import numpy as np

#combine all sentiment files into one
sentiment=pd.DataFrame()
xls = pd.ExcelFile('sentimen_out/google/ouput.xlsx')
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
#bank_counter = 0


for bank_name in bank_list:
    bank_sentiment_df=pd.read_excel(xls, bank_name+'bank_sentiment')
    sentiment=sentiment.append(bank_sentiment_df, ignore_index=True)

#Step one: check words counts to create dictionary 
#sort by most frequent words
sentiment=sentiment.groupby(['ngram','set_name'],as_index=False).sum()
sentiment=sentiment[['ngram', 'count', 'set_name']].sort_values(by=['count'],ascending=False)
sentiment['ngram']=sentiment['ngram'].astype(str) 
sentiment.to_excel('sentimen_out/google/ngram_counts.xlsx')
sentiment_df=sentiment.copy()

#define journeys
#Shopping	Consider and research for options
#Onboarding	Establish service terms and service levels
#Onboarding	Open a new account
#Onboarding	Plan for investment
#Transacting	Transfer in asset
#Transacting	Manage portfolio
#Transacting	Transfer out asset
#Administrating	Check performance
#Administrating	Manage my account
#Receive service	Receive service
#Receive service	Resolve an issue
#Referring	Refer product to a friend

#Onboarding	Open a new account
open_account=sentiment_df.ngram.apply(lambda x: 'register account' in x or 'application' in x or 'open account' in x)
sentiment_df.loc[open_account,'journey']='open a new account'

#Onboarding	access account
access_account=sentiment_df.ngram.apply(lambda x: 'log' in x or 'access account' in x \
                                        or 'password' in x or 'pin' in x or 'biometric' in x\
                                        or 'signon' in x or 'signin' in x or 'fingerprint' in x)
sentiment_df.loc[access_account,'journey']='access account'

# Onboarding	Plan for investment (education)
plan=sentiment_df.ngram.apply(lambda x: 'educat' in x or 'infom' in x \
                                        or 'feature' in x or 'plan' in x or 'goal' in x\
                                        or 'plan' in x or 'search' in x or 'research' in x)
sentiment_df.loc[plan,'journey']='plan for investment'

# Advisor service
advisor_service=sentiment_df.ngram.apply(lambda x: 'advisor' in x)
sentiment_df.loc[advisor_service,'journey']='advisor service'



#Transacting	Transfer asset
transfer=sentiment_df.ngram.apply(lambda x: 'transfer' in x  or 'wire' in x or 'move' in x)
sentiment_df.loc[transfer,'journey']='transfer'

#Transacting	 Manage portfolio and trade
manage_profolio=sentiment_df.ngram.apply(lambda x:  'portfolio' in x\
                                         or 'trad' in x or 'sell' in x or 'buy' in x) 
sentiment_df.loc[manage_profolio,'journey']='manage portfolio'     


#Administrating	Check performance
check_performance=sentiment_df.ngram.apply(lambda x: 'track' in x  or 'monit' in x or 'check' in x 
                                         or 'notifi' in x or 'alert' in x or 'chart' in x or 'graph' in x \
                                         or 'preformance' in x) 
sentiment_df.loc[check_performance,'journey']='check_performance'   

#Administrating	Manage my account
manage_account=sentiment_df.ngram.apply(lambda x: 'manage account' in x  or 'balance' in x or  'deposit' in x 
                                         or 'bill' in x or 'pay' in x  or 'profile' in x  or 'withdraw' in x   ) 
sentiment_df.loc[manage_account,'journey']='manage_account'   


#Receive service Receive service
receive_service=sentiment_df.ngram.apply(lambda x: 'customer service' in x or 'agent' in x 
                                        or 'phone call' in x ) 

sentiment_df.loc[receive_service,'journey']='receive service'  

#Receive service	Resolve an issue
issue=sentiment_df.ngram.apply(lambda x: 'crash' in x  or 'error' in x  or 'broke' in x \
                               or 'issue' in x or 'problem' in x or 'resolve' in x\
                               or 'fix' in x or 'fail' in x or 'solve' in x)
sentiment_df.loc[issue,'journey']='resolve an issue' 

#Referring	Refer product to a friend
refer=sentiment_df.ngram.apply(lambda x: 'refer' in x  or 'recommend' in x)
sentiment_df.loc[refer,'journey']='refer to a friend' 

#############define theme
#speed
speed=sentiment_df.ngram.apply(lambda x: 'speed' in x or  'time' in x or 'quick' in x or 'fast' in x \
                               or 'slow' in x or 'delay' in x  or 'wait' in x  or 'long' in x or 'lag' in x or 'realtime' in x)
sentiment_df.loc[speed,'theme']='speed'

#simplicity and ease of use
ui=sentiment_df.ngram.apply(lambda x: 'eas' in x or 'diffi' in x or 'convenien' in x or 'design' \
                            in x or 'user friendly' in x   or 'interf' in x  or 'hard' in x \
                            in x or 'outdate' in x  or 'update' in x  or 'clunky' in x or 'simpl' in x\
                            or 'new' in x or 'old' in x or 'user friendly' in x or 'clean' in x)
sentiment_df.loc[ui,'theme']='ui/ux'

#fee
fee=sentiment_df.ngram.apply(lambda x: 'fee' in x  or 'charge' in x   or 'commision' in x or 'free' in x)
sentiment_df.loc[fee,'theme']='charge-free' 

# error-proof 
issue=sentiment_df.ngram.apply(lambda x: 'crash' in x  or 'error' in x  or 'broke' in x \
                               or 'issue' in x or 'problem' in x or 'resolve' in x\
                               or 'fix' in x or 'work' in x or 'fail' in x)
sentiment_df.loc[issue,'theme']='error-proof' 

#informed
useful=sentiment_df.ngram.apply(lambda x: 'useful' in x  or 'helpful' in x  or 'inform' in x \
                               or 'educat' in x or 'advisor' in x or 'guid' in x or 'research' in x
                               or 'help' in x)
sentiment_df.loc[useful,'theme']='informed' 

# track and compare 
track=sentiment_df.ngram.apply(lambda x: 'track' in x  or 'monit' in x\
                                or 'chart' in x or 'graph' in x )
sentiment_df.loc[track,'theme']='trackable' 

#watch out
notify=sentiment_df.ngram.apply(lambda x: 'notif' in x or 'alert' in x  or 'remind' in x or 'watch' in x  )
sentiment_df.loc[notify,'theme']='watch out'

#personalizatoin
personalizatoin=sentiment_df.ngram.apply(lambda x: 'customized' in x or 'personal' in x)
sentiment_df.loc[personalizatoin,'theme']='personalizatoin'



#output the dictionay
sentiment_df=sentiment_df[['ngram', 'set_name', 'journey', 'theme']]
sentiment_df.loc[sentiment_df.theme.notna()].to_csv('sentimen_out/google/ngram_theme_dictionary_file.csv')
#update the 
sentiment_dic_gap=sentiment.merge(sentiment_df, on='ngram', how='left')
sentiment_dic_gap.to_csv('sentimen_out/google/dictionary_gap.csv')

#check how many are filled
sentiment_df.sort_value()
sentiment_df.theme.value_counts()/sentiment_df.shape[0]