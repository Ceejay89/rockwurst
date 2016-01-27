
CURRENCY_VALUES = { "alteration"	:	0.0781,
					"fusing"		: 	0.62,
					"alchemy"		:	0.3548,
					"chaos"			:	1,
					"gcp"			:	1.5,
					"exalted"		:	83,
					"chromatic"		:	0.0664,
					"divine"		:	19,
					"chisel"		:	0.4762}
					
					
def getChaosValue(raw):
	parts = raw.split(" ")
	
	count = parts[0]
	currency = parts[1]
	
	currency_val = CURRENCY_VALUES[currency]
	
	if currency_val:
		return float(count) * currency_val
		
	return None

