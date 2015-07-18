#!/usr/bin/python
import RPi.GPIO as GPIO
import time
  
try:
  # Definitions: 
  LOGFILE="/opt/ezs/log/ezs.log"
  BT=400  #BounceTime for edge detection in milisecs 
  GPIO.setmode(GPIO.BOARD)
  # the pins we are going to use (BOARD) - switchpins and relay
  switchpins  = [ 21, 23, 7, 11, 13, 15 ]
  relay = 8 
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
      #example:
      #Sat Jul 18 12:09:15 2015,1437214155,user000010
      if GPIO.input(innumber):
         logline = '%s,%d,%s' % (time.ctime(),int(time.time()),users[innumber])
         print logline
         logaccess(logline)
         #driverelay(BT/100)  #approx 3sec
 
  # Relay driver function 
  def driverelay(sleeptime):
      # relay switch On/Off
      GPIO.output(relay,False)
      time.sleep(sleeptime)
      GPIO.output(relay,True)
 
  # logaccess function
  #   appends log to the log file 
  def logaccess(logtext):
      try:
        file = open(LOGFILE, 'a')
        file.write(logtext)
        file.write('\n')
      except IOError:
        print "Error, can not open or write to file", logfile, logtext
      else: 
        file.close()
  
  # Main prog 
  # PIN settings        
  # 1. Relay PIN
  GPIO.setup(relay, GPIO.OUT)
  # 2. Switch PINs - for all switchpins setu up as INUPT and register event_detect
  for i in switchpins:
      # Set Up All PINs to pull down
      #GPIO.setup(i, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
      GPIO.setup(i, GPIO.IN, pull_up_down = GPIO.PUD_UP)
      # Add handler to all detected switches
      #GPIO.add_event_detect(i, GPIO.RISING, callback=switchpress, bouncetime=BT)
      GPIO.add_event_detect(i, GPIO.FALLING, callback=switchpress, bouncetime=BT)
  # END of setting PINs
  # 
  # Program loop starts here>
  logline = '%s %s' % ('#begin',time.ctime())
  print logline
  logaccess (logline)
  driverelay(0.01)
  
  # Main and Only Cycle
  while True:
          #print time.ctime()
          time.sleep(2)

except KeyboardInterrupt:
  pass
finally: GPIO.cleanup() 
# EOF
