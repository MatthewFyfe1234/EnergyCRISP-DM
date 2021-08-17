from services import general as g
import data_visualisation as dv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

hourly_data = pd.read_csv(r'test.csv', index_col=0)
agg_settings = {'Demand': 'sum', 'Generation': 'sum', 'Import': 'sum', 'Solar': 'sum', 'Wind': 'sum',
                'Other': 'sum', 'Day': 'min', 'Hour': 'min', 'Week': 'min', 't_mean_2m_1h:C': 'mean',
                'wind_speed_mean_10m_1h:ms': 'mean', 'daylight_status': 'min'}
average_day_hourly = hourly_data.groupby(['Hour']).agg(agg_settings)
del average_day_hourly['daylight_status'], average_day_hourly['Week'], average_day_hourly['Day']

fig, axis = plt.subplots(1, 3, figsize=(20, 7), sharex='none', sharey='none')
dv.subplot_line_set(['Demand', 'Generation', 'Import'], axis, 0, 'Energy Usage, Import and Generation', 'Hour of day',
                    'Energy (MW)', [0, 24], ['Demand', 'Generation', 'Import'], [0, 25, 2], average_day_hourly)
dv.subplot_line_set(['Solar', 'Wind', 'Other'], axis, 1, 'Generation Components', 'Hour of day', 'Energy (MW)', [0, 24],
                    ['Solar', 'Wind', 'Other'], [0, 25, 2], average_day_hourly)
# PLOT WIND SPEEDS ON SECONDARY Y AXIS
dv.subplot_line_set(['t_mean_2m_1h:C', 'wind_speed_mean_10m_1h:ms'], axis, 2, 'Wind and Temperature', 'Hour of day',
                    'Temperature (C)', [0, 24], ['t_mean_2m_1h:C', 'wind_speed_mean_10m_1h:ms'], [0, 25, 2],
                    average_day_hourly)
plt.show()

grouped_hours = [group.drop_duplicates() for _, group in hourly_data.groupby('Hour')]
dependents = ['Demand', 'Import']
std_dev_vars = ['Demand', 'Generation', 'Import', 'Solar', 't_mean_2m_1h:C', 'wind_speed_mean_10m_1h:ms', 'daylight_status']
rsq_inds = ['Solar', 'Day', 't_mean_2m_1h:C', 'wind_speed_mean_10m_1h:ms']
std_dev_inds = [[np.std(hour[variable])/np.mean(hour[variable]) for hour in grouped_hours] for variable in std_dev_vars]
rsq_inds_vs_demand, rsq_inds_vs_import = [], []
for ind_var in rsq_inds:
    rsqs_demand = [g.coeff_of_determination(hour[ind_var], hour[dependents[0]]) for hour in grouped_hours]
    rsqs_import = [g.coeff_of_determination(hour[ind_var], hour[dependents[1]]) for hour in grouped_hours]
    rsq_inds_vs_demand.append(rsqs_demand)
    rsq_inds_vs_import.append(rsqs_import)

fig2, axis = plt.subplots(1, 3, figsize=(20, 7), sharex='none', sharey='none')
dv.subplot_line_set([_ for _ in std_dev_inds], axis, 0, 'Standard Deviation for Various Variables Throughout the Day',
                    'Hour of day', 'Coefficient of Standard Deviation', [0, 24], std_dev_vars, [0, 25, 2])
dv.subplot_line_set([_ for _ in rsq_inds_vs_demand], axis, 1, 'R Squared for Various Variables Throughout the Day',
                    'Hour of day', 'R Squared', [0, 24], rsq_inds, [0, 25, 2])
dv.subplot_line_set([_ for _ in rsq_inds_vs_import], axis, 2, 'R Squared for Various Variables Throughout the Day',
                    'Hour of day', 'R Squared', [0, 24], rsq_inds, [0, 25, 2])
plt.show()
