#!/usr/bin/python3
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
servo1 = 12  #Pino 32
servo2 = 13  #Pino 33
######################################

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
        time.sleep(0.1)
        pi.write(b1, 0)
        pi.write(b2, 1)
        pi.write(b3, 0)
        time.sleep(0.1)
        pi.write(b1, 0)
        pi.write(b2, 0)
        pi.write(b3, 1)
        time.sleep(0.1)
        pi.write(b1, 0)
        pi.write(b2, 0)
        pi.write(b3, 0)
        print("   -OK")

    def testaStepMotors(self, pi):
        print("  Testando Servos...")
        # Zera a posição dos dois servos
        pi.set_servo_pulsewidth(servo1, 1000)
        pi.set_servo_pulsewidth(servo2, 2080)
        time.sleep(1)
        # roda lentamente ambos servos, o 1 no sentido horario e o 2 no anti-horario
        # Movimento completo dura 4 segundos
        for i in range(0, 800, 20):
            pi.set_servo_pulsewidth(servo1, 1000 + i)
            pi.set_servo_pulsewidth(servo2, 2080 - i)
            time.sleep(0.1)
        time.sleep(1)
        # Zera posição dos dois servos
        pi.set_servo_pulsewidth(servo1, 1000)
        pi.set_servo_pulsewidth(servo2, 2080)
        time.sleep(2)
        print("   -OK")

    def testaTodasGPIOs(self, pi):
        try:
            print("teste")
            self.testaLed(pi)
            self.testaBombas(pi)
            self.testaStepMotors(pi)
        except Exception as exc:
            exceptionLogger("testaGPIOs.py", "testaTodasGPIOs", getframeinfo(currentframe()).lineno, exc)
            print(exc)
