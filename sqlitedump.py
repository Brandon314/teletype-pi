import sqlite3

conn = sqlite3.connect('tweepytest.db')
print("Opened database successfully")

cursor = conn.execute("SELECT txt, author, created, source, id  from TWEETS")
for row in cursor:
   print("txt = ", row[0])
   print("author = ", row[1])
   print("created = ", row[2])
   print("source = ", row[3])
   print("id = ", row[4])
print("SUCCESS")
conn.close()
