# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 21:51:41 2015

@author: SW274998
"""
from nsepy.commons import *
import ast
import json
from bs4 import BeautifulSoup
from nsepy.liveurls import quote_eq_url, quote_derivative_url, option_chain_url


eq_quote_referer = "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={}&illiquid=0&smeFlag=0&itpFlag=0"
derivative_quote_referer = "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuoteFO.jsp?underlying={}&instrument={}&expiry={}&type={}&strike={}"
months={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}


def get_quote(symbol, series='EQ', instrument=None, expiry=None, option_type=None, strike=None):
    """
    1. Underlying security (stock symbol or index name)
    2. instrument (FUTSTK, OPTSTK, FUTIDX, OPTIDX)
    3. expiry (ddMMMyyyy)
    4. type (CE/PE for options, - for futures
    5. strike (strike price upto two decimal places
    """

    if instrument:
        expiry_str = "%02d%s%d"%(expiry.day, months[expiry.month][0:3].upper(), expiry.year)
        quote_derivative_url.session.headers.update({'Referer': eq_quote_referer.format(symbol)})
        
        res = quote_derivative_url(symbol, instrument, expiry_str, option_type, "{:0.2f}".format(strike))
        soup = BeautifulSoup(res.text, 'html5lib')
        table = soup.find('div', attrs={'id': 'responseDiv'})
        mj = re.search('.*data\":\[\{(.*)\}\]', table.get_text()).group(1).split(',')
        d = {}
        for elem in mj:
            k = elem.split(':')
            if len(k) == 2:
                d[k[0].strip('"')] = k[1].strip('"')
        return d
    else:
        quote_eq_url.session.headers.update({'Referer': eq_quote_referer.format(symbol)})
        res = quote_eq_url(symbol, series)
        #print res.content
        soup = BeautifulSoup(res.content, 'html5lib')
        table = soup.find('div', attrs={'id': 'responseDiv'})
        mj = re.search('.*data\":\[\{(.*)\}\]', table.get_text()).group(1).split(',')
        d = {}
        for elem in mj:
            k = elem.split(':')
            if len(k) == 2:
                d[k[0].strip('"')] = k[1].strip('"')
        return d

    '''
    d =  json.loads(res.text)['data'][0]
    res = {}
    for k in d.keys():
        v = d[k]
        try:
            v_ = None
            if v.find('.') > 0:
                v_ = float(v.strip().replace(',', ''))
            else:
                v_ = int(v.strip().replace(',', ''))
        except:
            v_ = v
        res[k] = v_
    '''

