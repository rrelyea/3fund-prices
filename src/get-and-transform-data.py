import pandas as pd
from alphaVantageAPI import AlphaVantage
import sys

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
ticker_M_VTI = av.data(symbol="VTI", function="M")
print(ticker_M_VTI)
ticker_D_VTI = av.data(symbol="VTI", function="D")
print(ticker_D_VTI)