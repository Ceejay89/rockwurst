import json

DEFAULT_RULE_FILE = "Rules/item_config.json"


class RuleParser(): 
	
	def __init__(self, rule_file=None):
		if not rule_file:
			rule_file = DEFAULT_RULE_FILE
			
		fh = open(rule_file, "r")
		
		self.rules = json.loads(fh.read())
		
		fh.close()
		
