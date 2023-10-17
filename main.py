#!/usr/bin/python3

import json
from datetime import datetime, timedelta
import urllib.request

print("Content-type: text/html")
print("")
print("<html><head><title>HitBTC Trades API</title></head>")
print("<body>")

fmat = '%Y-%m-%dT%H:%M:%S.%fZ'
url = "https://api.hitbtc.com/api/3/public/trades?limit=1000&by=timestamp&sort=DESC"

end = (datetime.now() - timedelta(hours=2)).strftime(fmat)
start = (datetime.now() - timedelta(hours=2, minutes=60)).strftime(fmat)
url = url + '&from=' + start + '&till=' + end
print("Source URL for processing is <a target=_blank href='" + url + "'>" + url + "</a><br>")
print("timestamp is GMT<br>")

res = urllib.request.urlopen(url)
res_body = res.read()

tradenum = 250
print("trade number threshold is 250 during the last hour (except CHSB/AVAX/TRX/REEF)<br>")
threshold = 0.0

print("index calculation is abs((sellwidth - buywidth) * volume)")

j = json.loads(res_body)

restable = ('<table>' +
	'<tr>' +
	'<th><b>Currency</b></th>' +
	'<th><b>Trades</b></th>' +
	'<th><b>Buys</b></th>' +
	'<th><b>Sells</b></th>' +
	'<th><b>Price</b></th>' +
	'<th><b>Quantity</b></th>' +
	'<th><b>Volume</b></th>' +
	'<th><b>Buy Width</b></th>' +
	'<th><b>Sell Width</b></th>' +
	'<th><b>Width Average</b></th>' +
	'<th><b>Index</b></th>' +
	'</tr>'
	)

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
	averageprice = 0
	counter = 0
	quantity = 0
	p = 0
	for m in a:
		counter += 1
		# process timestamp
		t = m['timestamp']
		d = datetime.strptime(t, '%Y-%m-%dT%H:%M:%S.%fZ')
		now = datetime.today()
		diff = now - d
		# difference to be in the last 10 minutes
		# print('Diff is ' + str(diff - timedelta(hours=2)))
		# if diff - timedelta(hours=2, minutes=10) < timedelta(minutes=10):
		tradecounter = tradecounter + 1
		# process volume
		p = m['price']
		averageprice += float(p)
		# print(price)
		qty = m['qty']
		quantity += float(qty)
		# print(qty)
		volume += (float(p) * float(qty))
		# print(volume)
		side = m['side']
		if side == 'buy':
			buy += float(p)
			buycounter += 1
		elif side == 'sell':
			sell += float(p)
			sellcounter += 1
		if buycounter != 0:
			buywidth = float(buy / buycounter)
		if sellcounter != 0:
			sellwidth = float(sell / sellcounter)
	if counter != 0:
		averageprice = averageprice / float(counter)
	index = abs((sellwidth - buywidth) * volume)
	volume = float(averageprice) * float(quantity)
	# res = ('<br><br>'
	#	+ '<b>' + i + '</b>'
	#	+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Trades</i>: ' + str(tradecounter)
	#	+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Buys</i>: ' + str(buycounter)
	#	+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Sells</i>: ' + str(sellcounter)
	#	+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Volume</i>: ' + str("%.2f" % volume)
	#	+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Buy Width</i>: ' + str("%.2f" % buywidth)
	#	+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Sell Width</i>: ' + str("%.2f" % sellwidth)
	#	+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Width Average</i>: ' + str("%.2f" % abs(sellwidth + buywidth)/2)
	#	+ '<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>Index</i>: ' + str("%.6f" % index))
	# res = '<br><br>'
	bool = 0
	if tradecounter > tradenum and index > threshold:
		if not i.endswith('PERP'):
			bool=1
	elif (
		i.endswith('TRXUSDT')
		or i.endswith('XTZUSDT')
		or i.endswith('REEFUSDT')
		or i.endswith('CHSBBTC')
		or i.endswith('AVAXUSDT')):
		bool = 1
	if bool==1:
		restable  += ('<tr>'
			+ '<td align="left">' + i + '</td>'
			+ '<td align="right">' + str(tradecounter) + '</td>'
			+ '<td align="right">' + str(buycounter) + '</td>'
			+ '<td align="right">' + str(sellcounter) + '</td>'
			+ '<td align="right">' + str("%.8f" % averageprice) + '</td>'
			+ '<td align="right">' + str("%.2f" % quantity) + '</td>'
			+ '<td align="right">' + str("%.2f" % volume) + '</td>'
			+ '<td align="right">' + str("%.2f" % buywidth) + '</td>'
			+ '<td align="right">' + str("%.2f" % sellwidth) + '</td>'
			+ '<td align="right">' + str("%.2f" % (abs(sellwidth + buywidth)/2)) + '</td>'
			+ '<td align="right">' + str("%.2f" % index) + '</td>'
			+ '</tr>'
			)
restable  += '</table>'
print('<br><br>'+restable)
print("</body>")
print("</html>")
