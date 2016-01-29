
from colorama import Fore, Back, Style, init

init()


def Log(msg, info, info_color, lvl):
	if info_color:
		color = eval("Fore.{}".format(info_color.upper()))
	else:
		color = ""
		
	offset = ""
	
	for i in range(lvl):
		offset += "\t"
		
	print("{}[{}{}{}] {}".format(offset, color, info, Fore.RESET, msg))

	
