#!/usr/bin/python3
import threading
import time
from inspect import currentframe, getframeinfo
from datetime import datetime
from queueAdmin import DrinkQueue
from hydraulicPumpHandler import HydraulicPump
from syscall import syscall
from servoControl import ServoControl
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

class RobotManager():
    def __init__(self, pi):
        self.pi = pi
        self.requestsQueue = DrinkQueue()
        self.pumpHandler = HydraulicPump(self.pi)
        self.servoControler = ServoControl(self.pi)

    def robcomDrinkMaker(self):
        '''
        Administra a função de preparo de drinks e pop na fila de pedidos
        param: pi: gpio controler
        '''
        try:
            while 1:
                #Verifica se bluetooth esta conectado
                #TODO!
                #Aguarda dado do carrinho avisando que está sob o dispenser
                #TODO!
                #Dar pop na fila de drinks, caso não haja pedidos na fila, o sistema fica parado aqui
                tableToDeliver, drinkToMake = self.requestsQueue.pop()
                print("Iniciando preparação de drink")
                self.pi.write(led1, 1)
                #Deposita copo (aciona função para enviar um copo)
                print("Retirando um copo")
                self.servoControler.retiraUmCopo()
                #Informa ao carro de que o copo foi enviado
                #TODO
                #Aguarda confirmação do carro de que recebeu copo (Segue ideia de um TCP pra prevenção de erros)
                #TODO
                #Aguarda dado de que o carrinho está sob as bombas hidraulicas
                #TODO
                #Executar as bombas hidraulicas de acordo com o drink desejado
                print("Preparando drink {0}".format(drinkToMake))
                self.pumpHandler.drinkMaker(drinkToMake)
                #Enviar dado ao carrinho que ele já pode entregar o drink para a mesa "tableID" definida pelo cliente
                #TODO
                print("Drink Pronto!!!")
                for i in range(3):
                    self.pi.write(led1, 1)
                    time.sleep(0.5)
                    self.pi.write(led1, 0)
                    time.sleep(0.5)
                self.pi.write(led1, 0)
                time.sleep(10)
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
