#!/usr/bin/python3

import hashlib
import hmac
import json
import time
from datetime import datetime, timedelta
import urllib.request

print("Content-type: text/html")
print("")
print("<html><head><title>Bitvavo Trades API</title></head>")
print("<body>")


class BitvavoRestClient:
    """
    A class to interact with the Bitvavo REST API.
    """
    def __init__(self, api_key: str, api_secret: str, access_window: int = 10000):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_window = access_window
        self.base = 'https://api.bitvavo.com/v2'

    def place_order(self, market: str, side: str, order_type: str, body: dict):
        """
        Send an instruction to Bitvavo to buy or sell a quantity of digital assets at a specific price.
        :param market: the market to place the order for. For example, `BTC-EUR`.
        :param side: either 'buy' or 'sell' in `market`.
        :param order_type: the character of the order. For example, a `stopLoss` order type is an instruction to
                           buy or sell a digital asset in `market` when it reaches the price set in `body`.
        :param body: the parameters for the call. For example, {'amount': '0.1', 'price': '2000'}.
        """
        body['market'] = market
        body['side'] = side
        body['orderType'] = order_type
        return self.private_request(method='POST', endpoint='/order', body=body)

    def private_request(self, endpoint: str, body: dict | None = None, method: str = 'GET'):
        """
        Create the headers to authenticate your request, then make the call to Bitvavo API.
        :param endpoint: the endpoint you are calling. For example, `/order`.
        :param body: for GET requests, this can be an empty string. For all other methods, a string
                     representation of the call body.
        :param method: the HTTP method of the request.
        """
        now = int(time.time() * 1000)
        sig = self.create_signature(now, method, endpoint, body)
        url = self.base + endpoint
        headers = {
            'bitvavo-access-key': self.api_key,
            'bitvavo-access-signature': sig,
            'bitvavo-access-timestamp': str(now),
            'bitvavo-access-window': str(self.access_window),
        }
        req = urllib.request.Request(url, method=method)
        req.add_header(key='bitvavo-access-key', val=self.api_key)
        req.add_header(key='bitvavo-access-signature', val=sig)
        req.add_header(key='bitvavo-access-timestamp', val=str(now))
        req.add_header(key='bitvavo-access-window', val=str(self.access_window))  
        ur = urllib.request.urlopen(req)
        data = ur.read()
        encoding = ur.info().get_content_charset('utf-8')
        jay = json.loads(data.decode(encoding))
        # r =  urllib.request.urlopen(method=method, url=url, headers=headers, json=body)
        return jay

    def create_signature(self, timestamp: int, method: str, url: str, body: dict | None):
        """
        Create a hashed code to authenticate requests to Bitvavo API.
        :param timestamp: a unix timestamp showing the current time.
        :param method: the HTTP method of the request.
        :param url: the endpoint you are calling. For example, `/order`.
        :param body: for GET requests, this can be an empty string. For all other methods, a string
                     representation of the call body. For example, for a call to `/order`:
                     `{"market":"BTC-EUR","side":"buy","price":"5000","amount":"1.23", "orderType":"limit"}`.
        """
        string = str(timestamp) + method + '/v2' + url
        #print(string)
        if (body is not None) and (len(body.keys()) != 0):
            string += json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.api_secret.encode('utf-8'), string.encode('utf-8'), hashlib.sha256).hexdigest()
        return signature
    
    def get_ticker(self, market: str, body: dict):
        """
        Send an instruction to Bitvavo to buy or sell a quantity of digital assets at a specific price.
        :param market: the market to place the order for. For example, `BTC-EUR`.
        :param side: either 'buy' or 'sell' in `market`.
        :param order_type: the character of the order. For example, a `stopLoss` order type is an instruction to
                           buy or sell a digital asset in `market` when it reaches the price set in `body`.
        :param body: the parameters for the call. For example, {'amount': '0.1', 'price': '2000'}.
        """

        return self.private_request(method='GET', endpoint='/ticker/24h', body=body)
    
