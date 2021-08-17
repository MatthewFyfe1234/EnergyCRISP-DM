import pandas as pd
import numpy as np
import datetime
from datetime import datetime as dt


def get_timeline_instance_set(df, dt_col, dt_format, interval):
    actual_datetimes = [datetime.datetime.strptime(value, dt_format) for value in list(df[dt_col])]
    start, end = min(actual_datetimes), max(actual_datetimes)
    return pd.date_range(start=start, end=end, freq=interval).to_pydatetime().tolist()


def report_missing_datetimes(df, dt_col, dt_format, interval):
    complete_dt_set = get_timeline_instance_set(df, dt_col, dt_format, interval)
    indexed_complete_set = {complete_dt_set[value]: value for value in range(len(complete_dt_set))}
    for value in list(df[dt_col]):
        del indexed_complete_set[datetime.datetime.strptime(value, dt_format)]
    return dict((v, k) for k, v in indexed_complete_set.items())


def replace_missing_datetimes(df, dt_col, dt_format, interval):
    missing_datetimes = report_missing_datetimes(df, dt_col, dt_format, interval)
    add_df = pd.DataFrame(columns=df.columns)
    for row, datetime_ in missing_datetimes.items():
        row_set = [np.nan for _ in range(len(df.columns))]
        row_set[df.columns.get_loc(dt_col)] = datetime_.strftime(dt_format)
        add_df.loc[row] = row_set
    df = pd.concat([df, add_df])
    df.sort_values(by='Timestamp', key=pd.to_datetime, inplace=True, ascending=True)
    return df


def add_day_hour_week_columns(df, dt_col, dt_format, period):
    timeline, new_col = list(df[dt_col]), []
    for element in range(len(timeline)):
        if period == 'Day':
            new_col.append(dt.strptime(timeline[element], dt_format).weekday())
        if period == 'Hour':
            new_col.append(dt.strptime(timeline[element], dt_format).hour)
        if period == 'Week':
            new_col.append(dt.strptime(timeline[element], dt_format).isocalendar()[1])
    df[period] = new_col
    return df
