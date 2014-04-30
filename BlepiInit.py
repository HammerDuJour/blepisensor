import sqlite3

connection = sqlite3.connect('/home/pi/blepisensor/SensorInfo.db')

cursor = connection.cursor()

print "Adding Data To DB"

cursor.execute("CREATE TABLE SensorTags(Id INT, Address TEXT, Description TEXT)")
cursor.execute("INSERT INTO SensorTags(1,'BC:6A:29:AB:D5:92','TAG 1')")

connection.commit()

print "Entire Database Contents"

for row in cursor.execute("SELECT * FROM log"):
    print row

connection.close()
