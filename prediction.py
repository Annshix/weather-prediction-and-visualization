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


class Prediction:
    def __init__(self, f):
        self.data = pandas.DataFrame(read_csv(f, header=0))
        self.scaler = None

    def series2supervise(self, data, n_in=1, n_out=1, is_drop=True):
        data = pandas.DataFrame(data)
        cols, names = list(), list()
        # add input patterns
        for i in range(n_in, 0, -1):
            cols.append(data.shift(i))
        # add output patterns
        for i in range(0, n_out):
            cols.append(data.shift(-i))
        # concat cols to array
        res = concat(cols, axis=1)
        if is_drop:
            res.dropna(inplace=True)
        return res

    def data_prepro(self):
        dt = self.data.sort_values([self.data.columns[0], self.data.columns[1]], ascending=True)
        #dt.reset_index(level=0, inplace=True)
        dt = self.data.astype('float32')
        reframed = self.series2supervise(dt)
        reframed.columns = range(10)
        reframed.drop(reframed.columns[[0, 1, 5, 6, 7, 8]], axis=1, inplace=True)
        print(reframed.shape)
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        reframed = pandas.DataFrame(self.scaler.fit_transform(reframed))
        print(reframed.shape)
        return reframed

    def model(self):
        reframed = self.data_prepro()
        values = reframed.values
        n_train = 365*24
        n_test = 30*24
        train = values[:n_train, :]
        test = values[n_train:n_train+n_test, :]
        train_X, train_y = train[:, :-1], train[:, -1]
        test_X, test_y = test[:, :-1], test[:, -1]

        print(train.shape)
        # reshape
        train_X = train_X.reshape(train_X.shape[0], 1, train_X.shape[1])
        test_X = test_X.reshape(test_X.shape[0], 1, test_X.shape[1])

        # build network
        model = Sequential()
        model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
        model.add(Dense(1))
        model.compile(loss='mae', optimizer='adam')

        # fit
        fit = model.fit(train_X, train_y, epochs=50, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=False)
        print(" -------train loss-------")

        # predict
        res_y = model.predict(test_X)

        # get true value
        test_X = test_X.reshape(test_X.shape[0], test_X.shape[2])
        y = concatenate((test_X[:, :], res_y), axis=1)
        y = self.scaler.inverse_transform(y)
        y = y[:, -1]

        # evaluate RMSE
        ground_y = test_y.reshape((len(test_y), 1))
        ground_y = concatenate((test_X[:, :], ground_y), axis=1)
        ground_y = self.scaler.inverse_transform(ground_y)
        ground_y = ground_y[:, -1]

        print(" -------PREDICTED TEMPERATURE-------")
        print(y)
        print(" -------ERROR DELTA------")
        print(y-ground_y)
        rmse = sqrt(mean_squared_error(y, ground_y))
        print(" -------RMSE------")
        print(rmse)

engine = Prediction('data.csv')
engine.model()
