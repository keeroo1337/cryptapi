from datetime import datetime, timedelta
from time import sleep
import requests
import json

# checke jede 5 mins https://api.hitbtc.com/#trades auf
# width>1.5 und volume >120 und trades >200 in den letzten 15 minuten



if __name__ == '__main__':
    fmat = '%Y-%m-%dT%H:%M:%S.%fZ'
    while True:
        print('start')
        url = "https://api.hitbtc.com/api/3/public/trades?limit=1000&by=timestamp&sort=DESC"
        end = (datetime.now() - timedelta(hours=2)).strftime(fmat)
        start = (datetime.now() - timedelta(hours=2, minutes=15)).strftime(fmat)
        url = url + '&from=' + start + '&till=' + end
        r = requests.get(url).content
        print(url)
        # print(r)
        j = json.loads(r)
        for i in j:
            a = j[i]
            tradecounter = float(0)
            counter = 0
            volume = 0
            buy = 0
            sell = 0
            buycounter = 0
            sellcounter = 0
            sellwidth = 0
            buywidth = 0
            for m in a:
                counter = counter + 1
                # process timestamp
                t = m['timestamp']
                d = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
                now = datetime.today()
                diff = now - d
                # difference to be in the last 15 minutes
                #print (str(diff - timedelta(hours=2)))
                if diff - timedelta(hours=2, minutes=15) < timedelta(minutes=15):
                    tradecounter = tradecounter + 1

                # process volume
                price = m['price']
                #print(price)
                qty = m['qty']
                #print(qty)
                volume += float(price)*float(qty)
                #print(volume)

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

            if tradecounter > 100 and ((sellwidth - buywidth) * volume) > 0:
                print(i
                      + '\tTrades: ' + str(tradecounter)
                      + '\tVolume: ' + str(volume)
                      + '\tBuy: ' + str(buywidth)
                      + '\tSell: ' + str(sellwidth)
                      + '\tWidth: ' + str(sellwidth - buywidth)
                      + '\tIndex: ' + str((sellwidth - buywidth) * volume)
                      )
        print('end')
        sleep(5)
