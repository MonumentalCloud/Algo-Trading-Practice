
from measures.value_trading import robust_value_data
from measures.momentum_strategy import hq_momentum_data
from sentimentAnalysis.sentiment_analysis import sentiment
import pandas as pd
import numpy as np

def central_sheet():
    hqm_dataframe = hq_momentum_data()
    rv_dataframe = robust_value_data()
    sentiment_dataframe = sentiment()

    final_dataframe = pd.DataFrame()
    final_dataframe[['Ticker','HQM Score']] = hqm_dataframe[['Ticker','HQM Score']]
    final_dataframe['Robust Value Score'] = rv_dataframe['Robust Value Score']

    return final_dataframe





