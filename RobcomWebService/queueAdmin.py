#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Finished at: 08/10/2018
import json
from inspect import currentframe, getframeinfo
from exceptionLogger import exceptionLogger
import time

class DrinkQueue():
    queue = []
    
    def push(self, tableID, drinkID):
        '''
        adiciona elemento json na fila na ultima posição
        '''
        try:
            data = json.dumps({'tableID': tableID, 'drinkID':drinkID})
            #print("push de {0}".format(data))
            self.queue = self.queue + [data] #insere elemento no fim da queue
            self.printQueue()
            return 1
        except Exception as exc:
            exceptionLogger("queueAdmin.py", "push", getframeinfo(currentframe()).lineno, exc)
            print (exc)
            return -1
        
    def pop(self):
        '''
        remove primeiro elemento da fila e o retorna na forma de 2 dados separados, tebleID e drinkID, nesta ordem
        '''
        try:
            while len(self.queue) == 0:
                #print("Fila vazia!")
                time.sleep(5)
            #print("Fila recebeu dado: {0}".format(self.queue))
            data = self.queue[0]
            data = json.loads(data)
            #print(data)
            self.queue = self.queue[1:] #Remove o elemento 0 da queue
            return data['tableID'], data['drinkID']
        except Exception as exc:
            exceptionLogger("queueAdmin.py", "pop", getframeinfo(currentframe()).lineno, exc)
            print (exc)
            return -1

    def printQueue(self):
        print("Fila atual: ")
        for i in self.queue:
            print("      -{0}".format(i))
