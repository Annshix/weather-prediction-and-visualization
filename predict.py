import pandas
from pandas import read_csv
from pandas import concat
from numpy import concatenate
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from math import sqrt

class Predict:
    def __init__(self, model, input):
        self.model = model
        self.input = input

    def predict(self):
        output = self.model.predict(self.input)
        return output
