import pandas as pd
import numpy as numpy

class ExtendedPanda():

    def __init__(self, df):
        self.df = df
            
    def calc_cec(self):
        mean_capital = self.df['invested capital'].apply(numpy.mean)
        mean_equities = self.df['equities'].apply(numpy.mean)
        mean_cash = self.df['cash'].apply(numpy.mean)
        return([mean_capital, mean_equities, mean_cash])


