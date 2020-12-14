from central_sheet import central_sheet
import pandas as pd

#REWARD
idlePunish = -1
buyReward = 1

class env:
    def __init__(self):
        self.sheets = central_sheet()
        self.history = pd.DataFrame()

    def step(self, action):
        if action.type == None:
            return (self.sheets, idlePunish)
        elif action.type == "Buy":
            return (self.sheets, buyReward)
        elif action.type == "Sell":
            past_position = self.history[self.history['Ticker'] == action.ticker]
            self.history[self.history['Ticker'] == action.ticker]['Size'] = self.history[self.history['Ticker'] == action.ticker]['Size'] - action.size
            sellReward = (self.sheets.loc[action.row, 'Price'] - past_position['Price'])*action.size
            return (self.sheets, sellReward)