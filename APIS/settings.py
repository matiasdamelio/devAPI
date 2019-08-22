# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 11:10:03 2019

@author: mdamelio
"""

import time
import pandas as pd
import itertools

def search_account(name):
    for l in cuentas:
        if l['user'] == name:
            try:
                return int(l['account'])
            except:
                return l['account']
def search_entorno(name):
    for l in cuentas:
        if l['user'] == name:
            return l['entorno']
def search_codigo(name):
    for l in cuentas:
        if l['user'] == name:            
            return l['codigo']
        
def search_lamina(ticker):
    return [x[1] for x in laminas if x[0] == ticker][0]
            

def search_index(name):
    try:
        for l in index_tickers:
            if name in l:
                return l[0]
    except:
        return -1


def init():
    
    global account, entorno, cuentas

    global dict_tickers, index_tickers

    index_tickers = []
    dict_tickers = {}    

      
    global currentDate 
    currentDate = time.strftime("%Y-%m-%d",time.localtime())
    
    df = pd.read_csv('Data/cuentas.txt', usecols=['user', 'account', 'entorno', 'codigo'])
    cuentas = df.to_dict(orient='records')