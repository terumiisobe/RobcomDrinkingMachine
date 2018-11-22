#!/usr/bin/python3
#Ref :http://www.uugear.com/portfolio/bluetooth-communication-between-raspberry-pi-and-arduino/

import serial
from time import sleep

#bluetoothSerial = serial.Serial( "/dev/rfcomm0", baudrate=9600, xonxoff=False, rtscts=False, dsrdtr=False) #pode variar o rfcomm
bluetoothSerial = serial.Serial( "/dev/rfcomm0", baudrate=9600, timeout=2) #pode variar o rfcomm
dado = "nada"
dado = input("Insira o dado que deseja enviar:\n Para sair, digite q;\n --> ")

while dado != 'q':
    try:
        #dado = input("Insira o dado que deseja enviar:\n Para sair, digite q;\n --> ")
        bluetoothSerial.write(str(dado).encode())
        print("Enviado {0}".format(dado))
        print (bluetoothSerial.readline().decode().replace('\n',''))
        #print (bluetoothSerial.read())
        sleep(1)
    except Exception as exc:
        print(exc)
        exit()
