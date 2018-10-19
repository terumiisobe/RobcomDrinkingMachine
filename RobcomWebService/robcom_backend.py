#!/usr/bin/python3
import time
import json
from flask import Flask, request, render_template #pip3 install flask
from inspect import currentframe, getframeinfo
from datetime import datetime
import threading
import pigpio
from robotProcessManager import RobotManager
from syscall import syscall
from exceptionLogger import exceptionLogger
from testaGPIOs import gpioTest

pi = None

#############Portas GPIO##############
#Bombas hidraulicas
b1 = 17  #Pino 11
b2 = 27  #Pino 13
b3 = 22  #Pino 15
#Led 1 só informando que está ligado
led1 = 18   #Pino 12
#Servo motores
servo1 = 12  #Pino 32
servo2 = 13  #Pino 33
######################################

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
        pi.set_mode(servo1, pigpio.OUTPUT)
        pi.set_mode(servo2, pigpio.OUTPUT)
        print("  OK")
        return pi
    except Exception as exc:
        print("TEVE EXCECAO: {0}".format(exc))
        exceptionLogger("flaskAPIBridge.py", "gpioConfig", getframeinfo(currentframe()).lineno, exc)


#---------------FLASK FUNCTIONS---------------
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    '''
    Pagina base do sistema de pedidos Robcom
    '''
    return render_template('index.html', title='Robçom Menu')

#Rota para redirecionar após realizar o pedido
#@app.route('/thanks!')
#def index():
'''
Pagina de agradecimento apos um cliente fazer um pedido/acompanhamento do estado de seu pedidos (uma ideia seria retornar para o usuário o tempo medio 
esperado para chegar o pedido dele, que pode-se calcular pela posição da fila que ele foi inserido)
'''
#    return render_template('thanks.html')

@app.route("/drinkRequest", methods=["POST"])
def socketSender():
    '''
    Rota para o front-end trocar dados com o back-end através da pagina /index.html
    '''
    print('Requisicao recebida no socketSender')
    try:
        if request.method == "POST":
            message = request.form.to_dict() #.decode()
            print (message)
            tableID = message['tableID'] #
            drinkID = message['drinkID'] #
            
            retorno = robotManager.drinkQueueAdd(tableID, drinkID)
            
            print("\n\nReceived: {0}".format(message))
            server_response = json.dumps({"status": retorno})
            return server_response
        else:
            server_response = {"status": -1}
            return json.dumps(server_response)
    except Exception as exc:
        print("TEVE EXCECAO: {0}".format(exc))
        exceptionLogger("flaskAPIBridge.py", "socketSender", getframeinfo(currentframe()).lineno, exc)
        server_response = {"status": -1}
        return json.dumps(server_response)
#---------------------------------------------


if __name__ == "__main__":
    '''
    main do sistema
    '''
    print('Iniciando Robcom...')
    try:
        pi = gpioConfig()
        robotManager = RobotManager(pi)
        #gpioTester = gpioTest()
        #gpioTester.testaTodasGPIOs(pi)
        #gpioTester.testaTodasGPIOs(pi)

        #app.debug = True
        print("  Ligando serviço de comunicação bluetooth com Robcom...")
        robcomDrinkMakerThread = threading.Thread(target=robotManager.robcomDrinkMaker, args=())
        robcomDrinkMakerThread.start()
        print("   -OK")
        print("  Ligando Flask Web Service...")
        app.run(host='192.168.241.1', port=80)
        print("   -OK")
        print(" -OK")
    except Exception as exc:
        print("TEVE EXCECAO: {0}".format(exc))
        exceptionLogger("flaskAPIBridge.py", "main", getframeinfo(currentframe()).lineno, exc)

