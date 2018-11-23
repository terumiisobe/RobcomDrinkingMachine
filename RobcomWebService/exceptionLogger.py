#!/usr/bin/python3
# -*- coding: utf-8 -*-
from datetime import datetime
from syscall import syscall

log_file = "RobcomLog"

def exceptionLogger(code, function, line_number, exc):
    '''
    Realiza log em arquivo externo no local ../RobcomLog. Auxiliar de debug
    '''
    global v_macEth0
    exc = str(exc).replace(')', '\)').replace('(', '\(').replace('>', '\>').replace('<', '\<').replace(';', '\;').replace(
        '"', '\\"').replace("'", "\\'")
    time = datetime.now().strftime("%H:%M:%S")
    mes_dia_ano = datetime.now().strftime("%b %d %Y")
    syscall("echo {0} {1} {2} {3} line:{4}: {5} >> ../{6}".format(mes_dia_ano, time, code, function,
                                                                                    line_number, exc, log_file))
