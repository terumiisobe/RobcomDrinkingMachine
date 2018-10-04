#!/usr/bin/python3
import threading
import time
import json
import subprocess
from flask import Flask, request, render_template #pip3 install flask
from urllib.parse import urlencode
from inspect import currentframe, getframeinfo
from datetime import datetime
import threading
import pigpio
pi = None

#############Portas GPIO##############
led1 = 4
led2 = 27
led3 = 22
######################################

def syscall(p_command):
    v_subProcess = subprocess.run(p_command, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
    return v_subProcess.stdout.decode('utf-8').split('\n')[:-1]

try:
    #-------------------------------------------------------------------------
    #LOG system
    log_file = "RobcomLog"
    print ("Log_file = %s"%(log_file))
    #-------------------------------------------------------------------------
except Exception as exc:
    print("Error in mac or log_file")
    
def exceptionLogger(code, function, line_number, exc):
    global v_macEth0
    exc = str(exc).replace(')','\)').replace('(','\(').replace('>','\>').replace('<','\<').replace(';','\;').replace('"','\\"').replace("'","\\'")
    time = datetime.now().strftime("%H:%M:%S")
    mes_dia_ano = datetime.now().strftime("%b %d %Y")
    syscall("echo {0} {1} {2} {3} line:{4}: {5} >> /home/pi/RobcomSetup/{6}".format(mes_dia_ano, time, code, function, line_number, exc, log_file))

def gpioConfig():
    print("Configurando GPIO...")
    try:
        global pi
        pi = pigpio.pi()
        if not pi.connected:
            print("Erro ao conectar GPIO.")

        ##Setup##
        #Inputs
        
        #Outputs
        pi.set_mode(led1, pigpio.OUTPUT)
        pi.set_mode(led2, pigpio.OUTPUT)
        pi.set_mode(led3, pigpio.OUTPUT)
    except Exception as exc:
        print("TEVE EXCESSAO: {0}".format(exc))
        exceptionLogger("flaskAPIBridge.py", "gpioConfig", getframeinfo(currentframe()).lineno, exc)

def drinkMaker():
    global pi
    global led1
    global led2
    global led3
    state = 0
    if state == 0:
        print("entrou na ledStateChange")
       # if(drinkID == 1):
        pi.write(led1, 1)
        pi.write(led2, 1)
       	pi.write(led3, 1)
        time.sleep(1)
       # elif(drinkID == 2):
        pi.write(led1, 0)
        pi.write(led2, 0)
        pi.write(led3, 0)
        time.sleep(1)
        pi.write(led1, 1)
        pi.write(led2, 1)
       	pi.write(led3, 1)
        time.sleep(1)
        pi.write(led1, 0)
        pi.write(led2, 0)
       	pi.write(led3, 0)
        time.sleep(1)
        return
    else:
        return
#---------------FLASK FUNCTIONS---------------
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Robçom Menu')

@app.route("/drinkRequest", methods=["POST"])
def socketSender(): #sincrona
    print('Requisicao recebida no socketSender')
    try:
        if request.method == "POST":
            message = request.form.to_dict() #.decode()
            print(message['tableID'])
            print(message['drinkID'])
            drinkMaker()
            #message = json.loads(message)
            print("\n\nReceived: {0}".format(message))
            server_response = json.dumps({"status": 1})
            return server_response
            #return "teste", 200, {"Content-Type": "application/json"}
        else:
            server_response = {"status": -1}
            return json.dumps(server_response)
    except Exception as exc:
        print("TEVE EXCESSAO: {0}".format(exc))
        exceptionLogger("flaskAPIBridge.py", "socketSender", getframeinfo(currentframe()).lineno, exc)
        server_response = {"status": -1}
        return json.dumps(server_response)
#---------------------------------------------


if __name__ == "__main__":
    print('Robcom iniciado!')
    try:
        gpioConfig()
        print("Testando Leds...")
        pi.write(led1, 1)
        pi.write(led2, 1)
        pi.write(led3, 1)
        time.sleep(1)
        pi.write(led1, 0)
        pi.write(led2, 0)
        pi.write(led3, 0)
        print("OK!")
       #app.debug = True
        app.run(host='192.168.25.1', port=80)
        print("OK")
        #app.run()
    except Exception as exc:
        print("TEVE EXCESSAO: {0}".format(exc))
        exceptionLogger("flaskAPIBridge.py", "main", getframeinfo(currentframe()).lineno, exc)

