from html.parser import HTMLParser




class HTMLPartsParser(HTMLParser):

	# Is used when there is nothing between an opening and his closing tag
	EMPTY = "<[EMPTY]>"
	
	def __init__(self, tag = "", attrs = {}):
		self.tag = tag
		self.attrs = attrs
		self.found = False
		self.matches = []
		self.start = None
		super(HTMLPartsParser, self).__init__()
		
	def reset(self):
		self.found = False
		self.matches = []
		HTMLParser.reset(self)
	
	def handle_starttag(self, tag, attrs):
		# If an match start is found, increase the depth for all incoming 
		# start tags. When start is None set the starting position to 
		# the actuall position. Incoming data will be recorded.
		if self.found:
			if self.start == None:
				self.start = self.getpos()
			self.depth += 1
			
		else:
			# Checking the right tag
			if self.tag == tag:
				# Are we looking for some attributes?
				if len(self.attrs) == 0:
					self.found = True
					self.depth = 1
					
				else:
					# If we look for some attributes check them
					for att in attrs:
						possible = self.attrs.get(att[0])
						if possible is not None:
							if att[1] in possible:
								self.found = True
								self.depth = 1
								self.start = None
							
	def handle_endtag(self, tag):
		if self.found:
			self.depth -= 1
			# If we are on the starting depth we handle the match
			if self.depth <= 0:
				self.handle_match()
				self.found = False
		
	def handle_data(self, data):
		if self.start == None:
			self.start = self.getpos()
			
	def handle_match(self):
		data = ""
		# No data between this tag
		if self.start == None:
			data = HTMLPartsParser.EMPTY
		else:
			rawdata = self.rawdata.split('\n')
			end = self.getpos()
			# i = line index of start, j = line index of end
			# m = offset of start, n = offset of end
			i, j = self.start[0]-1, end[0]-1
			m, n = self.start[1], end[1]
			# If the match is in only one line
			if i == j:
				data = rawdata[i][m:n]
			else:
				# Go through all impacting lines except the last one
				for x in range(i, j):
					data += rawdata[x][m:]
					# Set the start for following lines to offset = 0
					m=0
				# Add data from last line
				data += rawdata[j][:n]
		self.matches.append(data)
		
