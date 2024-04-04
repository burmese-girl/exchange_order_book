
import asyncio, base64, hashlib, hmac, json, os, time, websockets

API_KEY =os.environ.get("API_KEY","")
PASSPHRASE =os.environ.get("PASSPHRASE","")
SECRET_KEY = os.environ.get("SECRET_KEY","")


from dotenv import load_dotenv
load_dotenv()

# from exchange_rest import gemini_exchange,kraken_exchange


# URI = 'wss://ws-feed.exchange.coinbase.com'  # production
URI='wss://ws-feed-public.sandbox.exchange.coinbase.com'
SIGNATURE_PATH = '/users/self/verify'

channel = 'level2'
product_ids = 'ETH-BTC'
product_ids = 'USDT-USD'


async def generate_signature():
    timestamp = str(time.time())
    message = f'{timestamp}GET{SIGNATURE_PATH}'
    hmac_key = base64.b64decode(SECRET_KEY)
    signature = hmac.new(
        hmac_key,
        message.encode('utf-8'),
        digestmod=hashlib.sha256).digest()
    signature_b64 = base64.b64encode(signature).decode().rstrip('\n')
    return signature_b64, timestamp


async def websocket_listener():
    signature_b64, timestamp = await generate_signature()
    print("Singnature => " + str(signature_b64))
    subscribe_message = json.dumps({
        'type': 'subscribe',
        'channels': [channel],
        'product_ids': [product_ids],
        'signature': signature_b64,
        'key': API_KEY,
        'passphrase': PASSPHRASE,
        'timestamp': timestamp
    }, indent=3)

    print("Coinbase Request Subscribe => \n "+subscribe_message)
    print("\n " )
    while True:
        try:
            async with websockets.connect(URI, ping_interval=None) as websocket:
                await websocket.send(subscribe_message)
                while True:
                    response = await websocket.recv()
                    json_response = json.loads(response)
                    # print(json_response)
                    print("Coinbase Response Exchange => \n"+json.dumps(json_response, indent=3))

        except (websockets.exceptions.ConnectionClosedError, websockets.exceptions.ConnectionClosedOK):
            print('Connection closed, retrying..')
            await asyncio.sleep(1)



if __name__ == '__main__':
    try:
        # gemini_exchange()
        # kraken_exchange()
        asyncio.run(websocket_listener())
    except KeyboardInterrupt:
        print("Exiting WebSocket..")