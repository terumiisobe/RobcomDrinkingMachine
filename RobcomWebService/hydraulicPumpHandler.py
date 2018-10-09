#!/usr/bin/python3
from inspect import currentframe, getframeinfo
from exceptionLogger import exceptionLogger
import time
#############Portas GPIO##############
#Bombas hidraulicas
b1 = 17  #Pino 11
b2 = 27  #Pino 13
b3 = 22  #Pino 15
#Led 1 só informando que está ligado
led1 = 18   #Pino 12
#Servo motores
#servoWrite(pulseWidth): https://github.com/fivdi/pigpio/blob/master/doc/gpio.md#servowritepulsewidth
#motor1.servoWrite(500) = max anti-horário
#motor1.servoWrite(2500) = max horário
servo1 = 12  #Pino 32
servo2 = 13  #Pino 33
######################################

class HydraulicPump():
    @staticmethod
    def drinkMaker(self, pi, drinkID):
        try:
            if drinkID == 1: #Sex on the beach
                #100
                #010
                #001
                #000
                pi.write(b1, 1)
                pi.write(b2, 0)
                pi.write(b3, 0)
                time.sleep(1)
                pi.write(b1, 0)
                pi.write(b2, 1)
                pi.write(b3, 0)
                time.sleep(1)
                pi.write(b1, 0)
                pi.write(b2, 0)
                pi.write(b3, 1)
                time.sleep(1)
                pi.write(b1, 0)
                pi.write(b2, 0)
                pi.write(b3, 0)
                time.sleep(1)

            if drinkID == 2: #Cuba Libre
                #111
                #000
                #111
                #000
                pi.write(b1, 1)
                pi.write(b2, 1)
                pi.write(b3, 1)
                time.sleep(1)
                pi.write(b1, 0)
                pi.write(b2, 0)
                pi.write(b3, 0)
                time.sleep(1)
                pi.write(b1, 1)
                pi.write(b2, 1)
                pi.write(b3, 1)
                time.sleep(1)
                pi.write(b1, 0)
                pi.write(b2, 0)
                pi.write(b3, 0)
                time.sleep(1)
            if drinkID == 3: #Jakubits
                #110
                #011
                #010
                #000
                pi.write(b1, 1)
                pi.write(b2, 1)
                pi.write(b3, 0)
                time.sleep(1)
                pi.write(b1, 0)
                pi.write(b2, 1)
                pi.write(b3, 1)
                time.sleep(1)
                pi.write(b1, 0)
                pi.write(b2, 1)
                pi.write(b3, 0)
                time.sleep(1)
                pi.write(b1, 0)
                pi.write(b2, 0)
                pi.write(b3, 0)
                time.sleep(1)
        except Exception as exc:
            exceptionLogger("hidraulicPumpHandler.py", "drinkMaker", getframeinfo(currentframe()).lineno, exc)
            print (exc)
            return -1
        
