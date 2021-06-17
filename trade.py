from logging import info
import requests, json
import alpaca_trade_api as tradeapi
import yfinance as yf
from pandas_datareader import data as pdr
import pandas as pd

API_KEY = 'PKRZJKT6ZDLCXGSMF2XT'
API_SECRET_KEY = 'yDQmgrdxXTBdCYIBiqVcFJfbB89zToY97aYqmVOw'
HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': API_SECRET_KEY}

endpoint_URL = "https://paper-api.alpaca.markets"
account_URL = "{}/v2/account".format(endpoint_URL)
orders_URL = "{}/v2/orders".format(endpoint_URL)

api = tradeapi.REST(API_KEY, secret_key=API_SECRET_KEY, base_url=endpoint_URL)

def get_account():
    r = requests.get(account_URL, headers=HEADERS)
    return json.loads(r.content)

def place_order(symbol, qty, side, type, time_in_force):
    data = {
        'symbol': symbol,
        'qty': qty,
        'side': side,
        'type': type,
        'time_in_force': time_in_force
    }

    r = requests.post(orders_URL, json=data, headers=HEADERS)
    return json.loads(r.content)

def get_orders():
    r = requests.get(orders_URL, headers=HEADERS)
    orders = json.loads(r.content)
    return orders



# list all stocks
url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
df=pd.read_csv(url, sep="|")
print(df.head())
print("\n")


def lookup_fn(df, key_row, key_col):
    try:
        return df.iloc[key_row][key_col]

    except IndexError:
        return 0

movementlist = []
for stock in df['Symbol']:
# get history
  thestock = yf.Ticker(stock)
  hist = thestock.history(period="1d")

  # print(stock)
  low = float(10000)
  high = float(0)

  # print(thestock.info)
  for day in hist.itertuples(index=True, name='Pandas'):
    if day.Low < low:
      low = day.Low

    if high < day.High:
      high = day.High
  
  deltapercent = 100 * (high - low)/low
  Open = lookup_fn(hist, 0, "Open")

  # some error handling: 
  if len(hist >=5):
    Close = lookup_fn(hist, 4, "Close")

  else :
    Close = Open

  if(Open == 0):
    deltaprice = 0

  else:
    deltaprice = 100 * (Close - Open) / Open
  
  print(stock+"    "+str(deltapercent)+ "    "+ str(deltaprice))
  pair = [stock, deltapercent, deltaprice]
  movementlist.append(pair)

'''for entry in movementlist:
  if entry[1]>float(100):
    print(entry)'''

print(movementlist[0])




def get_top_100_movers():
    '''active_assets = api.list_assets(status='active')
    nasdaq_assets = [a for a in active_assets if a.exchange == 'NASDAQ']
    tradable_nasdaq_assets = [a for a in nasdaq_assets if a.tradable == True]
    print(tradable_nasdaq_assets)'''

#Place orders
"""buy_Order = place_order('AMZN', 20, 'buy', 'market', 'gtc')
buy_Order = place_order('FB', 200, 'buy', 'market', 'gtc')
print(buy_Order)"""

# Get orders
"""orders = get_orders()
print(orders)"""