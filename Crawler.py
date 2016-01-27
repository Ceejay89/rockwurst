# coding=utf-8
import http.client, urllib.parse
import re
from Parser import HTMLPartsParser

COST_REX = re.compile("title=\"([0-9]+[^\"]*)")
IGN_REX  = re.compile("IGN: ([^< ]*)")
NAME_REX = re.compile("view-thread\/[0-9]*[^>]*> *([^< ]*)")


def getRegexFromEntry(rex, entry):
	return re.search(rex, entry).group(1)

def getCostFromEntry(entry):
	return getRegexFromEntry(COST_REX, entry)

def getIGNFromEntry(entry):
	return getRegexFromEntry(IGN_REX, entry)

def getItemNameFromEntry(entry):
	return getRegexFromEntry(NAME_REX, entry)
	
class ItemCrawler():

	def __init__(self):
		self.params = urllib.parse.urlencode({'bare': 'true', 'sort': 'price_in_chaos'})
		self.headers = {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8", 
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
		self.conn = http.client.HTTPConnection("poe.trade")
	
	def hits(self, url):
		self.conn.request("POST", "/search/" + url, self.params, self.headers)
		response = self.conn.getresponse().read().decode("utf-8", errors="ignore")

		parser = HTMLPartsParser("tr", {"class" : ["first-line"]})
		parser.feed(response)
		
		
		return parser.matches
	
	def close(self):
		self.conn.close()
		
		
"""
ic = ItemCrawler()
matches = ic.requests("okainhiritigor")

for match in matches:
	print("IGN --> " + getIGNFromEntry(match) + " Cost --> " +  getCostFromEntry(match))

matches = ic.requests("atokaronariria")

for match in matches:
	print("IGN --> " + getIGNFromEntry(match) + " Cost --> " +  getCostFromEntry(match))
"""