class Util:
    def convert_timestamp(self, unixtimestamp: str):
        utc_time = ""
        if unixtimestamp is not None and unixtimestamp != "":
            # fmat = '%Y-%m-%dT%H:%M:%S.%fZ'
            fmat = '%Y-%m-%d %H:%M:%S'
            delta = 60*60*2
            curtime = float(unixtimestamp) - delta
            #print(time.time())
            #print(unixtimestamp)
            d = datetime.fromtimestamp(timestamp=time.time())
            #print(d)
            utc_time = (d).strftime(fmat)
        return utc_time
    
key=""
secret=""
with open(".secret") as file:
    linecounter = 0
    for line in file:
        if linecounter == 0:
            key = line.strip()
        elif linecounter == 1:
            secret = line.strip()
        linecounter += 1

print(key)
                    
brc = BitvavoRestClient(api_key=key, api_secret=secret)
util = Util()

r = brc.get_ticker(market="25", body = {})

restableheader = (	'<thead><tr>' +
'<th><b>market</b></th>' +
'<th><b>Width</b></th>' +
'<th><b>startTimestamp</b></th>' +
'<th><b>timestamp</b></th>' +
'<th><b>open</b></th>' +
'<th><b>openTimestamp</b></th>' +
'<th><b>high</b></th>' +
'<th><b>low</b></th>' +
'<th><b>last</b></th>' +
'<th><b>closeTimestamp</b></th>' +
'<th><b>bid</b></th>' +
'<th><b>bidSize</b></th>' +
'<th><b>ask</b></th>' +
'<th><b>askSize</b></th>' +
'<th><b>volume</b></th>' +
'<th><b>volumeQuote</b></th>' +    
'</tr></thead><tbody>'
)

restable_Bitvavo = ('<table id="tableBitvavo" class="tablesorter">' + restableheader)

for i in r:
    market = i["market"]

    if i.get("startTimestamp", -1) != -1:
        startTimestamp = i["startTimestamp"]
    else:
        startTimestamp = ""

    timestamp = i["timestamp"]
    open = i["open"]

    if i.get("openTimestamp", -1) != -1:
        openTimestamp = i["openTimestamp"]
    else:
        openTimestamp = ""

    high = i["high"]
    low = i["low"]

    if i.get("last", -1) != -1:
        last = i["last"]
    else:
        last = ""  

    if i.get("closeTimestamp", -1) != -1:
        closeTimestamp = i["closeTimestamp"]
    else:
        closeTimestamp = ""   

    if i.get("bid", -1) != -1 and i.get("bid", -1) is not None:
        bid = i["bid"]
    else:
        bid = 0 
    

    bidSize = i["bidSize"]

    if i.get("ask", -1) != -1 and i.get("ask", -1) is not None:
        ask = i["ask"]
    else:
        ask = 0   
    
    
    askSize = i["askSize"]
    volume = i["volume"]
    volumeQuote = i["volumeQuote"]

    width = float(ask) - float(bid)

    restable = ('<tr>'
		+ '<td align="left">' + market + '</td>'
        + '<td align="right">' + str(width) + '</td>'
		+ '<td align="right">' + str(util.convert_timestamp(startTimestamp)) + '</td>'
		+ '<td align="right">' + str(util.convert_timestamp(timestamp)) + '</td>'
		+ '<td align="right">' + str(open) + '</td>'
		+ '<td align="right">' + str(util.convert_timestamp(openTimestamp)) + '</td>'
		+ '<td align="right">' + str(high) + '</td>'
		+ '<td align="right">' + str(low) + '</td>'
		+ '<td align="right">' + str(last) + '</td>'
		+ '<td align="right">' + str(util.convert_timestamp(closeTimestamp)) + '</td>'
		+ '<td align="right">' + str(bid) + '</td>'
		+ '<td align="right">' + str(bidSize) + '</td>'
	    + '<td align="right">' + str(ask) + '</td>'
		+ '<td align="right">' + str(askSize) + '</td>'
		+ '<td align="right">' + str(volume) + '</td>'
		+ '<td align="right">' + str(volumeQuote) + '</td>'            
		+ '</tr>'
		)

    restable_Bitvavo += restable

restable_Bitvavo += '</tbody></table>'

print('<br><br>'+restable_Bitvavo)
print("</body>")
print("</html>")
