# coding=utf-8
import urllib.request
import urllib.error
import http.cookiejar
import ssl
import os
import re
import sys
import time
import http.client, urllib.parse
from Parser import HTMLPartsParser

f = open("output.html", "w")
err = open("not_working.txt", "w")
COST_REX = re.compile("title=\"([0-9]+[^\"]*)")
IGN_REX  = re.compile("IGN: ([^< ]*)")



params = urllib.parse.urlencode({'bare': 'true', 'sort': 'price_in_chaos'})
headers = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8", 
			'Accept': '*/*',
			'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
			'Accept-Encoding': 'none',
			'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
			"Connection" : "keep-alive",
			"Referer": "http://poe.trade/search/aukususasahomi",
			"Host" : "poe.trade",
			"X-Requested-With" : "XMLHttpRequest",
			"Cookie" : "_ga=GA1.2.1007963689.1453324732; league=Talisman",
			"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"}
conn = http.client.HTTPConnection("poe.trade")

conn.request("POST", "/search/yatammahasinos", params, headers)
response = conn.getresponse().read().decode("utf-8", errors="ignore")

parser = HTMLPartsParser("span", {"class" : ["requirements"]})
parser.feed(response)
cnt = 0
for req in parser.matches:
	ign = re.search(IGN_REX, req)
	cost = re.search(COST_REX, req)
	
	if not ign or not cost:
		err.write(req)
	else:
		cnt+=1
		print("{} IGN : {}  cost: {}".format(cnt, ign.group(1), cost.group(1)))
	
print(cnt)
f.write("".join(parser.matches))
f.close
