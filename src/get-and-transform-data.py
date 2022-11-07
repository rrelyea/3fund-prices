import pandas as pd
from alphaVantageAPI import AlphaVantage
from datetime import *
from dateutil.relativedelta import *
import calendar
import sys
import os

if len(sys.argv) >= 3 and sys.argv[1] == "--key":
  key = sys.argv[2]
if len(sys.argv) >= 5 and sys.argv[3] == "--etf":
  etf = sys.argv[4] == "true"

av = AlphaVantage(
        api_key=key,
        premium=False,
        output_size="compact",
        datatype='json',
        export=False,
        export_path="~/av_data",
        output="csv",
        clean=False,
        proxy={}
    )

def updateTicker(ticker):
  updateData(ticker, "MA") # monthly adjusted for dividends
  updateData(ticker, "D")

def updateData(ticker, function):
  path = "./data/" + function + "_" + ticker + ".csv"
  try:
    data = av.data(symbol=ticker, function=function)
    del data["1. open"]
    del data["2. high"]
    del data["3. low"]

    if (function == "MA"):
        del data["6. volume"]
        data.rename(columns = {'4. close':'close', '5. adjusted close':'adjusted close', '7. dividend amount':'dividend'}, inplace = True)
    elif (function == "D"):
        del data["5. volume"]
        data.rename(columns = {'4. close':'close'}, inplace = True)
      
        startOfMonth = datetime.today().replace(day=1)
        endOfLastMonth = startOfMonth + relativedelta(days=-1)

        if datetime.today().month == 12:
          startOfNextMonth = startOfMonth.replace(month=1,year=datetime.today().year + 1)
        else:
          startOfNextMonth = startOfMonth.replace(month=startOfMonth.month+1)
        data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
        data = data.query("date > '" + str(endOfLastMonth) + "' \
                          and date < '" + str(startOfNextMonth) + "'")
    
    num_rows = data.count()[0]
    if num_rows > 0:   # don't overwrite last months daily data until there is at least one day worth of data.
      data.to_csv(path, index=False)
    print("fetched " + ticker + " " + function, flush=True)
  except ValueError:
    print("ValueError: fetching " + ticker + " " + function, flush=True)

targetPath = './data/'
while not os.path.exists(targetPath):
  os.mkdir(targetPath)

fundTypes = pd.read_csv('./data/fundTypes.csv')
for i, funds in fundTypes.iterrows():
  if etf and funds['type'].endswith("ETF"):
    print(i, funds['stockFund'], funds['internationalStockFund'],funds['bondFund'])
    updateTicker(funds['stockFund'])
    updateTicker(funds['internationalStockFund'])
    updateTicker(funds['bondFund'])
  elif not etf and not funds['type'].endswith("ETF"):
    print(i, funds['stockFund'], funds['internationalStockFund'],funds['bondFund'])
    updateTicker(funds['stockFund'])
    updateTicker(funds['internationalStockFund'])
    updateTicker(funds['bondFund'])
