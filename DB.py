import sqlite3
from ItemRules import RuleParser


def check_url_is_inserted(purl):
	connection = sqlite3.connect('example.db')
	cursor = connection.cursor()
	cursor.execute("SELECT COUNT(*) from items where url LIKE ? LIMIT 1", (purl, ))
	res = cursor.fetchone()[0]
	connection.close()
	if res == 0:
	  	return False
	else:
		return True

def insert_item(plink, pname):
	connection = sqlite3.connect('example.db')
	connection.execute("INSERT INTO items VALUES (?,?)",(plink, pname))
	connection.commit()
	print("Added: "+pname+"\nLink: "+plink)
	connection.close()

def insert_scan(purl,value):
	connection = sqlite3.connect('example.db')
	connection.execute("INSERT INTO scan (item_url,value,date) "
		+"VALUES (?,?,datetime('now'))",(purl,value))
	connection.commit()
	connection.close()

def get_avg_price(purl):
	connection = sqlite3.connect('example.db')
	cursor = connection.cursor()
	cursor.execute("SELECT COUNT(*) from scan where item_url=?",(purl,))
	exist = cursor.fetchone()[0]
	if exist >= 1:
		cursor.execute("Select AVG(value) from scan where item_url=? group by item_url",(purl,))
		res = cursor.fetchone()[0]
	else:
		res = 0
	connection.close()
	return res

def print_full_db():
	connection = sqlite3.connect('example.db')
	cursor = connection.cursor()
	cursor.execute("SELECT * from items")
	print(cursor.fetchall())
	cursor.execute("SELECT * from scan")
	print(cursor.fetchall())
	connection.close()

def delete_old_scans(pdays):
	connection = sqlite3.connect('example.db')
	connection.execute("DELETE FROM scan WHERE date <= date('now','-? day')",(pdays,))
	connection.commit()
	connection.close()

def update_items():
	connection = sqlite3.connect('example.db')
	connection.execute('''CREATE TABLE if not exists items
              (url text not null primary key, 
              name text)''')
	connection.execute('''CREATE TABLE if not exists scan
             (ID INTEGER primary key AUTOINCREMENT, 
             item_url text not null,
             value float,
             date date,
             FOREIGN KEY(item_url) REFERENCES items(url))''')
	connection.close()
	rp = RuleParser()
	rules = rp.rules
	for rule in rules:
		url_is_set = check_url_is_inserted(rule.link)
		if url_is_set == False:
			insert_item(rule.link, rule.name)
	# print_full_db()

update_items()

