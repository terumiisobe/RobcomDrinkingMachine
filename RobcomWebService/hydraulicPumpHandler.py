#!/usr/bin/python3
# -*- coding: utf-8 -*-
from inspect import currentframe, getframeinfo
from exceptionLogger import exceptionLogger
import time

# ############Portas GPIO##############
# Bombas hidraulicas
b1 = 17  # Pino 11
b2 = 27  # Pino 13
b3 = 22  # Pino 15
# Led 1 só informando que está ligado
led1 = 18   # Pino 12
# Servo motores
# servoWrite(pulseWidth): https://github.com/fivdi/pigpio/blob/master/doc/gpio.md#servowritepulsewidth
# motor1.servoWrite(500) = max anti-horário
# motor1.servoWrite(2500) = max horário
servo0 = 19  # Pino 31 - Servo DISPENSER
servo1 = 12  # Pino 32 - Servo ESQUERDA
servo2 = 13  # Pino 33 - Servo DIREITA
# ###################x##################

class HydraulicPump():
    def __init__(self, pi):
        self.pi = pi

    def drinkMaker(self, drinkID):
        #Bomba 1 = Suco
        #Bomba 2 = Vodka
        #Bomba 3 = Refrigerante
        try:
            drinkID = str(drinkID)
            if drinkID == "1":
                #Disco Voador
                # 10% Vodka
                # 80% Suco
                self.pi.write(b1, 1)
                self.pi.write(b2, 1)
                self.pi.write(b3, 0)
                time.sleep(5)
                self.pi.write(b1, 1)
                self.pi.write(b2, 0)
                self.pi.write(b3, 0)
                time.sleep(12)
                self.pi.write(b1, 0)
                self.pi.write(b2, 0)
                self.pi.write(b3, 0)

            if drinkID == "2": #
                #Disco Voador
                # 20% Vodka
                # 40% Suco
                # 40% Refri
                self.pi.write(b1, 1)
                self.pi.write(b2, 1)
                self.pi.write(b3, 1)
                time.sleep(5)
                self.pi.write(b1, 1)
                self.pi.write(b2, 0)
                self.pi.write(b3, 1)
                time.sleep(5)
                self.pi.write(b1, 0)
                self.pi.write(b2, 0)
                self.pi.write(b3, 0)
            if drinkID == "3":
                # Neném
                # 100% Suco
                self.pi.write(b1, 1)
                self.pi.write(b2, 0)
                self.pi.write(b3, 0)
                time.sleep(10)
                self.pi.write(b1, 0)
                self.pi.write(b2, 0)
                self.pi.write(b3, 0)
            if drinkID == "4":
                # Sem Graca
                # 100% Refri
                self.pi.write(b1, 0)
                self.pi.write(b2, 0)
                self.pi.write(b3, 1)
                time.sleep(10)
                self.pi.write(b1, 0)
                self.pi.write(b2, 0)
                self.pi.write(b3, 0)
            if drinkID == "5":
                # La Muerte
                # 100% Vodka
                self.pi.write(b1, 0)
                self.pi.write(b2, 1)
                self.pi.write(b3, 0)
                time.sleep(8)
                self.pi.write(b1, 0)
                self.pi.write(b2, 0)
                self.pi.write(b3, 0)
            if drinkID == "6":
                # RefriFake
                # 20% Vodka
                # 40% Refri
                self.pi.write(b1, 0)
                self.pi.write(b2, 1)
                self.pi.write(b3, 1)
                time.sleep(4)
                self.pi.write(b1, 0)
                self.pi.write(b2, 0)
                self.pi.write(b3, 1)
                time.sleep(10)
                self.pi.write(b1, 0)
                self.pi.write(b2, 0)
                self.pi.write(b3, 0)
        except Exception as exc:
            exceptionLogger("hidraulicPumpHandler.py", "drinkMaker", getframeinfo(currentframe()).lineno, exc)
            print (exc)
            return -1
