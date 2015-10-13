import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD) #sets GPIO numbering system to BOARD pin numbers versus BCM numbering

GPIO.setup(23, GPIO.IN)

#print(GPIO.input(23))
#print(1 - GPIO.input(23))

GPIO.add_event_detect(23, GPIO.RISING) #add rising edge detection on GPIO 23

n = 25

while True:

   if GPIO.event_detected(23):
      while 0 < n: 
         time.sleep(0.003) #wait time for start bit end
         print(1 - GPIO.input(23))
         n -= 1
         time.sleep(0.006) #time between bits
      break

#if GPIO.input(
