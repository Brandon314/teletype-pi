import sqlite3
import teletype
import time
import webiopi
import tprint

conn = sqlite3.connect('tweepytest.db')
print("Opened database successfully")



# loop this to parse dbase, grab the deets, cleanup dbase, print to teletype, start over
while True:
   cursor = conn.execute("SELECT txt, author, created, source, id  from TWEETS")
   #for row in cursor:
   row = cursor.fetchone()
   if row:
      print("txt = ", row[0])
      t = row[0] #stores tweet text for printing
      print("author = ", row[1])
      print("created = ", row[2])
      print("source = ", row[3])
      print("id = ", row[4])
      tid = row[4] #stores tweet ID for deletion purposes
      print(type(tid))
      print("Successfully acquired data from d-base")
      conn.execute("DELETE from TWEETS where id=?", (tid,)) #we got what we wanted, time to say goodbye
      print("deleted tweet with ID = ", tid)
      conn.commit() #save our changes to dbase
      tprint.tty_tx_str(t) #send string to app for printing to tty
      
   else:
      print("database empty")
      time.sleep(5)

   #conn.close()

  
