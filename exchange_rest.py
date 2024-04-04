
import json, hmac, hashlib, time, requests, base64, os, sys
from urllib.parse import urlparse


API_KEY =""
PASSPHRASE =""
SECRET_KEY = ""

def coinbase_exchange():
   product_id='USDT-USD'
   query_id = '&product_id=' + product_id
   url = f'https://api-public.sandbox.exchange.coinbase.com/orders?limit=100'
   timestamp = str(int(time.time()))
   method = 'GET'
   url_path = f'{urlparse(url).path}?{urlparse(url).query}'

   message = timestamp + method + url_path
   hmac_key = base64.b64decode(SECRET_KEY)
   signature = hmac.digest(hmac_key, message.encode('utf-8'), hashlib.sha256)
   signature_b64 = base64.b64encode(signature)

   headers = {
      'CB-ACCESS-SIGN': signature_b64,
      'CB-ACCESS-TIMESTAMP': timestamp,
      'CB-ACCESS-KEY': API_KEY,
      'CB-ACCESS-PASSPHRASE': PASSPHRASE,
      'Accept': 'application/json'
   }

   response = requests.get(url, headers=headers)
   print("Coinbase_exchange => "+str(response.status_code))
   parse = json.loads(response.text)
   print("Coinbase_exchange Result => "+json.dumps(parse, indent=3))


def coinbase_pro():
   coinbase_pro_url = 'https://api.pro.coinbase.com/products/BTC-USD/book?level=2'
   headers = {}
   response = requests.get(url=coinbase_pro_url, headers=headers)
   print("\n\n\nCoinbase_pro Status: " + str(response.status_code))
   parse = json.loads(response.text)
   bids_list = parse['bids']
   asks = parse['asks']
   print("\nCoinbase Pro = > \n" + json.dumps(parse, indent=3))

def gemini_exchange():
   gemini_exchange_url = 'https://api.gemini.com/v1/book/BTCUSD'
   headers={}
   response = requests.get(url=gemini_exchange_url, headers=headers)
   print("Gemini Exchange Status => "+str(response.status_code))
   parse = json.loads(response.text)
   bids_list = parse['bids']
   asks = parse['asks']
   print("Gemini Exchange => \n" +json.dumps(parse, indent=3))

def kraken_exchange():
   kraken_exchange_url = 'https://api.kraken.com/0/public/Depth?pair=XBTUSD'
   headers={}
   response = requests.get(url=kraken_exchange_url, headers=headers)
   print("\n\n\nKraken Exchange Status: " + str(response.status_code))
   parse = json.loads(response.text)
   bids_list =(parse['result']['XXBTZUSD']['bids'])
   asks_list = (parse['result']['XXBTZUSD']['asks'])
   print("\nKraken_exchange = > \n" + json.dumps(parse, indent=3))


coinbase_exchange()
coinbase_pro()
gemini_exchange()
kraken_exchange()

