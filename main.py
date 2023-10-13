#!/usr/bin/python3

import json
from datetime import datetime, timedelta
import urllib.request

print("Content-type: text/html")
print("")
print("<html><head><title>CGI</title></head>")
print("<body>")

fmat = '%Y-%m-%dT%H:%M:%S.%fZ'
url = "https://api.hitbtc.com/api/3/public/trades?limit=1000&by=timestamp&sort=DESC"

end = (datetime.now() - timedelta(hours=2)).strftime(fmat)
start = (datetime.now() - timedelta(hours=2, minutes=15)).strftime(fmat)
url = url + '&from=' + start + '&till=' + end
print("<a target=_blank href='" + url + "'>" + url + "</a><br>")
res = urllib.request.urlopen(url)
res_body = res.read()

tradenum = 100
threshold = 0.1

j = json.loads(res_body)

for i in j:
	a = j[i]
	tradecounter = 0
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
		volume += float(price) * float(qty)
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
	index = abs((sellwidth - buywidth) * volume)
	res = ('<br><br>'
		+ '<b>' + i + '</b>'
		+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Trades</i>: ' + str(tradecounter)
		+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Buys</i>: ' + str(buycounter)
		+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Sells</i>: ' + str(sellcounter)
		+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Volume</i>: ' + str(volume)
		+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Buy Width</i>: ' + str(buywidth)
		+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Sell Width</i>: ' + str(sellwidth)
		+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Width Average</i>: ' + str(abs(sellwidth - buywidth))
		+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Index</i>: ' + str(index))
	if tradecounter > tradenum and index > threshold:
		if not i.endswith('PERP'):
			print(res)
	elif i.endswith('TRXUSDT') or i.endswith('REEFUSDT') or i.endswith('CHSBBTC') or i.endswith('AVAXUSDT'):
		print(res)


print("</body>")
print("</html>")