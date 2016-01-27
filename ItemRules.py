import json

DEFAULT_RULE_FILE = "Rules/item_config.json"


class RuleParser(): 
	
	def __init__(self, rule_file=None):
		if not rule_file:
			rule_file = DEFAULT_RULE_FILE
			
		fh = open(rule_file, "r")
		
		self.rules = []
		
		for ruleInfo in json.loads(fh.read()):
			self.rules.append(Rule(ruleInfo))
			
		fh.close()
		

class Rule():
	def __init__(self, info):
		self.enabled = info["Enabled"]
		self.name	 = info["Name"]
		self.link	 = info["Link"]
		self.price	 = info["Price"]
		self.alert	 = info["Alert"]