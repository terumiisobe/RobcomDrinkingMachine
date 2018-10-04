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
#import RPi.GPIO as GPIO
import pigpio

pi = -1
#############Portas GPIO##############
led1 = 4
######################################
led1_state = 0
def gpioConfig():
    print("Configurando GPIO...")
    try:
        global pi
        pi = pigpio.pi()
        if not pi.connected:
            print("Erro ao conectar GPIO.")
        else: 
            print("Pi conectada")
        ##Setup##
        #Inputs
        #Outputs
        pi.set_mode(led1, pigpio.OUTPUT)
    except Exception as exc:
        print(exc)

if __name__ == "__main__":
    print('Robcom iniciado!')
    try:
        gpioConfig()
        #global pi
        while 1:
            print("led 7 ligado")
            pi.write(led1, 1)
            time.sleep(2)
            print("led 7 desligado")
            pi.write(led1, 0)
            time.sleep(2)
    except Exception as exc:
        print(exc)
        exceptionLogger("led.py", "main", getframeinfo(currentframe()).lineno, exc)

