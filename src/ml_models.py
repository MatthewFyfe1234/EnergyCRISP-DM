from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
from sklearn import linear_model as lm


def multireg(path, X_set, y, train_threshold):
    df = pd.read_csv(path, parse_dates=True)
    train_X, test_X = df[X_set][:train_threshold], df[X_set][train_threshold:]
    train_y, test_y = df[y][:train_threshold], df[y][train_threshold:]
    regr = lm.LinearRegression()
    regr.fit(train_X, train_y)
    test_forecast = []
    for index, row in test_X.iterrows():
        test = regr.predict([[row[variable] for variable in X_set]])
        test_forecast.append(test[0])
    sum_test_forecast = sum(v for i, v in enumerate(test_forecast))
    return sum_test_forecast


def ann(path, all_vars, ind_vars, dep_var, train_threshold):
    data = loadtxt(path, delimiter=',', skiprows=1, usecols=all_vars)
    X, y = data[:, ind_vars], data[:, dep_var]
    model = Sequential()
    model.add(Dense(12, input_dim=3, kernel_initializer='normal', activation='relu'))
    model.add(Dense(6, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X, y, epochs=150, batch_size=3)
    pred_train = model.predict(X)
    sum_test_forecast = sum(pred_train[train_threshold:])[0]
    return sum_test_forecast
