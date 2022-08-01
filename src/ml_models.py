from sklearn import linear_model as lm
from numpy import loadtxt
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dropout
from keras.layers import Dense
import pandas as pd
import numpy as np
from services import matrix


def multireg(path, X_set, y, tr_threshold):
    data = pd.read_csv(path, parse_dates=True)
    X_tr, y_tr, X_te = data[X_set][:tr_threshold], data[y][:tr_threshold], data[X_set][tr_threshold:]
    model = lm.LinearRegression()
    model.fit(X_tr, y_tr)
    return sum(model.predict(X_te))


def ann(path, all_vars, X_set, y, tr_threshold):
    data = loadtxt(path, delimiter=',', skiprows=1, usecols=all_vars)
    X_tr, y_tr, X_te = data[:tr_threshold, X_set], data[:tr_threshold, y], data[tr_threshold:, X_set]
    model = Sequential()
    model.add(Dense(3, input_dim=4, kernel_initializer='normal', activation='relu'))
    # model.add(Dropout(0.5, input_shape=(3,)))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)
    model.fit(X_tr, y_tr, epochs=110, batch_size=4, callbacks=[callback])
    return model.predict(X_te)


# def mf_multireg(path, X_set, y, train_threshold):
#     df = pd.read_csv(path, parse_dates=True)
#     train_X, test_X = df[X_set][:train_threshold], df[X_set][train_threshold:]
#     train_y, test_y = df[y][:train_threshold], df[y][train_threshold:]
#     null_y_matrix = matrix.get_null_y_matrix(train_X, y)
#     transposed_matrix = matrix.transpose(null_y_matrix)
#     product_matrix = matrix.multiply(transposed_matrix, null_y_matrix)
#     inverse_matrix = pd.DataFrame(_ for _ in np.linalg.inv(product_matrix.values.tolist()))
#     b_hat = matrix.multiply(transposed_matrix, train_y)
#     b_hat_vals = matrix.multiply(inverse_matrix, b_hat)
#     X_b_hat = matrix.multiply(null_y_matrix, b_hat_vals)
#     e_vals = matrix.add_subtract(train_y, X_b_hat, 'sub')
#     sum_e_sq = matrix.sum_e_sq(e_vals)
#     Ssq_b = (sum_e_sq / (len(train_X) - len(train_X.columns))) * inverse_matrix
#     Ssq_vals = matrix.diaval(Ssq_b)
#     test_list = test_X.values.tolist()
#     output = 0
#     for row in test_list:
#         print(row)
    #     output += Ssq_vals[0]
    #     for value in range(1, len(Ssq_vals)):
    #         output += row[value] * Ssq_vals[value]
    # print(output)
