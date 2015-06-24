#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# Defs: 
BT=300  #BounceTime for edge detection in milisecs 
#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM) # attention!
# PIN definition
# the pins we are going to use (BOARD)
# pinid1 = 21 #pinid2 = 23 #pinid3 = 7 #pinid4 = 11 #pinid5 = 13 #pinid6 = 15
# Pin Array
switchpins  = [ 21, 23, 7, 11, 13, 15 ]
relay = 4 
# users array 
users = {
	21: 'user000001', 
	23: 'user100000', 
	7:  'user000100', 
	11: 'user010000', 
	13: 'user001000', 
	15: 'user000010', 
}
# switchpress function 
#   logs switch press and writes the log 
def switchpress(innumber):
    print time.ctime(), ",", time.time(), "," ,users[innumber]
    # relay switch On/Off
    GPIO.output(relay,True)
    time.sleep(BT/300)
    GPIO.output(relay,False)    

# Main prog 
# PIN settings        
# 1. Relay PIN
GPIO.setup(relay, GPIO.OUT)
# 2. Switch PINs - for all switchpins setu up as INUPT and register event_detect
for i in switchpins:
    # Set Up All PINs to pull down
    GPIO.setup(i, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    # Add handler to all detected switches
    GPIO.add_event_detect(i, GPIO.RISING, callback=switchpress, bouncetime=BT)
# END of setting PINs

# Main and Only Cycle
while True:
        print time.ctime()
        time.sleep(2)

#GPIO.cleanup()
# EOF
