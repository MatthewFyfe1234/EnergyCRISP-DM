from services import timeseries as t
from datetime import datetime as dt
from services import general as g
import math
import pandas as pd


def aggregate_gridded_weather_data():
    # Aggregate gridded weather data
    temp_sets = g.csv_multi_read('data/temperatures_historic', [2, 3])
    wind_sets = g.csv_multi_read('data/wind_speeds_historic', [2, 3])
    # The loop groups and means the grid points for each location, then the outer groupby groups and means the locations
    weather_means = pd.concat([set_.groupby(['validdate']).mean() for set_ in temp_sets]).groupby(['validdate']).mean()
    wind_means = pd.concat([set_.groupby(['validdate']).mean() for set_ in wind_sets]).groupby(['validdate']).mean()
    weather_means['wind_speed_mean_10m_1h:ms'] = wind_means['wind_speed_mean_10m_1h:ms']
    weather_means.index = pd.to_datetime(weather_means.index, errors='coerce')
    return weather_means


def dsa_data_quality():
    # Load and improve quality of DSA Dataset
    energy_data = pd.read_csv('data/DSA_Dataset.csv')
    # Ensure complete timeseries column
    energy_data = t.replace_missing_datetimes(energy_data, 'Timestamp', '%m/%d/%Y %H:%M', '5min')
    for period in ['Day', 'Hour', 'Week']:
        energy_data = t.add_day_hour_week_columns(energy_data, 'Timestamp', '%m/%d/%Y %H:%M', period)
    # Split into weeks, by weekday/weekend day, to accurately replace nan's
    weekday_weekend_sets = [energy_data[energy_data['Day'] < 5], energy_data[energy_data['Day'] > 4]]
    # Replace missing values in all sets
    for set_ in range(len(weekday_weekend_sets)):
        for column in ['Demand', 'Generation', 'Import', 'Solar', 'Wind', 'Other']:
            value_list = list(weekday_weekend_sets[set_][column])
            limiter_list = list(weekday_weekend_sets[set_]['Week'])
            for i, v in enumerate(value_list):
                if math.isnan(v):
                    week = limiter_list[i]
                    value_list[i] = round(g.mean_of_list_of_not_nans(value_list, i, limiter_list, week, 288), 2)
            weekday_weekend_sets[set_][column] = value_list
    # Recompile energy data and sort in timeseries order
    recompiled_energy = pd.concat(set_ for set_ in weekday_weekend_sets)
    recompiled_energy.sort_values(by='Timestamp', key=pd.to_datetime, inplace=True, ascending=True)
    return recompiled_energy


def compile_weather_and_energy_data(weather_data, energy_data):
    energy_data['Timestamp'] = pd.to_datetime(energy_data['Timestamp'])
    energy_data.set_index('Timestamp', inplace=True, drop=False)
    agg_settings = {'Demand': 'sum', 'Generation': 'sum', 'Import': 'sum', 'Solar': 'sum', 'Wind': 'sum',
                    'Other': 'sum', 'Day': 'min', 'Hour': 'min', 'Week': 'min'}
    reduced = energy_data.resample('H').agg(agg_settings)
    reduced = reduced.tz_localize('utc')
    abt = reduced.join(weather_data, on='Timestamp', how='left', lsuffix='_left', rsuffix='_right')
    return abt


def intergrate_daylight_status(abt):
    daylight_data = pd.read_csv('data/daylight hours.csv')
    daylight_data = daylight_data.set_index('date')
    daylight_data.index = pd.to_datetime(daylight_data.index, errors='coerce')
    daylight_data = daylight_data.tz_localize('utc')
    abt['sunrise'], abt['sunset'], abt['daylight_status'] = '', '', ''
    for i, v in enumerate(abt.index.tolist()):
        for ii, vv in enumerate(daylight_data.index.tolist()):
            if v.date() == vv.date():
                abt.iat[i, abt.columns.get_loc('sunrise')] = list(daylight_data['sunrise'])[ii]
                abt.iat[i, abt.columns.get_loc('sunset')] = list(daylight_data['sunset'])[ii]
        date_time = v.time()
        sunrise = dt.strptime(abt.iat[i, abt.columns.get_loc('sunrise')], '%H:%M').time()
        sunset = dt.strptime(abt.iat[i, abt.columns.get_loc('sunset')], '%H:%M').time()
        abt.iat[i, abt.columns.get_loc('daylight_status')] = 1 if sunrise <= date_time <= sunset else 2
    del abt['sunrise'], abt['sunset']
    return abt


# DONT FORGET TO DEAL WITH OULIERS
