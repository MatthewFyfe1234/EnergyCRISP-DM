import math
import numpy as np
import pandas as pd
import glob


def csv_multi_read(inner_path, columns):
    return [pd.read_csv(filename, usecols=columns) for filename in glob.glob(inner_path + "/*.csv")]


def mean_of_list_of_not_nans(vals, incident_index, limiter_vals, limiter_val, increment):  # This name is bad
    limiter_index_set = [val for val in range(len(limiter_vals)) if limiter_vals[val] == limiter_val]
    num_increments_before = math.floor(incident_index/increment)
    first_index = int(incident_index - num_increments_before * increment)
    all_indices = [index for index in range(first_index, len(vals), increment) if index in limiter_index_set]
    non_nans = []
    for i, v in enumerate(vals):
        if not math.isnan(v) and i in all_indices:
            non_nans.append(v)
    return sum(non_nans)/len(non_nans)


def ml_performance_output(model, ind_var, test_actual, test_forecast):
    return (
        '*********************************************************\n' +
        '{} model results for: {}\n'.format(model, ind_var) +
        'Test measured: ' + str(round(test_actual, 2)) + '\n'
        'Test predicted: ' + str(round(test_forecast, 2)) + '\n'
        'Measured as percentage of prediction: ' + str(round(test_actual / test_forecast * 100, 2)) + '%\n'
        '*********************************************************'
    )


def co_variance(set_x, set_y):
    mean_x, mean_y = np.mean(set_x), np.mean(set_y)
    numerator = sum([(set_x[val] - mean_x) * (set_y[val] - mean_y) for val in range(len(set_x))])
    return numerator/(len(set_x))


def slope(set_x, set_y):
    covariance = co_variance(list(set_x), list(set_y))
    std_dev = np.square(np.std(set_x))
    return covariance/std_dev


def intercept(set_x, set_y):
    b1_est = slope(list(set_x), list(set_y))
    x_mean, y_mean = np.mean(list(set_x)), np.mean(list(set_y))
    return y_mean - b1_est * x_mean


def get_y(set_x, set_y, x_val):
    return intercept(set_x, set_y) + slope(set_x, set_y) * x_val


def coeff_of_determination(set_x, set_y):
    sum_e_sq = sum([np.square(list(set_y)[element] - get_y(set_x, set_y, list(set_x)[element]))
                    for element in range(len(set_y))])
    sum_y_sq = sum([np.square(list(set_y)[element] - np.mean(list(set_y))) for element in range(len(set_y))])
    return 1 - sum_e_sq/sum_y_sq
