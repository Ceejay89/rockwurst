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

from pygame import mixer

LEAGUE			 = "Standard"

# Die obersten MAX_HITS_FOR_AVG treffer bilden den Durchschnittswert
MAX_HITS_FOR_AVG = 5

# Multiplikator für ein Schnäpchen
PRICE_MULTIPLICATOR = 1

# Fake Angebote ausschließen, alles was unter PRICE_IGNORE_MIN und über PRICE_IGNORE_MAX liegt wird als fake angesehen
PRICE_IGNORE_MIN = 0.1
PRICE_IGNORE_MAX = 5


mixer.init()
mixer.music.load("testsound.mp3")

def handleRule(rule):
	ic = ItemCrawler()
	db_avg_cost = DB.get_avg_price(rule.link)

	Log("{} for less then {} Chaos".format(rule.name, (PRICE_MULTIPLICATOR*db_avg_cost)),"CURRENT SCAN", "blue", 0)
	
	hits = ic.hits(rule.link)
	
	if not rule.enabled:
		return
	
	isFirst = True
	hitCnt = 0
	hitSum = 0
	for hit in hits:
		
		cost = Crawler.getCostFromEntry(hit)
		if cost is None:
			continue
		ign  = Crawler.getIGNFromEntry(hit)
		(corrupted, item_name) = Crawler.getItemNameFromEntry(hit)
		
		item_print = item_name 
		
		if not item_name:
			item_name = "<NOT FOUND>"
		else:
			if corrupted:
				item_print = Fore.RED + "Corrupted" + Fore.RESET + " " + item_name
				
		chaos_cost = Currency.getChaosValue(cost)
		
		# Solange noch kein Item gefunden wurde ist db_avg_cost = 0 und db_avg_cost * PRICE_IGNORE_MIN ebenfalls. 
		# Das gleiche gilt für PRICE_IGNORE_MAX
		if not db_avg_cost:
			db_avg_cost = chaos_cost
			
		if chaos_cost < db_avg_cost * PRICE_IGNORE_MIN or chaos_cost > db_avg_cost * PRICE_IGNORE_MAX:
			Log("Someone is selling {} ({}) for {} chaos!!".format(item_print, rule.link, chaos_cost), 
				"TROLL ALERT", "red", 0)
			continue
		
		if(hitCnt < MAX_HITS_FOR_AVG):
			hitSum += chaos_cost
			hitCnt += 1
			
		
		# if chaos_cost <= rule.price and isFirst:
		if chaos_cost <= (PRICE_MULTIPLICATOR*db_avg_cost):
			Log("Schnappaaah : ", "INFO", "yellow", 0)
			Log(rule.name, "RULE", None, 1)
			Log(item_print, "ITEM", None, 1)
			Log(rule.link, "LINK", None, 1)
			Log(cost, "COST", None, 1)
			Log(chaos_cost, "CHAOS COST", None, 1)
			Log("@{} Hi, I would like to buy your {} listed for {} in {}\n".format(ign, item_name, cost, LEAGUE), "WHISPER", None, 1)
			
			if rule.alert:
				mixer.music.play()

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
		
