#!/usr/bin/python3
# -*- coding: utf-8 -*-
# at: 10/10/2018
import threading
import time
import serial
from inspect import currentframe, getframeinfo
from exceptionLogger import exceptionLogger
from syscall import syscall
import multiprocessing

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


def btReconect():
    syscall("/home/pi/RobcomDrinkingMachine/RobcomWebService/bluetooth_connect.sh")
    #syscall("rfcomm connect hci0 98:D3:33:80:8E:AE")
    return

#thread_btReconect = threading.Thread(target=btReconect, args=())

class bluetoothControler():
    def __init__(self):
        self.thread_btReconect = multiprocessing.Process(target=btReconect, args=())

    def sendBluetooth(self, str_to_send):
        while 1:
            try:
                bluetoothSerial = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=2)  # pode variar o rfcomm
                bluetoothSerial.write(str(str_to_send).encode())
                print("Enviado via blutooth: {0}".format(str_to_send))
                return
            except Exception as exc:
                print("TEVE EXCECAO: {0}".format(exc))
                #exceptionLogger("bluetoothController.py", "sendBluetooth", getframeinfo(currentframe()).lineno, exc)
                #syscall("for i in $(pgrep rfcomm); do kill $i; done;")
                #syscall("for i in $(pgrep bluetooth_conn); do kill $i; done;")
                time.sleep(3);
                """
                try:
                    try:
                        #thread_btReconect.stop()
                        self.thread_btReconect.terminate()
                    except Exception as exc:
                        print("Erro em stop: {0}".format(exc))
                    time.sleep(3)
                    self.thread_btReconect.start()
                    #thread_btReconect.start()
                except Exception as exc:
                    print("Erro em bluetooth: {0}".format(exc))
                time.sleep(10)
                """

    def receiveBluetooth(self, data_expected):
        while 1:
            try:
                while(1):
                    bluetoothSerial = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=2)
                    print("Aguardando...")
                    resposta = bluetoothSerial.readline()
                    resposta = resposta.decode().replace('\n', '')
                    print("Recebido via blutooth: {0}".format(resposta))
                    if (str(resposta) != data_expected ):
                        try:
                            print("Dado errado recebido. Esperado: {0}, Recebido: {1}".format(data_expected, resposta))
                            self.sendBluetooth((int(data_expected)-1))
                        except Exception as exc:
                            print("TEVE EXCECAO: {0}".format(exc))
                    else:
                        return
            except Exception as exc:
                print("TEVE EXCECAO: {0}".format(exc))
                #exceptionLogger("bluetoothController.py", "sendBluetooth", getframeinfo(currentframe()).lineno, exc)
                #syscall("for i in $(pgrep rfcomm); do kill $i; done;")
                #syscall("for i in $(pgrep bluetooth_conn); do kill $i; done;")
                time.sleep(3);
                """
                try:
                    try:
                        #thread_btReconect.stop()
                        #self.thread_btReconect.terminate()
                    except Exception as exc:
                        #print("Erro em stop: {0}".format(exc))
                    #time.sleep(3)
                    #self.thread_btReconect.start()
                    #thread_btReconect.start()
                except Exception as exc:
                    print("Erro em bluetooth: {0}".format(exc))
                time.sleep(10)
                """

    def connectionChecker(self):
        while 1:
            try:
                bluetoothSerial = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=2)
                bluetoothSerial.write(str("A").encode())
                return
                #print("Enviado via blutooth: {0}".format("A"))
            except Exception as exc:
                print("TEVE EXCECAO: {0}".format(exc))
                #exceptionLogger("bluetoothController.py", "sendBluetooth", getframeinfo(currentframe()).lineno, exc)
                print("Erro na conexao bluetooth, reconectando...")
                #syscall("for i in $(pgrep rfcomm); do kill $i; done;")
                #syscall("for i in $(pgrep bluetooth_conn); do kill $i; done;")
                time.sleep(3);
                """
                try:
                    try:
                        pass
                        #thread_btReconect.stop()
                        #self.thread_btReconect.terminate()
                    except Exception as exc:
                        print("Erro em stop: {0}".format(exc))
                    #time.sleep(3)
                    #self.thread_btReconect.start()
                    #thread_btReconect.start()
                except Exception as exc:
                    print("Erro em bluetooth: {0}".format(exc))
                """
                #time.sleep(10)

    def connectionCheckerOfInit(self):
        try:
            bluetoothSerial = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=2)
            bluetoothSerial.write(str("A").encode())
            time.sleep(2)
            return
            #print("Enviado via blutooth: {0}".format("A"))
        except Exception as exc:
            print("TEVE EXCECAO: {0}".format(exc))
            #exceptionLogger("bluetoothController.py", "sendBluetooth", getframeinfo(currentframe()).lineno, exc)
            print("Erro na conexao bluetooth, reconectando...")
            #syscall("for i in $(pgrep rfcomm); do kill $i; done;")
            #syscall("for i in $(pgrep bluetooth_conn); do kill $i; done;")
            time.sleep(3);
            """
            try:
                try:
                    #thread_btReconect.stop()
                    #self.thread_btReconect.terminate()
                except Exception as exc:
                    print("Erro em stop: {0}".format(exc))
                time.sleep(3)
                #self.thread_btReconect.start()
            except Exception as exc:
                print("Erro em bluetooth: {0}".format(exc))
            time.sleep(10)
            """
