from datetime import datetime, timedelta
from time import sleep
import requests
import json
from flask import Flask

app = Flask(__name__)
fmat = '%Y-%m-%dT%H:%M:%S.%fZ'

@app.route("/")
def index():
    url = "https://api.hitbtc.com/api/3/public/trades?limit=1000&by=timestamp&sort=DESC"
    end = (datetime.now() - timedelta(hours=2)).strftime(fmat)
    start = (datetime.now() - timedelta(hours=2, minutes=15)).strftime(fmat)
    url = url + '&from=' + start + '&till=' + end
    print(url)
    s = ''
    r = requests.get(url).content
    s += url
    tradenum = 100
    threshold = 0
    timeframe = 15
    printer = ('Parameters:<br>'
               + 'Trades: ' + str(tradenum) + ' Index Threshold > ' + str(threshold))
    print(printer)
    s += '<br>' + printer
    j = json.loads(r)
    counter = 0
    for i in j:
        a = j[i]
        tradecounter = float(0)
        volume = 0
        buy = 0
        sell = 0
        buycounter = 0
        sellcounter = 0
        sellwidth = 0
        buywidth = 0
        for m in a:
            # process timestamp
            t = m['timestamp']
            d = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
            now = datetime.today()
            diff = now - d
            # difference to be in the last 15 minutes
            # print('Diff is ' + str(diff - timedelta(hours=2)))
            if diff - timedelta(hours=2, minutes=15) < timedelta(minutes=15):
                tradecounter = tradecounter + 1
                # process volume
                price = m['price']
                # print(price)
                qty = m['qty']
                # print(qty)
                volume += float(price)*float(qty)
                # print(volume)
                side = m['side']
                if side == 'buy':
                    buy += float(price)
                    buycounter += 1
                elif side == 'sell':
                    sell += float(price)
                    sellcounter += 1
                if buycounter != 0:
                    buywidth = float(buy / buycounter)
                if sellcounter != 0:
                    sellwidth = float(sell / sellcounter)
        if tradecounter > tradenum and ((sellwidth - buywidth) * volume) > threshold:
            s += ('<br><br>'
                  + '<b>' + i + '</b>'
                  + '<br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Trades:</i>' + str(tradecounter)
                  + '<br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Volume</i>: ' + str(volume)
                  + '<br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Buy</i>: ' + str(buywidth)
                  + '<br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Sell</i>: ' + str(sellwidth)
                  + '<br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Width</i>: ' + str(sellwidth - buywidth)
                  + '<br>&nbsp;&nbsp;&nbsp;&nbsp;<i>Index</i>: ' + str((sellwidth - buywidth) * volume)
                  )
    return s

# checke jede 5 mins https://api.hitbtc.com/#trades auf
# width>1.5 und volume >120 und trades >200 in den letzten 15 minuten
if __name__ == '__main__':
    app.run()

