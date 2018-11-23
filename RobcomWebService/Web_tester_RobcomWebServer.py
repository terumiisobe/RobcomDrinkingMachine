#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
import json
from flask import Flask, request, render_template #pip3 install flask
from inspect import currentframe, getframeinfo
from datetime import datetime
import threading
from syscall import syscall
from exceptionLogger import exceptionLogger
import logging



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
            #retorno = robotManager.drinkQueueAdd(tableID, drinkID)
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


def main():
    '''
    main do sistema
    '''
    print('Iniciando Robcom...')
    try:
        #pi = gpioConfig()
        #global robotManager
        #robotManager = RobotManager(pi)
        #return
        #gpioTester = gpioTest()
        #gpioTester.testaTodasGPIOs(pi)
        #print("  Ligando serviço de comunicação bluetooth com Robcom...")
        #btObj = bluetoothControler()
        #btObj.connectionCheckerOfInit()
        #print("   -OK")
        #print("  Ligando serviço de tratamento de drinks...")
        #robcomDrinkMakerThread = threading.Thread(target=robotManager.robcomDrinkMaker, args=())
        #robcomDrinkMakerThread.start()
        print("   -OK")
        print("  Ligando Flask Web Service...")
#        if __name__ == "__main__" or 1: #esse or 1 é pra debug
        app.run(host='127.0.0.1', port=8000, debug=False)
        #app.run()
        #app.run(host='0.0.0.0', port=80, debug=False)
        #app.run(host='0.0.0.0', debug=False)
        print("   -OK")
        print(" -OK")
    except Exception as exc:
        print("TEVE EXCECAO: {0}".format(exc))
        exceptionLogger("flaskAPIBridge.py", "main", getframeinfo(currentframe()).lineno, exc)

main()
