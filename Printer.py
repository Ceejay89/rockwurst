
from colorama import Fore, Back, Style, init

init()


def Log(msg, info, info_color = None, lvl = 0):
	if info_color:
		color = eval("Fore.{}".format(info_color.upper()))
	else:
		color = Fore.GREEN
		
	offset = ""
	
	for i in range(lvl):
		offset += "\t"
		
	print("{}[{}{}{}] {}".format(offset, color, info, Fore.RESET, msg))

	
