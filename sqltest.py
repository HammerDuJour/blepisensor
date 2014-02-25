import sqlite3

connection = sqlite3.connect('/home/pi/blepimesh/data/client.db')

cursor = connection.cursor()

print "Adding Data To DB"


cursor.execute("INSERT INTO log(tagDate) values(date('now'))")
cursor.execute("INSERT INTO log  values('5',date('now'),time('now'),'34','43','TagAddr','')")

connection.commit()

print "Entire Database Contents"

for row in cursor.execute("SELECT * FROM log"):
    print row

connection.close()
