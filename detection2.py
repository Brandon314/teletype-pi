import RPi.GPIO as GPIO
import time
import os
from teletype import tx_ctl
from teletype import tx_ascii_chr
from teletype import txbaudot
#from threading import Thread
from multiprocessing import Pool


#sets up the asyncronous process(es)
if __name__ == '__main__':
    pool = Pool(processes=1) 


GPIO.setmode(GPIO.BOARD) #sets GPIO numbering system to BOARD pin numbers versus BCM numbering

key = 3

GPIO.setup(key, GPIO.IN)

#print(GPIO.input(key))
print(1 - GPIO.input(key))
#b = (1 - GPIO.input(key))
#print(b)

GPIO.add_event_detect(key, GPIO.RISING, bouncetime=130) #add rising edge detection on GPIO 23

a = []
d = 0.020
e = 0.030
s = 0 #ltrs mode by default
tx_ctl('ltrs') #sent printer to letters mode on start

#lookup dictionary for ltrs
asciiltrs_to_binstr = {
  'A'  : '00011',
  'B'  : '11001',
  'C'  : '01110',
  'D'  : '01001',
  'E'  : '00001',
  'F'  : '01101',
  'G'  : '11010',
  'H'  : '10100',
  'I'  : '00110',
  'J'  : '01011',
  'K'  : '01111',
  'L'  : '10010',
  'M'  : '11100',
  'N'  : '01100',
  'O'  : '11000',
  'P'  : '10110',
  'Q'  : '10111',
  'R'  : '01010',
  'S'  : '00101',
  'T'  : '10000',
  'U'  : '00111',
  'V'  : '11110',
  'W'  : '10011',
  'X'  : '11101',
  'Y'  : '10101',
  'Z'  : '10001',
}

#lookup dictionary for figs
asciifigs_to_binstr = {
  '1'  : '10111',
  '2'  : '10011',
  '3'  : '00001',
  '4'  : '01011',
  '5'  : '10000',
  '6'  : '10101',
  '7'  : '00111',
  '8'  : '00110',
  '9'  : '11000',
  '0'  : '10110',
  '-'  : '00011',
  '?'  : '11001',
  ':'  : '01110',
  '$'  : '01001',
  '!'  : '01001',
  '&'  : '11010',
  '#'  : '10100',
  '('  : '01111',
  ')'  : '10010',
  '.'  : '11100',
  ','  : '01100',
  '\'' : '01010',
  '/'  : '11101',
  '"'  : '11101',
  ' '  : '00100'
}

#swaps table data to generate binsrt_to_asciiltrs for teletype tx
binstr_to_asciiltrs = { asciiltrs_to_binstr[k]: k for k in asciiltrs_to_binstr}

#swaps table data to generate binsrt_to_asciifigs for teletype tx
binstr_to_asciifigs = { asciifigs_to_binstr[k]: k for k in asciifigs_to_binstr}



def readbit(): #read a single bit
   return (1 - GPIO.input(key)) #read dat bit

def teletype_tx(data):
   txbaudot(data)
   
while True:
   a = [] #blank the list
   n = 5 #reset the count
   if GPIO.event_detected(key):
         time.sleep(0.035) #center up on start bit
         while n > 0:
            b = readbit()
            a.append(b) #add next bit to end
            n -= 1 
            time.sleep(d) #wait for exit of bit and start of next
         time.sleep(e) #stop bit buffer
         a.reverse() #reverse order to match lookup table oddities
         baudot = ''.join(map(str, a)) #convert list to string
         print(baudot)
         if (baudot == '11111'):
            s = 0 #ltrs mode
            print("ltrs mode")
            #txbaudot(baudot)
         elif (baudot == '11011'):
            s = 1 #figs mode
            print("figs mode")
            #txbaudot(baudot)
         elif (s == 0 and baudot in binstr_to_asciiltrs):
            c = binstr_to_asciiltrs[baudot]
            #tx_ascii_chr(c)
            print(c)
            #txbaudot(baudot)
         elif (s == 1 and baudot in binstr_to_asciifigs):
            c = binstr_to_asciifigs[baudot]
            #tx_ascii_chr(c)
            print(c)
            #txbaudot(baudot)
         else:
            print(baudot)
            #txbaudot(baudot)
         pool.apply_async(txbaudot, [baudot]) #execute the async process to transmit baudots out
         
