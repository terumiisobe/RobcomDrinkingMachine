#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import json
from flask import Flask, request, render_template #pip3 install flask
from inspect import currentframe, getframeinfo
from datetime import datetime
import threading
import pigpio
from robotProcessManager import RobotManager
from syscall import syscall
from bluetoothControler import bluetoothControler
from exceptionLogger import exceptionLogger
from testaGPIOs import gpioTest
import logging

# ----------------TRATADOR DE CONSTANTES---------------------------
print('RobcomWebService Iniciado.\n')

pi = None
robotManager = None

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

def gpioConfig():
    '''
    Configura os modos das GPIO da raspberry pi B
    '''
    print("Configurando GPIO...")
    try:
        global pi
        pi = pigpio.pi()
        if not pi.connected:
            print("Erro ao conectar GPIO.")
        #Outputs
        pi.set_mode(b1, pigpio.OUTPUT)
        pi.set_mode(b2, pigpio.OUTPUT)
        pi.set_mode(b3, pigpio.OUTPUT)
        pi.set_mode(led1, pigpio.OUTPUT)
        pi.set_mode(servo0, pigpio.OUTPUT)
        pi.set_mode(servo1, pigpio.OUTPUT)
        pi.set_mode(servo2, pigpio.OUTPUT)
        #Garante que todas IOs estejam no estado inicial correto
        pi.set_servo_pulsewidth(servo1, 1010)
        pi.set_servo_pulsewidth(servo2, 2210)
        pi.set_servo_pulsewidth(servo0, 1900)
        pi.write(b1, 0)
        pi.write(b2, 0)
        pi.write(b3, 0)

        print("  OK")
        return pi
    except Exception as exc:
        print("TEVE EXCECAO: {0}".format(exc))
        exceptionLogger("flaskAPIBridge.py", "gpioConfig", getframeinfo(currentframe()).lineno, exc)

#---------------FLASK FUNCTIONS---------------
app = Flask(__name__)

@app.route('/')
#@app.route('/index')
def index():
    '''
    Pagina base do sistema de pedidos Robcom
    '''
    return render_template('login.html', title='Robçom Menu')

@app.route("/tableAndName", methods=["GET"])
def tableAndName():
    '''
    '''
    try:
        global robotManager
        if request.method == "GET":
            #message = request.form.to_dict() #.decode()
            #tableID = message['tableID']
            tableID = request.args.get('tableID')
            return render_template('drinklist.html', table=tableID)
        else:
            print("Request != get")
            server_response = {"status": -1}
            return json.dumps(server_response)
    except Exception as exc:
        print("TEVE EXCECAO: {0}".format(exc))
        exceptionLogger("flaskAPIBridge.py", "drinkRequest", getframeinfo(currentframe()).lineno, exc)
        server_response = {"status": -1}
        return json.dumps(server_response)

#Rota para redirecionar após realizar o pedido
@app.route('/waiting', methods=["GET"])
def waiting():
    '''
    Pagina de agradecimento apos um cliente fazer um pedido/acompanhamento do estado de seu pedidos (uma ideia seria retornar para o usuário o tempo medio 
    esperado para chegar o pedido dele, que pode-se calcular pela posição da fila que ele foi inserido)
    '''
    try:
        global robotManager
        if request.method == "GET":
            tableID = request.args.get('tableID')
            drinkID = request.args.get('drinkID')
            retorno = robotManager.drinkQueueAdd(tableID, drinkID)
            return render_template('waiting.html', table=tableID)
        else:
            print("Request != POST")
            server_response = {"status": -1}
            return json.dumps(server_response)
    except Exception as exc:
        print("TEVE EXCECAO: {0}".format(exc))
        exceptionLogger("flaskAPIBridge.py", "drinkRequest", getframeinfo(currentframe()).lineno, exc)
        server_response = {"status": -1}
        return json.dumps(server_response)



"""
@app.route("/drinkRequest", methods=["POST", "GET"])
def drinkRequest():
    '''
    Rota para o front-end trocar dados com o back-end através da pagina /index.html
    '''
    print('Requisicao recebida no drinkRequest')
    try:
        global robotManager
        if request.method == "GET":
            message = request.form.to_dict() #.decode()
            print("LOG FEITO")
            tableID = message['tableID'] #
            drinkID = message['drinkID'] #
            print("\n\nReceived: {0}".format(message))
            server_response = json.dumps({"status": retorno})
            return server_response
        if request.method == "GET":
            server_response = {"response": "False"}
            return json.dumps(server_response)
        else:
            server_response = {"status": -1}
            return json.dumps(server_response)
    except Exception as exc:
        print("TEVE EXCECAO: {0}".format(exc))
        exceptionLogger("flaskAPIBridge.py", "drinkRequest", getframeinfo(currentframe()).lineno, exc)
        server_response = {"status": -1}
        return json.dumps(server_response)
"""
#---------------------------------------------


def main():
    '''
    main do sistema
    '''
    print('Iniciando Robcom...')
    try:
        pi = gpioConfig()
        global robotManager
        robotManager = RobotManager(pi)
        #return
        gpioTester = gpioTest()
        #gpioTester.testaTodasGPIOs(pi)
        print("  Ligando serviço de comunicação bluetooth com Robcom...")
        #btObj = bluetoothControler()
        #btObj.connectionCheckerOfInit()
        print("   -OK")
        print("  Ligando serviço de tratamento de drinks...")
        robcomDrinkMakerThread = threading.Thread(target=robotManager.robcomDrinkMaker, args=())
        robcomDrinkMakerThread.start()
        print("   -OK")
        print("  Ligando Flask Web Service...")
#        if __name__ == "__main__" or 1: #esse or 1 é pra debug
        app.run(host='192.168.241.1', port=80, debug=False)
        #app.run()
        #app.run(host='0.0.0.0', port=80, debug=False)
        #app.run(host='0.0.0.0', debug=False)
        print("   -OK")
        print(" -OK")
    except Exception as exc:
        print("TEVE EXCECAO: {0}".format(exc))
        exceptionLogger("flaskAPIBridge.py", "main", getframeinfo(currentframe()).lineno, exc)

main()
