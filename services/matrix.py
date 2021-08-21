import pandas as pd
import numpy as np


def get_determinant(df_m):
    sub_matrix_set = [df_m]
    all_column_combinations = []
    matrix_indexer = len(df_m)
    while len(sub_matrix_set[len(sub_matrix_set) - 1]) > 2:
        for matrix in sub_matrix_set[matrix_indexer:]:
            matrix_columns = [matrix[matrix.columns[col]].tolist() for col in range(len(matrix))]
            matrix_column_combinations = []
            for i, row in enumerate(matrix):
                matrix_column_combinations.append([matrix_columns[lst] for lst in range(len(matrix)) if lst != i])
            all_column_combinations.append(matrix_column_combinations)
        for matrix_combination_set in all_column_combinations:
            if len(matrix_combination_set) <= matrix_indexer:
                for i, combination in enumerate(matrix_combination_set):
                    sub_matrix = pd.DataFrame()
                    for ii, column in enumerate(combination):
                        column_ = column.copy()
                        del column_[0]
                        sub_matrix['{}'.format(ii)] = column_
                    sub_matrix_set.append(sub_matrix)
        all_column_combinations = []
        matrix_indexer -= 1
    # output_matrix = []
    # while len(output_matrix[0]) < len(df_m):
    #     print()
    return sub_matrix_set  # output_matrix[0]


def get_null_y_matrix(df_m, dependent_column):
    null_y_matrix = pd.DataFrame()
    sets = [df_m[column].tolist() for column in df_m.columns if not column == dependent_column[0]]
    sets.insert(0, [1 for _ in range(len(df_m))])
    for i, set_ in enumerate(sets):
        null_y_matrix['{}'.format(i)] = set_
    return null_y_matrix


def transpose(df_m):
    df_mT = pd.DataFrame()
    matrix = df_m.values.tolist()
    for i, row in enumerate(matrix):
        df_mT['{}'.format(i)] = row
    return df_mT


def multiply(df_ml, df_mr):
    set_ = []
    for ii in range(len(df_mr.columns)):
        column_ = df_mr[list(df_mr.columns)[ii]].tolist()
        col_vals = []
        for i in range(len(df_ml)):
            row_ = df_ml.loc[i, :].values.flatten().tolist()
            val = sum([row_[iii] * column_[iii] for iii in range(len(row_))])
            col_vals.append(val)
        set_.append(col_vals)
    df_product = pd.DataFrame()
    for col in range(len(set_)):
        df_product["m{}".format(col)] = set_[col]
    return df_product


def get_identity_matrix(df_m):
    identity_matrix = pd.DataFrame()
    for i, set_ in enumerate(df_m.columns):
        vals = np.array([0 for _ in range(len(df_m))])
        vals[i] = 1
        identity_matrix["m{}".format(i)] = vals
    return identity_matrix


def add_subtract(df_ml, df_mr, operation='add'):
    ml_list = [df_ml[column].tolist() for column in df_ml.columns]
    mr_list = [df_mr[column].tolist() for column in df_mr.columns]
    new_columns = []
    for column in range(len(ml_list)):
        new_column = []
        for item in range(len(ml_list[column])):
            if operation == 'add':
                new_column.append(ml_list[column][item] + mr_list[column][item])
            else:
                new_column.append(ml_list[column][item] - mr_list[column][item])
        new_columns.append(new_column)
    df_m_out = pd.DataFrame()
    for column in range(len(new_columns)):
        df_m_out['{}'.format(column)] = new_columns[column]
    return df_m_out


def diaval(df_m):
    vals = []
    for row in range(len(df_m)):
        vals.append(df_m.iat[row, row])
    return vals


def sum_e_sq(df_e):
    sum_e_sq_ = 0
    for val in df_e.values.tolist():
        for val_ in val:
            sum_e_sq_ += np.square(val_)
    return sum_e_sq_
