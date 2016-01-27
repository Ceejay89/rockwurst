import Currency
import Crawler
from Crawler import ItemCrawler
from ItemRules import RuleParser



def handleRule(rule):
	ic = ItemCrawler()
	hits = ic.hits(rule["Link"])
	
	for hit in hits:
		
		cost = Crawler.getCostFromEntry(hit)
		ign  = Crawler.getIGNFromEntry(hit)
		item_name = Crawler.getItemNameFromEntry(hit)
		
		if not item_name:
			item_name = "<NOT FOUND>"
		
		chaos_cost = Currency.getChaosValue(cost)
		
		if chaos_cost < rule["Price"]:
			print("Schnappaaah : ")
			print("\t[Rule] {}\r\n\t[Item] {}\r\n\t[Cost] {}\r\n\t[Chaos Value] {}".format(rule["Name"], item_name, cost, chaos_cost))
			print("\t[Whisper] @{} Hi, I would like to buy your {} listed for {} in Talisman".format(ign, item_name, cost))
			break

def start():

	rp = RuleParser()
	rules = rp.rules
	
	for rule in rules:
		handleRule(rule)


if __name__ == "__main__":
	start()