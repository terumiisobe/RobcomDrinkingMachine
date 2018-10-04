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

try:
    connections = syscall("""netstat -natp | grep ESTABLISHED | grep ssh | grep -v tcp6""")
    #print (len(connections))
    if len(connections) <= 1:
        syscall("""sshpass -p "mwn@1209" ssh -fN -o StrictHostKeyChecking=no -R 30001:localhost:22 root@vps0803.publiccloud.com.br &""")
    else:
        #print("Connexãoes extrapoladas")
        sys.exit(0)
except Exception as exc:
    exceptionLogger("ssh_reverse_tunneling.py", "ssh_connection", 67, exc)

