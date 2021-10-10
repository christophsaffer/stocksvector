import numpy as np
import pandas as pd
from os import listdir
import datetime


# CONFIG
DIR_DATA = "data"
DIR_PROCESSED_DATA = "processed_data"
DEBUG = True


def print_debug(s):
    if (DEBUG):
        print(s)


def get_csv_files(path: str) -> list:
    return [csv_file for csv_file in listdir(path) if ".csv" in csv_file]


def get_files_last_n_days(n: int, init_day=datetime.datetime.now()) -> list:
    dt = init_day - datetime.timedelta(n+1)
    return sorted([d for d in get_csv_files(DIR_DATA) if datetime.datetime.strptime(d.split(".")[0], '%Y-%m-%d') > dt])


def clean_data_set(data: pd.DataFrame, from_column=1) -> pd.DataFrame:
    # remove milliseconds from "timestamp" column
    data["timestamp"] = [timestamp.split(".")[0] for timestamp in data["timestamp"]]
    data.insert(0, "daytime", [int(timestamp.split(":")[0]) - 8 for timestamp in data["timestamp"]])

    # remove wrong values
    for ind in data[(data.iloc[:, from_column:] < 0).any(1)].index:
        for col in data.columns[from_column:]:
            if data.loc[ind, col] < 0:
                if ind != 0:
                    # replace values that are smaller than 1 (=error) with the value from the minute before
                    data.loc[ind, col] = data.loc[ind - 1, col]
                else:
                    # if first value is smaller than 1 (=error), then replace it with the mean value
                    data.loc[ind, col] = data[data[col] > 0][col].mean()
    return data[60:900].reset_index(drop=True)


def merge_files(file_list: list, step_size=1) -> pd.DataFrame:
    df_combined = pd.DataFrame()
    print_debug("Start to combine {} files ...".format(len(file_list)))
    for file in file_list:
        data = pd.read_csv("{}/{}".format(DIR_DATA, file), index_col=0)
        data = clean_data_set(data)
        data = data[data.index % step_size == 0]
        data.insert(0, "day", file.split(".")[0])
        data.insert(0, "weekday", datetime.datetime.strptime(file.split(".")[0], '%Y-%m-%d').weekday())
        df_combined = df_combined.append(data)
    df_combined.set_index(np.arange(len(df_combined)), inplace=True)

    print_debug("done.")
    return df_combined


def summarize_data_set(dataframe: pd.DataFrame, ao: int) -> pd.DataFrame:
    # ao == average over
    print_debug("Start to summarise a stock value every {} minutes of each stock ...".format(ao))
    new_dataframe = pd.DataFrame(columns=dataframe.columns)
    for i in range(int(len(dataframe) / ao)):
        curr_col = list(dataframe.iloc[i * ao:(i + 1) * ao, 3:].mean().values)
        mid = int(ao * (i + 0.5))
        for j in [2, 1, 0]:
            curr_col.insert(0, dataframe.iloc[mid, j])
        new_dataframe.loc[len(new_dataframe)] = curr_col
    print("done.")

    return new_dataframe


if __name__ == '__main__':
    list_of_files = get_files_last_n_days(5)  # get stockdata from last 365 days (depends on input files)
    df = merge_files(list_of_files)  # merge all files
    df_s = summarize_data_set(df, 2)  # take mean value of every 30 minutes from each stock
    df_s.to_csv("{}/processed_stock_data.csv".format(DIR_PROCESSED_DATA))
    print_debug("Saved processed dataframe to {}/".format(DIR_PROCESSED_DATA))
