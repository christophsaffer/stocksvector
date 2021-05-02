import numpy as np
import pandas as pd
import calendar
from os import listdir
import datetime


#Config
DIR_DATA = "data"
DIR_PROCESSED_DATA = "processed_data"


def get_csv_files(path):
    return [csv_file for csv_file in listdir(path) if ".csv" in csv_file]


def get_files_last_N_days(N):
    dt = datetime.datetime.now() - datetime.timedelta(N+1)
    return np.sort([d for d in get_csv_files(DIR_DATA) if datetime.datetime.strptime(d.split(".")[0], '%Y-%m-%d') > dt])


def get_data_last_N_days(N, step_size=0):
    files = get_files_last_N_days(N)
    if step_size == 0:
        step_size = len(files)
    df_combined = pd.DataFrame()
    for day in files:
        df = pd.read_csv("{}/{}".format(DIR_DATA, day), index_col=0)
        df = df[df.index % step_size == 0]
        df["timestamp"] = [timestamp.split(".")[0] for timestamp in df["timestamp"]]
        df.insert(0, "day", day.split(".")[0])
        df.insert(0, "weekday", datetime.datetime.strptime(day.split(".")[0], '%Y-%m-%d').weekday())
        df_combined = df_combined.append(df)
    df_combined.set_index(np.arange(len(df_combined)), inplace=True)

    return df_combined


if __name__ == '__main__':
    days_to_go_back = [3, 7, 30, 100]
    for day in days_to_go_back:
        get_data_last_N_days(day).to_csv("{}/data_last_{}_days.csv".format(DIR_PROCESSED_DATA, day))