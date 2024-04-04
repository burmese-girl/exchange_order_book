import json, requests


def sort_by_price(data):
   return data['price']

def sort_by_amount(data):
   return data['amount']

def sort_by_price(data):
   return data['price']

def calculate_buying_price(buy_list):
   bid_price = 0
   bid_num_of_coin = 0
   for bid in buy_list :
      if bid_num_of_coin <=10:
         if float(bid['amount']) + bid_num_of_coin <= 10:
             bid_price+= float(bid['price'])
             bid_num_of_coin += float(bid['amount'])

   return bid_price,bid_num_of_coin

def calculate_selling_price(sell_list):
   ask_price = 0
   ask_num_of_coin = 0
   for ask in sell_list:
      if ask_num_of_coin <= 10:
         if float(ask['amount']) + ask_num_of_coin <= 10:
            ask_price += float(ask['price'])
            ask_num_of_coin += float(ask['amount'])

   return ask_price, ask_num_of_coin

# Coinbase Pro API Integration
def coinbase_pro():
   coinbase_pro_url = 'https://api.pro.coinbase.com/products/BTC-USD/book?level=2'
   headers = {}
   response = requests.get(url=coinbase_pro_url, headers=headers)
   # print("\nCoinbase_pro Status: " + str(response.status_code))
   parse = json.loads(response.text)
   bids_list = parse['bids'][0]
   asks = parse['asks'][0]
   print("bids_list => "+str(bids_list))
   print("asks => " + str(asks))
   # print("\nCoinbase Pro = > \n" + json.dumps(parse, indent=3))

# Gemini Exchange API Integration
def gemini_exchange():
   gemini_exchange_url = 'https://api.gemini.com/v1/book/BTCUSD'
   headers={}
   response = requests.get(url=gemini_exchange_url, headers=headers)
   parse = json.loads(response.text)
   # print("\nGemini Exchange Status => "+str(response.status_code))
   # print("Gemini Exchange => \n" +json.dumps(parse, indent=3))
   bids_list = parse['bids']
   asks_list = parse['asks']
   bids_list.sort(key=sort_by_price,reverse = True) # sorted by hightest price
   asks_list.sort(key=sort_by_price) # sorted by lowest price
   bid_price,bid_num_of_coin=calculate_buying_price(bids_list)
   ask_price, ask_num_of_coin = calculate_selling_price(asks_list)
   print("Buying Price => " + str(bid_price))
   print("Total Buying Coins => " + str(bid_num_of_coin))
   print("Selling Price for 10 coins => " + str(ask_price))
   print("Total Selling Coins => " + str(ask_num_of_coin))

# Kraken Exchange API Integration
def kraken_exchange():
   kraken_exchange_url = 'https://api.kraken.com/0/public/Depth?pair=XBTUSD'
   headers={}
   response = requests.get(url=kraken_exchange_url, headers=headers)
   print("\nKraken Exchange Status: " + str(response.status_code))
   parse = json.loads(response.text)
   bids_list =(parse['result']['XXBTZUSD']['bids'])
   asks_list = (parse['result']['XXBTZUSD']['asks'])
   print("\nKraken_exchange = > \n" + json.dumps(parse, indent=3))

# coinbase_pro()
gemini_exchange()
# kraken_exchange()