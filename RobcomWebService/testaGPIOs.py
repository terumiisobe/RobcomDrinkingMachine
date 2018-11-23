#!/usr/bin/python3
# -*- coding: utf-8 -*-
# at: 10/10/2018
import threading
import time
from inspect import currentframe, getframeinfo
from exceptionLogger import exceptionLogger

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

class gpioTest():
    def testaLed(self, pi):
        print("  Testando Led...")
        pi.write(led1, 1)
        time.sleep(1)
        pi.write(led1, 0)
        print("   -OK")

    def testaBombas(self, pi):
        print("  Testando bombas hidraulicas...")
        pi.write(b1, 1)
        pi.write(b2, 0)
        pi.write(b3, 0)
        time.sleep(0.5)
        pi.write(b1, 0)
        pi.write(b2, 1)
        pi.write(b3, 0)
        time.sleep(0.5)
        pi.write(b1, 0)
        pi.write(b2, 0)
        pi.write(b3, 1)
        time.sleep(0.5)
        pi.write(b1, 0)
        pi.write(b2, 0)
        pi.write(b3, 0)
        print("   -OK")

    def testaStepMotors(self, pi):
        print("  Testando Servos...")
        # Zera a posição dos 3 servos
        pi.set_servo_pulsewidth(servo1, 1010)
        pi.set_servo_pulsewidth(servo2, 2210)
        pi.set_servo_pulsewidth(servo0, 1900)
        time.sleep(0.2)
	# Prende o dispenser com o servo 0
        pi.set_servo_pulsewidth(servo0, 1600)
        time.sleep(1)
        # roda lentamente ambos servos, o 1 no sentido horario e o 2 no anti-horario
        # Movimento completo dura 4 segundos
#        return
        for i in range(0, 750, 20):
            pi.set_servo_pulsewidth(servo1, 1010 + i)
            pi.set_servo_pulsewidth(servo2, 2210 - i)
            time.sleep(0.1)
        time.sleep(1)
        # Zera posição dos dois servos
        for i in range(0, 750, 40):
            pi.set_servo_pulsewidth(servo1, 1750 - i)
            pi.set_servo_pulsewidth(servo2, 1460 + i)
            time.sleep(0.1)
        time.sleep(1)
	# Solta o dispenser com o servo 0
        pi.set_servo_pulsewidth(servo1, 1010)
        pi.set_servo_pulsewidth(servo2, 2210)
        pi.set_servo_pulsewidth(servo0, 1900)
        print("   -OK")

    def testaTodasGPIOs(self, pi):
        try:
            self.testaLed(pi)
            self.testaBombas(pi)
            self.testaStepMotors(pi)
        except Exception as exc:
            exceptionLogger("testaGPIOs.py", "testaTodasGPIOs", getframeinfo(currentframe()).lineno, exc)
            print(exc)
