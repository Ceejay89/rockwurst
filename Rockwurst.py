import Currency
import Crawler
import os
import time
import datetime
import DB
from Printer import Log
from Crawler import ItemCrawler
from ItemRules import RuleParser
from colorama import Fore, Back

LEAGUE			 = "Talisman"
MAX_HITS_FOR_AVG = 10

def handleRule(rule):
	ic = ItemCrawler()
	
	Log("{} for less then {} Chaos".format(rule.name, rule.price),"CURRENT SCAN", "blue", 0)
	
	hits = ic.hits(rule.link)
	
	if not rule.enabled:
		return
	
	isFirst = True
	hitCnt = 0
	hitSum = 0
	for hit in hits:
		
		cost = Crawler.getCostFromEntry(hit)
		ign  = Crawler.getIGNFromEntry(hit)
		(corrupted, item_name) = Crawler.getItemNameFromEntry(hit)
		
		item_print = item_name 
		
		if not item_name:
			item_name = "<NOT FOUND>"
		else:
			if corrupted:
				item_print = Fore.RED + "Corrupted" + Fore.RESET + " " + item_name
				
		chaos_cost = Currency.getChaosValue(cost)
		if(hitCnt < MAX_HITS_FOR_AVG):
			hitSum += chaos_cost
			hitCnt += 1
			
		
		if chaos_cost <= rule.price and isFirst:
			Log("Schnappaaah : ", "INFO", "yellow", 0)
			Log(rule.name, "RULE", None, 1)
			Log(item_print, "ITEM", None, 1)
			Log(rule.link, "LINK", None, 1)
			Log(cost, "COST", None, 1)
			Log(chaos_cost, "CHAOS COST", None, 1)
			Log("@{} Hi, I would like to buy your {} listed for {} in {}\n".format(ign, item_name, cost, LEAGUE), "WHISPER", None, 1)
			
			if rule.alert:
				os.system("start C:\\Users\\Ramon\\workspace\\git\\rockwurst\\testsound.mp3")

			isFirst = False
	if len(hits) > 0:
		hitAvg = hitSum / hitCnt
		Log("took the first {} items with an avarage of {} chaos".format(hitCnt, hitAvg), "SCAN RESULT", "white", 0)
		DB.insert_scan(rule.link, hitAvg)

def start():
	date_str = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S am %d.%m.%Y')
	Log("Scan start", "INFO", "yellow", 0)
	rp = RuleParser()
	rules = rp.rules
	
	for rule in rules:
		handleRule(rule)
	
	Log("Scan finished --- I'll be back ! \n\n", "INFO", "yellow", 0)


if __name__ == "__main__":
	Currency.updateCurrencys()
	Currency.printCurrencys()
	while True:
		start()
		time.sleep(180)
		