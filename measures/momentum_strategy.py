# -*- coding: utf-8 -*-
"""algotrading-2(quantitative momentum strategy).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dUVFw_NtIiJMblQgW6g8TXxeHB2eS33N
"""

import numpy as np
import pandas as pd
import requests
import math
from measures.secrets import IEX_CLOUD_API_TOKEN
from utils import chunks
from scipy.stats import percentileofscore as score

stocks = pd.read_csv('../AlgoTrading/sp_500_stocks.csv')

symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0,len(symbol_groups)):
  symbol_strings.append(','.join(symbol_groups[i]))
#
# my_columns = ['Ticker', 'Stock Price', 'One Year Price Return', 'Num Shares to Buy']
#
# final_dataframe = pd.DataFrame(columns = my_columns)
#
# for symbol_string in symbol_strings:
#   batch_api_call_url = f"https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=price,stats&token={IEX_CLOUD_API_TOKEN}"
#   data = requests.get(batch_api_call_url).json()
#   for symbol in symbol_string.split(','):
#     final_dataframe = final_dataframe.append(
#         pd.Series([
#                  symbol,
#                  data[symbol]['price'],
#                  data[symbol]['stats']['year1ChangePercent'],
#                  'N/A'
#         ], index=my_columns),
#         ignore_index = True
#     )
#
# final_dataframe
#
# final_dataframe.sort_values('One Year Price Return', ascending=False, inplace=True)
# final_dataframe = final_dataframe[:50]
# final_dataframe.reset_index(inplace=True)
#
# #calculating the number of shares to buy
# portfolio_input()
#
# position_size = float(portfolio_size)/len(final_dataframe.index)
# for i in range(0, len(final_dataframe)):
#   final_dataframe.loc[i, 'Num Shares to Buy'] = math.floor(position_size/final_dataframe.loc[i, 'Stock Price'])
#
# final_dataframe

#Lets utilize high quality momentum
def hq_momentum_data():
    hqm_columns = [
                   'Ticker',
                   'Price',
                   'Number of Shares to Buy',
                   'One-Year Price Return',
                   'One-Year Return Percentile',
                   'Six-Month Price Return',
                   'Six-Month Return Percentile',
                   'Three-Month Price Return',
                   'Three-Month Return Percentile',
                   'One-Month Price Return',
                   'One-Month Return Percentile',
                   'HQM Score'
    ]

    hqm_dataframe = pd.DataFrame(columns = hqm_columns)


    for symbol_string in symbol_strings:
      batch_api_call_url = f"https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=price,stats&token={IEX_CLOUD_API_TOKEN}"
      data = requests.get(batch_api_call_url).json()
      for symbol in symbol_string.split(','):
        hqm_dataframe = hqm_dataframe.append(
            pd.Series([
                   symbol,
                   data[symbol]['price'],
                   'n/a',
                   data[symbol]['stats']['year1ChangePercent'],
                   'n/a',
                   data[symbol]['stats']['month6ChangePercent'],
                   'n/a',
                   data[symbol]['stats']['month3ChangePercent'],
                   'n/a',
                   data[symbol]['stats']['month1ChangePercent'],
                   'n/a',
                   'n/a'
            ], index=hqm_columns),
            ignore_index=True
        )

    time_periods = [
                    'One-Year',
                    'Six-Month',
                    'Three-Month',
                    'One-Month'
    ]

    for row in hqm_dataframe.index:
        for time_period in time_periods:
          if hqm_dataframe.loc[row, f'{time_period} Price Return'] == None:
                hqm_dataframe.loc[row, f'{time_period} Price Return'] = np.NaN

    for row in hqm_dataframe.index:
        for time_period in time_periods:
          change_col = f'{time_period} Price Return'
          percentile_col = f'{time_period} Return Percentile'
          hqm_dataframe.loc[row, percentile_col] = score(hqm_dataframe[change_col], hqm_dataframe.loc[row, change_col])/100


    #HQM score: arithmatic mean of the 4 momentum percentile scores that we calculated in the last section
    from statistics import mean

    for row in hqm_dataframe.index:
      momentum_percentiles = []
      for time_period in time_periods:
        momentum_percentiles.append(hqm_dataframe.loc[row, f'{time_period} Return Percentile'])
        hqm_dataframe.loc[row, 'HQM Score'] = float(mean(momentum_percentiles))


    #Selecting the 50 best momentum stocks

    # hqm_dataframe.sort_values('HQM Score', ascending=False, inplace=True)
    # hqm_dataframe = hqm_dataframe[:50]
    # hqm_dataframe.reset_index(inplace=True)

    # portfolio_size = portfolio_input()
    #
    # position_size = float(portfolio_size)/len(hqm_dataframe.index)
    #
    # for i in hqm_dataframe.index:
    #   hqm_dataframe.loc[i,'Number of Shares to buy'] = math.floor(position_size/hqm_dataframe.loc[i,'Price'])

    return hqm_dataframe