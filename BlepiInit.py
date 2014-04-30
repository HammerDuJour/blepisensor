import sqlite3

connection = sqlite3.connect('/home/pi/blepisensor/SensorInfo.db')

cursor = connection.cursor()

print "Adding Data To DB"

cursor.execute("INSERT INTO SensorTags values('1','BC:6A:29:AB:D5:92','TAG 1')")
cursor.execute("INSERT INTO SensorTags values('2','BC:6A:29:AB:23:DA','TAG 2')")
cursor.execute("INSERT INTO SensorTags values('3','BC:6A:29:AB:3B:4B','TAG 3')")
cursor.execute("INSERT INTO SensorTags values('4','BC:6A:29:AB:23:F6','TAG 4')")

connection.commit()

print "Entire Database Contents"

for row in cursor.execute("SELECT * FROM SensorTags"):
    print row

connection.close()
