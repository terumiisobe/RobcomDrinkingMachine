#!/usr/bin/python3
# Finished at: 10/10/2018
from inspect import currentframe, getframeinfo
from exceptionLogger import exceptionLogger
import time

#############Portas GPIO##############
# Bombas hidraulicas
b1 = 17  # Pino 11
b2 = 27  # Pino 13
b3 = 22  # Pino 15
# Led 1 só informando que está ligado
led1 = 18  # Pino 12
# Servo motores
# servoWrite(pulseWidth): https://github.com/fivdi/pigpio/blob/master/doc/gpio.md#servowritepulsewidth
# motor1.servoWrite(500) = max anti-horário
# motor1.servoWrite(2500) = max horário
servo1 = 12  #Pino 32
servo2 = 13  #Pino 33
######################################

class ServoControl():
    @staticmethod
    def retiraUmCopo(self, pi):
        """
        Move ambos servos de forma a retirar um copo do dispenser
        param:pi: gpio controler
        """
        # 1000 # spin fast anticlockwise
        # 1400 # spin slow anticlockwise
        # 1500 # stop
        # 1600 # spin slow clockwise
        # 2000 # spin fast clockwise
        try:
            # Zera a posição dos dois servos
            pi.set_servo_pulsewidth(servo1, 1000)
            pi.set_servo_pulsewidth(servo2, 2000)
            time.sleep(1)
            # roda lentamente ambos servos, o 1 no sentido horario e o 2 no anti-horario
            # Movimento completo dura 4 segundos
            for i in range(0, 800, 20):
                pi.set_servo_pulsewidth(servo1, 1000 + i)
                pi.set_servo_pulsewidth(servo2, 2000 - i)
                time.sleep(0.1)
            time.sleep(1)
            # Zera posição dos dois servos
            pi.set_servo_pulsewidth(servo1, 1000)
            pi.set_servo_pulsewidth(servo2, 2000)
            time.sleep(2)
        except Exception as exc:
            exceptionLogger("servoControl.py", "removeUmCopo", getframeinfo(currentframe()).lineno, exc)
            print(exc)
            return -1
