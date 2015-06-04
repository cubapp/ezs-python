#!/usr/bin/python
import RPi.GPIO as GPIO
import time

# Definice: 
BT=300  #BounceTime pro detekci hrany v milisekundach
GPIO.setmode(GPIO.BOARD)
# definice PINu
# the pins we are going to use (BOARD)
#pinid1 = 21
#pinid2 = 23
#pinid3 = 7
#pinid4 = 11
#pinid5 = 13
#pinid6 = 15
# pole pinu 
piny  = [ 21, 23, 7, 11, 13, 15 ]
# uzivatele
users = {21: 'user000001', 23: 'user100000', 7: 'user000100', 11: 'user010000', 13: 'user001000', 15: 'user000010', }
# funkce tlacitko
#   loguje tlacitko a pise cislo podle tabulky
def tlacitko(cislo):
        #print("Tlacitko cislo: "), cislo, time.ctime(), ",", time.time(), "," ,users[cislo]
        print time.ctime(), ",", time.time(), "," ,users[cislo]

GPIO.cleanup()

# Hlavni program 
# nastaveni PINu        
for i in piny
    GPIO.setup(i, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    GPIO.add_event_detect(i, GPIO.RISING, callback=tlacitko, bouncetime=BT)

# smycka 
while True:

        print time.ctime()
        time.sleep(2)

GPIO.cleanup()
# EOF
