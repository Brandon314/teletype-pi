from teletype import txbaudot
from threading import Thread

def teletype_tx(data):
   txbaudot(data)

baudot = '10101'


thread = Thread(target = teletype_tx, args = (baudot, ))
thread.start()
print("Finished")
