import hashlib
import hmac
import json
import urllib

from websocket import create_connection


class BitmexWS:
    BITMEX_URL = "wss://testnet.bitmex.com"
    VERB = "GET"
    ENDPOINT = "/realtime"

    def __init__(self):
        self.ws = create_connection(self.BITMEX_URL + self.ENDPOINT)

    def subscribe_topic(self, topic_name):
        request = {"op": "subscribe", "args": topic_name}
        self.ws.send(json.dumps(request))

    def receive(self):
        result = self.ws.recv()
        result_json = json.loads(result)
        try:
            result = {
                'price': result_json['data'][0]['lastPrice'],
                'symbol': result_json['data'][0]['symbol'],
                'timestamp': result_json['data'][0]['timestamp']
            }
            return result
        except KeyError:
            return None

    def bitmex_signature(apiSecret, verb, url, nonce, postdict=None):
        """Given an API Secret key and data, create a BitMEX-compatible signature."""
        data = ''
        if postdict:
            # separators remove spaces from json
            # BitMEX expects signatures from JSON built without spaces
            data = json.dumps(postdict, separators=(',', ':'))
        parsedURL = urllib.parse.urlparse(url)
        path = parsedURL.path
        if parsedURL.query:
            path = path + '?' + parsedURL.query
        message = (verb + path + str(nonce) + data).encode('utf-8')
        signature = hmac.new(apiSecret.encode('utf-8'), message, digestmod=hashlib.sha256).hexdigest()
        print("Signature: %s" % signature)
        return signature
