#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# Defs: 
BT=300  #BounceTime for edge detection in milisecs 
#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM) # attention!
# PIN definition
# the pins we are going to use (BOARD)
#pinid1 = 21
#pinid2 = 23
#pinid3 = 7
#pinid4 = 11
#pinid5 = 13
#pinid6 = 15
# Pin Array
piny  = [ 21, 23, 7, 11, 13, 15 ]
relay = 4 
# users array 
users = {21: 'user000001', 23: 'user100000', 7: 'user000100', 11: 'user010000', 13: 'user001000', 15: 'user000010', }
# tlacitko function 
#   logs switch press and writes the log 
def tlacitko(cislo):
    print time.ctime(), ",", time.time(), "," ,users[cislo]
    # relay switch On/Off
    GPIO.output(relay,True)
    time.sleep(BT/300)
    GPIO.output(relay,False)    

# Main prog 
# PIN settings        
for i in piny:
    # Set Up All PINs to pull down
    GPIO.setup(i, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    # Add handler to all detected switches
    GPIO.add_event_detect(i, GPIO.RISING, callback=tlacitko, bouncetime=BT)
#Relay PIN
GPIO.setup(relay, GPIO.OUT)

# cycle
while True:
        print time.ctime()
        time.sleep(2)

GPIO.cleanup()
# EOF
