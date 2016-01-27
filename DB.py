import sqlite3
connection = sqlite3.connect('example.db')
connection.execute('DROP TABLE items')
connection.execute('''CREATE TABLE items
             (url text not null primary key, 
             name text)''')
connection.execute('DROP TABLE scan')
connection.execute('''CREATE TABLE scan
             (ID INTEGER primary key AUTOINCREMENT, 
             item_url text not null,
             value float,
             date date,
             FOREIGN KEY(item_url) REFERENCES items(url))''')

connection.execute("INSERT INTO items VALUES ('http://poe.trade/search/omobodosaonigu','test')")
# connection.execute("INSERT INTO scan (ID, item_url, value, date) VALUES (0,'http://poe.trade/search/omobodosaonigut', 3.56, '2016-01-03')")
connection.execute("INSERT INTO scan (item_url, value, date) VALUES ('http://poe.trade/search/omobodosaoniguz', 3.56, '2016-01-03')")
connection.execute("INSERT INTO scan (ID, item_url, value, date) VALUES (1, 'http://poe.trade/search/omobodosaoniguz', 3.56, '2016-01-03')")
connection.commit()
# Insert a row of data
# database.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# Save (commit) the changes
cursor = connection.cursor()
cursor.execute("SELECT * FROM items")
res = cursor.fetchone()
print (res)
cursor.execute("SELECT * from scan")
print (cursor.fetchall())
connection.close()