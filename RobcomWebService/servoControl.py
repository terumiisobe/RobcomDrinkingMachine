#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Finished at: 10/10/2018
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
servo0 = 19  #Pino 31 - Servo DISPENSER
servo1 = 12  #Pino 32 - Servo ESQUERDA
servo2 = 13  #Pino 33 - Servo DIREITA
####################x##################

class ServoControl():
    def __init__(self, pi):
        self.pi = pi

    def retiraUmCopo(self):
        """
        Move ambos servos de forma a retirar um copo do dispenser
        param:pi: gpio controler
        """
        try:
            # 1000 # spin fast anticlockwise
            # 1400 # spin slow anticlockwise
            # 1500 # stop
            # 1600 # spin slow clockwise
            # 2000 # spin fast clockwise

            # Zera a posição dos 3 servos
            self.pi.set_servo_pulsewidth(servo1, 1010)
            self.pi.set_servo_pulsewidth(servo2, 2210)
            self.pi.set_servo_pulsewidth(servo0, 1900)
            time.sleep(0.2)
            # Prende o dispenser com o servo 0
            self.pi.set_servo_pulsewidth(servo0, 1600)
            time.sleep(0.5)
            # roda lentamente ambos servos, o 1 no sentido horario e o 2 no anti-horario
            # Movimento completo dura 4 segundos
            for i in range(0, 750, 20):
                self.pi.set_servo_pulsewidth(servo1, 1010 + i)
                self.pi.set_servo_pulsewidth(servo2, 2210 - i)
                time.sleep(0.1)
            time.sleep(1)
            # Zera posição dos dois servos
            for i in range(0, 750, 50):
                self.pi.set_servo_pulsewidth(servo1, 1760 - i)
                self.pi.set_servo_pulsewidth(servo2, 1460 + i)
                time.sleep(0.1)
            # Solta o dispenser com o servo 0
            self.pi.set_servo_pulsewidth(servo1, 1010)
            self.pi.set_servo_pulsewidth(servo2, 2210)
            self.pi.set_servo_pulsewidth(servo0, 1900)
        except Exception as exc:
            exceptionLogger("servoControl.py", "retiraUmCopo", getframeinfo(currentframe()).lineno, exc)
            print(exc)
            return -1

    def shakeYoAss(self):
        """
        faz o dispenser de copos tremer para destravar os copos
        param:pi: gpio controler
        """
        try:
            # Zera a posição dos 3 servos
            self.pi.set_servo_pulsewidth(servo1, 1010)
            self.pi.set_servo_pulsewidth(servo2, 2210)
            self.pi.set_servo_pulsewidth(servo0, 1900)
            for i in range(0, 750, 20):
                self.pi.set_servo_pulsewidth(servo0, 1850)
                time.sleep(0.1)
                self.pi.set_servo_pulsewidth(servo0, 1750)
                time.sleep(0.1)
            time.sleep(0.5)
            self.pi.set_servo_pulsewidth(servo0, 1900)
            time.sleep(0.5)
        except Exception as exc:
            exceptionLogger("servoControl.py", "retiraUmCopo", getframeinfo(currentframe()).lineno, exc)
            print(exc)
            return -1
