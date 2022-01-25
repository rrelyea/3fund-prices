import pandas as pd
from alphaVantageAPI import AlphaVantage
from datetime import date,datetime
import sys
import os

if len(sys.argv) >= 3 and sys.argv[1] == "--key":
  key = sys.argv[2]

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

def updateData(ticker, function):
  path = "./data/" + function + "_" + ticker + ".csv"   
  data = av.data(symbol=ticker, function=function)
  del data["1. open"]
  del data["2. high"]
  del data["3. low"]
  del data["5. volume"]
  data.rename(columns = {'4. close':'close'}, inplace = True)
  if function == "D":
    startOfMonth = datetime.today().replace(day=1)
    if datetime.today().month == 12:
      startOfNextMonth = startOfMonth.replace(month=1,year=datetime.today().year + 1)
    else:
      startOfNextMonth = startOfMonth.replace(month=startOfMonth.month+1)
    data['date'] = pd.to_datetime(data['date'], format='%Y-%m-%d')
    data = data.query("date >= '" + str(startOfMonth) + "' \
                      and date < '" + str(startOfNextMonth) + "'")
  data.to_csv(path, index=False)

def updateTicker(ticker):
  updateData(ticker, "M")
  updateData(ticker, "D")

targetPath = './data/'
while not os.path.exists(targetPath):
  os.mkdir(targetPath)

tickers = ["VTI", "VXUS", "BND", "VTSAX", "VTIAX", "VBTLX"]

for ticker in tickers:
  updateTicker(ticker)
