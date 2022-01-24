import pandas as pd
from alphaVantageAPI import AlphaVantage
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

def createDataFile(ticker, function):
  path = "./data/" + function + "_" + ticker + ".csv"   
  data = av.data(symbol=ticker, function=function)
  del data["1. open"]
  del data["2. high"]
  del data["3. low"]
  del data["5. volume"]
  data.rename(columns = {'4. close':'close'}, inplace = True)
  data.to_csv(path, index=False)

targetPath = './data/'
while not os.path.exists(targetPath):
  os.mkdir(targetPath)
createDataFile("VTI", "M")
createDataFile("VXUS", "M")
createDataFile("BND", "M")
createDataFile("VTI", "D")
createDataFile("VXUS", "D")
createDataFile("BND", "D")
