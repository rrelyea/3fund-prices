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
  data = av.data(symbol=ticker, function=function)
  file = open("data/"+function+"_"+ticker+".txt", 'w') 
  file.write(data)
  file.close()

targetPath = './data/'
while not os.path.exists(targetPath):
  os.mkdir(targetPath)
createDataFile("VTI", "M")
createDataFile("VXUS", "M")
createDataFile("BND", "M")