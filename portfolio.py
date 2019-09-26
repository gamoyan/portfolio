import pandas as pd
from functools import reduce

class Portfolio:
    path = "./data/"
    def __init__(self, code, units):
        self.stocks = {}
        self.df = pd.DataFrame()
        self.since = 2015
        self.to = 2020

        for c, u in zip(code, units):
            self.stocks[c] = u
        self.loadAll()

    def __getitem__(self, code):
        return self.stocks[code]
    
    def __setitem__(self, code, units):
        self.stocks[code] = units
        
    def load(self, code):
        c = [pd.read_csv(Portfolio.path+str(code)+"_"+str(year)+".csv",
                         header=1, index_col=0, usecols=[0, 4],
                         names=['date', code],
                         parse_dates=True, encoding='shift-jis')
             for year in range(self.since, self.to)]
        return pd.concat(c)
        
    def loadAll(self):
        p = []
        for code in self.stocks.keys():
            c = self.load(code)
            p.append(c)
        self.df = reduce(lambda x, y: x.join(y, how='inner'), p)
       
    def add(self, code, units):
        if code not in self.stocks.keys():
            c = self.load(code)
            self.df.join(c, how='inner')
        self.stocks[code] = units

    def remove(self, code):
        try:
            del self.stocks[code]
        except KeyError:
            print('does not exist')
        else:
            self.df.drop(code, axis=1, inplace=True)
        
    def plot(self, _figsize=(16,4), _legend=False):
        self.df.plot(figsize=_figsize, legend=_legend)

    def subplots(self, _figsize=(16,3)):
        fs = _figsize[0], _figsize[1]*len(self.stocks)
        self.df.plot(figsize=fs, subplots=True)
        
    def total(self, _figsize=(16,4), _legend=False):
        value = self.df * list(self.stocks.values())
        value.sum(axis=1).plot(figsize=_figsize, legend=_legend)


def nikkei():
    n = pd.read_csv(Portfolio.path+"nikkei225.csv", header=9, index_col=0,
                    names=['Date', 'Nikkei225'], parse_dates=True)
    return n
