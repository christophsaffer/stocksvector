# Stocksvector

- A naive project to track, evaluate and analyze stock data


## Crawl stocks

At first, clone the repository.

```
git clone https://github.com/mindpad/stocksvector.git
```

To get current stock prices, go in the folder crawler and execute the python script.

```
cd crawler
python3 stock-crawler.py
```

To adjust the stocks you'd like to crawl, you have to adjust the file ```crawler/stock_list_finanznachrichten```. Here you have to add the stock's name (should be unique and a valid name (no spaces)) and the link where its value can be found. Be careful: In ```crawler/stock-crawler.py``` around line 65 it is determined how the value is parsed. If you use another site than "finanznachrichten.de", you have to adjust this line of code.
