import Currency
import Crawler
# import winsound
import time
import datetime
from Crawler import ItemCrawler
from ItemRules import RuleParser

ALERT_FREQ = 500 #Hz
ALERT_DUR  = 2000 #ms



def handleRule(rule):
	ic = ItemCrawler()
	
	print("[CurrentScan] {} for less then {} Chaos".format(rule.name, rule.price))
	
	hits = ic.hits(rule.link)
	
	if not rule.enabled:
		return
	
	for hit in hits:
		
		cost = Crawler.getCostFromEntry(hit)
		ign  = Crawler.getIGNFromEntry(hit)
		item_name = Crawler.getItemNameFromEntry(hit)
		
		if not item_name:
			item_name = "<NOT FOUND>"
		
		chaos_cost = Currency.getChaosValue(cost)
		
		if chaos_cost <= rule.price:
			print("Schnappaaah : ")
			print("\t[Rule] {}\r\n\t[Item] {}\r\n\t[Cost] {}\r\n\t[Chaos Value] {}".format(rule.name, item_name, cost, chaos_cost))
			print("\t[Whisper] @{} Hi, I would like to buy your {} listed for {} in Talisman\n".format(ign, item_name, cost))
			
			# if rule.alert:
				# winsound.Beep(ALERT_FREQ, ALERT_DUR)
			break

def start():
	date_str = datetime.datetime.strftime(datetime.datetime.now(), '%H:%M:%S am %d.%m.%Y')
	print("SCAN STRAT --- " + date_str)
	rp = RuleParser()
	rules = rp.rules
	
	for rule in rules:
		handleRule(rule)
		
	print("SCAN FINISHED --- I'll be back ! \n\n")


if __name__ == "__main__":
	Currency.updateCurrencys()
	Currency.printCurrencys()
	while True:
		start()
		time.sleep(60)
		