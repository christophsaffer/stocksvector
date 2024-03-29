import requests
import calendar
import pandas as pd
import numpy as np
import os.path

# CONFIG #
STOCK_CSV_FILE = "stock_list_finanznachrichten.csv"
DIR_DATA = "."
TODAY_DATE = str(calendar.datetime.datetime.now()).split(" ")[0]
CURRENT_FILE = DIR_DATA + "/" + TODAY_DATE + ".csv"
DEBUG = True


def print_debug(s):
    if (DEBUG):
        print(s)


def download(url, user_agent='wswp', num_retries=2, proxies=None):
    print_debug('Downloading: {}'.format(url))
    headers = {'User-Agent': user_agent}
    try:
        resp = requests.get(f"{url}", headers=headers, proxies=proxies)
        html = resp.text
        if resp.status_code >= 400:
            print('Download error:', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    except requests.exceptions.RequestException as e:
        print('Download error:', e.reason)
        html = None

    return html


def create_file_for_today():
    if not os.path.isfile(CURRENT_FILE):
        link_list = pd.read_csv(STOCK_CSV_FILE)
        names = link_list["name"].values
        names = ["timestamp"] + list(names)
        stocks_empty = pd.DataFrame(columns=names)
        stocks_empty.to_csv(CURRENT_FILE)
        print_debug("Created {}".format(CURRENT_FILE))
    else:
        print_debug("{} already exists for today".format(CURRENT_FILE))


def get_current_stock_values(stock_data):
    link_list = pd.read_csv(STOCK_CSV_FILE)
    names = stock_data.columns
    stock_names = names[1:]

    curr_values = []
    curr_timestep = str(calendar.datetime.datetime.now()).split(" ")[1]
    curr_values.append(curr_timestep)
    for name in stock_names:
        link = link_list[link_list["name"] == name]["link"].values[0]
        current_val = -1
        try:
            html = download(link)
            # apparently the most important line in this script: Responsible for parsing out the actual stock value
            current_val = html.split("priceCurrency")[0][-150:-1].split('Rate">')[1].split("<")[0].replace(",", ".")
        except:
            current_val = -1
        print_debug("{}: {}".format(name, current_val))
        curr_values.append(current_val)

    return pd.DataFrame(np.array(curr_values).reshape(1, len(curr_values)), columns=names)


if __name__ == '__main__':
    create_file_for_today()
    stock_data = pd.read_csv(CURRENT_FILE, index_col=0)
    current_minute = get_current_stock_values(stock_data)
    updated_stock_data = stock_data.append(current_minute, ignore_index=True)
    updated_stock_data.to_csv(CURRENT_FILE)

