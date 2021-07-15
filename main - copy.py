import numpy as np
import pandas

#archivo = open("Text.txt", "r")
lista = np.array(["Primera línea", "Segunda línea", "Tercera línea"])

print(lista)

import requests
token_api_taapi = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImZhYmlhbmtwa0BnbWFpbC5jb20iLCJpYXQiOjE2MTc0Nzk3MDQsImV4cCI6NzkyNDY3OTcwNH0.uWIyH_zRb_Gk3MgMq5CtYrh8gcUBG_TgdHx7R0FBoeo"
#interval =
indicators = ['rsi', 'kdj', 'stochrsi']
timelines = ['1m', '3m', '5m', '15m', '30m',
             '1h', '2h', '4h', '6h', '12h',
             '1d', '3d', '1w']
portafolio = None  # extract from wallet's assets.
# ATTENTION! taapi and binance haven't same names pairs.
params = {"secret": token_api_taapi, "exchange": "binance", "symbol": "ATOM/USDT", "interval": "1m"}
response = requests.get("https://api.taapi.io/rsi", params)
response2 = requests.get("https://api.taapi.io/kdj", params)
response3 = requests.get("https://api.taapi.io/stochrsi", params)
print(response.content)    # RSI
print(response2.content)   # KDJ
print(response3.content)  #StochRSI
py_json = response.json()
print(response2.json())
print(py_json)
print(py_json["value"])

