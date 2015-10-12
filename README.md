Project basted on http://sudobob.com/teletype-pi and his work with a uni-directional teleprinter setup. As my particular Model 15 Teletypewriter has a keyboard, I'm aiming to make it bi-directional, using similar methods.

Much thanks to SudoBob!

Compatible with python3

Raspberry Pi OS "Jessie"
python3.4
Install WebIOPi (using version WebIOPi-0.7.1)

Run 'python3 app.py' to start.

Note: python (python2) and webiopi don'y play nice and  have a significant issue (webiopi will not install properly).
After fighting this for hours, decided to just move to python3 (which required editing the code for new syntax compatiblity).


Modes:

tx = Accepting Teletype Keyboard Input, Echoed to Teletype Printer, Sent to Twitter, Motor On

rx = Tweets Printing to Teletype Printer, Teletype Keyboard Input Ignored, Motor On

sleep = Waiting for Tweets from Twitter or Waiting for UserStart (Start Button, Motion, or KeyPress), Motor Off
