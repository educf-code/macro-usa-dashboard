# -*- coding: utf-8 -*-
"""Teste.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SYrI-RU63NMHDR8EnM03cETZpmvmjQkI
"""

from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from google.colab import userdata
from urllib.parse import urlencode
import time
import requests as req
import pandas as pd
import numpy as np
import os

base_url = "https://api.stlouisfed.org/fred/series/observations"
api_key = ''
if (os.environ.get("FRED_API_KEY")):
  api_key = os.environ.get("FRED_API_KEY")
else:
  api_key = userdata.get("FRED_API_KEY")

from datetime import datetime
from dateutil.relativedelta import relativedelta

today = datetime.today()

one_year_ago = today - relativedelta(years=1)

print(one_year_ago.strftime("%Y-%m-%d"))

data_info = {
    "fed_funds_effective_rate": {
        "series_id": "DFF",
        "observation_start": one_year_ago,
        "frequency": "d",
        "observation_start": one_year_ago.strftime("%Y-%m-%d")
    }
}

with pd.ExcelWriter("database.xlsx", mode="w", engine="openpyxl") as writer:
  for key, params in data_info.items():
      query_params = {
          "series_id": params["series_id"],
          "observation_start": params["observation_start"],
          "frequency": params["frequency"],
          "api_key": api_key,
          "file_type": "json"
      }

      url = f"{base_url}?{urlencode(query_params)}"
      res = req.get(url)
      time.sleep(10)
      data = res.json()

      for dictonary in data["observations"]:
        del dictonary["realtime_start"]
        del dictonary["realtime_end"]

      df = pd.DataFrame(data["observations"], index=None)
      df.to_excel("database.xlsx", sheet_name=key, index= False)

