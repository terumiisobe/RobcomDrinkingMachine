#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import sys
import subprocess
import os
import time
from inspect import currentframe, getframeinfo
from datetime import datetime

def syscall(p_command):
    v_subProcess = subprocess.run(p_command, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
    return v_subProcess.stdout.decode('utf-8').split('\n')[:-1]
