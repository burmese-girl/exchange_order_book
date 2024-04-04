import websocket
import json
import jwt
import time
import random
import hashlib
import base64
import os

API_KEY = 'organizations/{org_id}/apiKeys/{key_id}'
SIGNING_KEY = '-----BEGIN EC PRIVATE KEY-----\nYOUR PRIVATE KEY\n-----END EC PRIVATE KEY-----\n'

algorithm = 'ES256'

if not SIGNING_KEY or not API_KEY:
    raise ValueError('missing mandatory environment variable(s)')

CHANNEL_NAMES = {
    'level2': 'level2',
    'user': 'user',
    'tickers': 'ticker',
    'ticker_batch': 'ticker_batch',
    'status': 'status',
    'market_trades': 'market_trades',
    'candles': 'candles'
}

WS_API_URL = 'wss://advanced-trade-ws.coinbase.com'
# WS_API_URL = 'wss://ws-feed.exchange.coinbase.com'

def sign_with_jwt(message, channel, products=[]):
    jwt_payload = {
        'iss': 'coinbase-cloud',
        'nbf': int(time.time()),
        'exp': int(time.time()) + 120,
        'sub': API_KEY
    }
    jwt_token = jwt.encode(jwt_payload, SIGNING_KEY, algorithm=algorithm, headers={
        'kid': API_KEY,
        'nonce': hashlib.sha256(os.urandom(16)).hexdigest()
    })
    message['jwt'] = jwt_token
    return message

def on_message(ws, message):
    parsed_data = json.loads(message)
    print( "Result => " +json.dumps(parsed_data, indent=3))
    parsed_data =json.dumps(parsed_data, indent=3)
    with open('../python_basic/python_code_test/exchange_result.txt', 'a') as file:
        file.write(message)

def subscribe_to_products(products, channel_name, ws):
    message = {
        'type': 'subscribe',
        'channel': channel_name,
        'product_ids': products,
        'channels': [{'name': channel_name, 'product_ids': [products]}],
    }
    subscribe_msg = sign_with_jwt(message, channel_name, products)
    ws.send(json.dumps(subscribe_msg))


def unsubscribe_to_products(products, channel_name, ws):
    message = {
        'type': 'unsubscribe',
        'channel': channel_name,
        'product_ids': products
    }
    unsubscribe_msg = sign_with_jwt(message, channel_name, products)
    ws.send(json.dumps(unsubscribe_msg))

connections = []
sent_unsub = False

for i in range(1):
    date1 = int(time.time())
    ws = websocket.WebSocketApp(WS_API_URL, on_message=on_message)
    ws.on_open = lambda ws: subscribe_to_products(['BTC-USD'], CHANNEL_NAMES['level2'], ws)
    ws.run_forever()
    date2 = int(time.time())
    diff_time = abs(date2 - date1)
    if diff_time > 5000 and not sent_unsub:
        unsubscribe_to_products(['BTC-USD'], CHANNEL_NAMES['level2'], ws)
        sent_unsub = True
    connections.append(ws)

