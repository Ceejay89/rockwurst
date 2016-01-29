import urllib.request
from enum import Enum
from Parser import HTMLPartsParser
import Rockwurst

# ERSETZT CURRENCY_VALUES WENNS AUTOMATISCH
MAX_CURRENCY_ID   = 24
CHAOS_CURRENCY_ID = 4
MAX_CURRENCY_COUNT_FOR_AVG = 3

TRADE_URL = "http://currency.poe.trade/search?league={}&online=x&want={}&have={}"

def getChaosValue(raw):
	parts = raw.split(" ")

	count = parts[0]
	currency = parts[1]
	
	currency_val = CURRENCYS[eval("Currency.{}".format(currency))]
	if currency_val is not None:
		return float(count) * currency_val

	return None

class Currency(Enum):
	alteration		= 1
	fusing 			= 2
	alchemy			= 3
	chaos			= 4
	gcp				= 5
	exalted			= 6
	chromatic		= 7
	jewelers		= 8
	chance			= 9
	chisel			= 10
	scouring		= 11
	blessed			= 12
	regret			= 13
	regal			= 14
	divine			= 15
	vaal			= 16
	wisdom			= 17
	portal			= 18
	armourer		= 19
	whetstone		= 20
	bauble 			= 21
	transmutty		= 22
	augmentation	= 23
	mirror			= 24
	ethernal		= 25
	
	
CURRENCYS = {
		Currency.alteration : 0.0,
		Currency.fusing		: 0.0,
		Currency.alchemy	: 0.0,
		Currency.chaos		: 1.0,
		Currency.gcp		: 0.0,
		Currency.exalted	: 0.0,
		Currency.chromatic	: 0.0,
		Currency.jewelers	: 0.0,
		Currency.chance		: 0.0,
		Currency.chisel		: 0.0,
		Currency.scouring	: 0.0,
		Currency.blessed	: 0.0,
		Currency.regret		: 0.0,
		Currency.regal		: 0.0,
		Currency.divine		: 0.0,
		Currency.vaal		: 0.0,
		Currency.wisdom		: 0.0,
		Currency.portal		: 0.0,
		Currency.bauble		: 0.0,
		Currency.armourer	: 0.0,
		Currency.whetstone	: 0.0,
		Currency.transmutty	: 0.0,
		Currency.augmentation	: 0.0,
		Currency.mirror		: 10000,
		Currency.ethernal	: 1000
}


def updateCurrencys():
	for i in range(1, MAX_CURRENCY_ID):
		if i == CHAOS_CURRENCY_ID:
			continue
		
		updateCurrency(i)
	
def updateCurrency(currencyId):
	html = getCurrencyHTML(currencyId)
	
	parser = HTMLPartsParser("div", {"class" : ["displayoffer-middle"]})
	parser.feed(html)
	
	matches = parser.matches
	
	if len(matches) > MAX_CURRENCY_COUNT_FOR_AVG:
		matches = matches[:MAX_CURRENCY_COUNT_FOR_AVG]
		
	sum = 0
	for match in matches:
		
		(to, chaos) = match.split("&lArr;")
		sum += float(chaos) / float(to)
		
	CURRENCYS[Currency(currencyId)] = sum / MAX_CURRENCY_COUNT_FOR_AVG
	
	
def getCurrencyHTML(currencyId):
	response = urllib.request.urlopen(TRADE_URL.format(Rockwurst.LEAGUE, currencyId, CHAOS_CURRENCY_ID))
	return response.read().decode("utf-8")
	
def printCurrencys():
	print("CURRENCY VALUES:")
	for curr in CURRENCYS:
		tabs =  "\t"
		if len(curr.name) < 11:
			tabs += "\t"
			if len(curr.name) < 4:
				tabs += "\t"
		print("\t[{}]  {}{} chaos".format(curr.name.upper(), tabs, round(CURRENCYS[curr]*1000)/1000))
	print("\n")