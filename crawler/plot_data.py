import numpy as np
import pandas as pd

import cufflinks as cf
import plotly.express as px
cf.go_offline()


# CONFIG
DIR_DATA = "data"
DIR_PROCESSED_DATA = "processed_data"


def plot_stocks_value_range(df: pd.DataFrame, minval: int, maxval: int):
    x_values = df["day"] + " " + df["timestamp"]

    dataframe = pd.DataFrame()
    dataframe["date"] = x_values
    for col in df.columns[3:]:
        if maxval > df[col].mean() > minval:
            dataframe[col] = df[col]

    step_size = int(len(dataframe) / 4)
    ticks = np.arange(4) * step_size + int(step_size / 2)
    values = dataframe.loc[ticks, "date"].values
    fig = px.line(dataframe, x=dataframe.index, y=[x for x in dataframe.columns if x != "date"],
                  labels=dict(index="Time", value="Price"))
    fig.update_layout(xaxis=dict(tickmode='array', tickvals=ticks, ticktext=values))

    return fig


if __name__ == '__main__':
    df = pd.read_csv("{}/processed_stock_data.csv".format(DIR_PROCESSED_DATA), index_col=0)
    # adjust the range of the stocks you'd like to check (df, min, max)
    plot_stocks_value_range(df, 90, 110).show()
