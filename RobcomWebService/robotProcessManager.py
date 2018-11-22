#!/usr/bin/python3
# -*- coding: utf-8 -*-
import threading
import time
from inspect import currentframe, getframeinfo
from datetime import datetime
from queueAdmin import DrinkQueue
from hydraulicPumpHandler import HydraulicPump
from bluetoothControler import bluetoothControler
from syscall import syscall
from servoControl import ServoControl
from exceptionLogger import exceptionLogger

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

class RobotManager():
    def __init__(self, pi):
        self.pi = pi
        self.requestsQueue = DrinkQueue()
        self.pumpHandler = HydraulicPump(self.pi)
        self.servoControler = ServoControl(self.pi)
        self.bluetoothContr = bluetoothControler()

    def robcomDrinkMaker(self):
        '''
        Administra a função de preparo de drinks e pop na fila de pedidos
        param: pi: gpio controler
        '''
        try:
            # Verifica se bluetooth esta conectado
            # robcomDrinkMakerThread = threading.Thread(target=self.bluetoothContr.connectionChecker, args=())
            # robcomDrinkMakerThread.start()
            while 1:
                self.bluetoothContr.connectionChecker()
                # Aguarda dado do carrinho avisando que está sob o dispenser
                print("Aguardando carro enviar 1 via bluetooth pra avisar que está sob o dispenser.")
                self.bluetoothContr.receiveBluetooth("1")
                # Dar pop na fila de drinks, caso não haja pedidos na fila, o sistema fica parado aqui
                drinkToMake = 1
                tableToDeliver = 8
                #tableToDeliver, drinkToMake = self.requestsQueue.pop()
                print("Iniciando preparação de drink")
                #self.pi.write(led1, 1)
                # Deposita copo (aciona função para enviar um copo)
                print("Retirando um copo")
                time.sleep(1)
                #self.servoControler.retiraUmCopo()
                # Informa ao carro de que o copo foi enviado
                # Aguarda confirmação do carro de que recebeu copo (Segue ideia de um TCP pra prevenção de erros)
                self.bluetoothContr.sendBluetooth("2")
                # Aguarda dado de que o carrinho está sob as bombas hidraulicas
                self.bluetoothContr.receiveBluetooth("3")
                # Executar as bombas hidraulicas de acordo com o drink desejado
                print("Preparando drink {0}".format(drinkToMake))
                self.pi.write(b1, 1)
                self.pi.write(b2, 0)
                self.pi.write(b3, 0)
                time.sleep(0.5)
                self.pi.write(b1, 0)
                self.pi.write(b2, 1)
                self.pi.write(b3, 0)
                time.sleep(0.5)
                self.pi.write(b1, 0)
                self.pi.write(b2, 0)
                self.pi.write(b3, 1)
                time.sleep(0.5)
                self.pi.write(b1, 0)
                self.pi.write(b2, 0)
                self.pi.write(b3, 0)
                #time.sleep(10)
                #self.pumpHandler.drinkMaker(drinkToMake)
                # Enviar dado ao carrinho que ele já pode entregar o drink para a mesa "tableID" definida pelo cliente
                self.bluetoothContr.sendBluetooth(tableToDeliver)
                print("Drink Pronto!!!")
                time.sleep(8)
        except Exception as exc:
            exceptionLogger("robotProcessManager.py", "robcomDrinkMaker", getframeinfo(currentframe()).lineno, exc)
            print(exc)

    def drinkQueueAdd(self, tableID, drinkID):
        '''
        Insere um pedido feito no cardápio na fila de pedidos
        '''
        try:
            return self.requestsQueue.push(tableID, drinkID)
        except Exception as exc:
            exceptionLogger("robotProcessManager.py", "drinkQueueAdd", getframeinfo(currentframe()).lineno, exc)
            print(exc)
            return -1
