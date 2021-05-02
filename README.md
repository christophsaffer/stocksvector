# Stocksvector

- A naive project to track, evaluate and analyze stock data

At first, clone the repository.

```
git clone https://github.com/mindpad/stocksvector.git
```

This was tested and developed in python3.6. Additionally, you need to have a number of libraries installed such as numpy, pandas, plotly, cufflinks ...


## Plot current stocks

I uploaded some files in crawler/data.tar.gz. To check the current stock prices, unpack the files, create the necessary processed_data folder and start the following scripts:

```
cd crawler
tar -xf data.tar.gz
mkdir processed_data
python3 process_data.py
python3 plot_data.py
```

## Crawl stocks

To get current stock prices, execute the python script in the crawler folder.

```
python3 crawler/stock-crawler.py
```

To adjust the stocks you'd like to crawl, you have to adjust the file ```crawler/stock_list_finanznachrichten```. Here you have to add the stock's name (should be unique and a valid name (no spaces)) and the link where its value can be found. Be careful: In ```crawler/stock-crawler.py``` around line 65 it is determined how the value is parsed. If you use another site than "finanznachrichten.de", you have to adjust this line of code.
