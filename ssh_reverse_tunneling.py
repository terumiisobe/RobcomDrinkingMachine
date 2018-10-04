#!/usr/bin/python3
#Author: Lucas C. Tavano
#Date: 04/05/2018
import json
from urllib.parse import urlencode
import httplib2
import sys
import subprocess
import os
import socket

def syscall(p_command):
    v_subProcess = subprocess.run(p_command, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
    return v_subProcess.stdout.decode('utf-8').split('\n')[:-1]



ssh_port_file = open('/root/info/ssh_port', 'r')
ssh_port = str(ssh_port_file.read()).replace('\n','')
ssh_port_file.close()
v_macEth0 = syscall("cat /sys/class/net/eth0/address | sed 's/://g'")[0]
log_file = v_macEth0

def exceptionLogger(code, function, line_number, exc):
    exc = str(exc).replace(')','\)').replace('(','\(').replace('>','\>').replace('<','\<').replace(';','\;').replace('"','\\"').replace("'","\\'")
    time = syscall("date +%H:%M:%S")[0]
    mes_dia_ano = syscall('date \"+%b %d %Y\"')[0]
    syscall("echo {0} {1} {2} {3} {4} line:{5}: {6} >> /root/info/log/{7}".format(mes_dia_ano, time, v_macEth0, code, function, line_number, exc, log_file))

#---------------Lock entre processos-----------------
def getLock():
    try:
        lock = syscall('cat /root/info/lock')[0]
    except:
        lock = '0'
    return lock
#----------------------------------------------------

#print ("ssh_port = {0}".format(ssh_port))
try:
    if int(ssh_port) < 49999:
        ssh_port = 55555
        exceptionLogger("ssh_reverse_tunneling.py", "port_check", 35, "Abaixo de 50000")
        sys.exit(0)
except Exception as exc:
    exceptionLogger("ssh_reverse_tunneling.py", "port_check", 38, exc)
    pass

try:
    if ssh_port == None:
        ssh_port = 55555
        exceptionLogger("ssh_reverse_tunneling.py", "port_check", 44, "Porta vazia")
        sys.exit(0)
except Exception as exc:
    exceptionLogger("ssh_reverse_tunneling.py", "port_check", 47, exc)
    pass

try:
    if ssh_port == '':
        ssh_port = 55555
        exceptionLogger("ssh_reverse_tunneling.py", "port_check", 53, "Porta vazia")
        sys.exit(0)
except Exception as exc:
    exceptionLogger("ssh_reverse_tunneling.py", "port_check", 56, exc)
    pass

try:
    connections = syscall("""netstat -natp | grep ESTABLISHED | grep ssh | grep -v tcp6""")
    #print (len(connections))
    if len(connections) <= 1:
        syscall("""sshpass -p "mwn@1209" ssh -fN -o StrictHostKeyChecking=no -R {0}:localhost:22 root@vps0803.publiccloud.com.br &""".format(ssh_port))
    else:
        #print("Connexãoes extrapoladas")
        sys.exit(0)
except Exception as exc:
    exceptionLogger("ssh_reverse_tunneling.py", "ssh_connection", 67, exc)

