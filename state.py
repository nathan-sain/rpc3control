#!/usr/bin/env python

import sys
import re
import syslog
import time
import os
import errno
import datetime
import fcntl
from rpc3Control import *

RPC = None
#RPCUSER= str(sys.argv[2])
RPCUSER= None
RPCPASS = None
OUTLET = int(sys.argv[1])
delta = 701

def file_exists(path, filename):
        for file_or_folder in os.listdir(path):
                if file_or_folder == filename:
                        return True
        return False

lock_filename = 'telnetrunning.txt'
fileexists = file_exists("/var/homebridge/rpc3control/", lock_filename)
if fileexists:
        with open(lock_filename,'ra') as my_file:
                while True:
                        try:
                                #print "trying"
                                fcntl.flock(my_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                                #print "locked"
                                break
                        except IOError as e:
                                # raise on unrelated IOErrors
                                if e.errno != errno.EAGAIN:
                                        raise
                                else:
                                        time.sleep(0.05)
                statearray = [line.split(',') for line in my_file]
                fcntl.flock(my_file, fcntl.LOCK_UN)
        my_file.close()
        delta = int(round(time.time() * 100)) - int(statearray[0][0])
        if delta <= 700:
                status = statearray[OUTLET][1]
                print status

if delta > 700:
        (RPC, RPCUSER, RPCPASS, WHITELIST) = load_credentials("/var/homebridge/rpc3control/.credentials")
        #RPCUSER = str(sys.argv[2])
        RPCUSER = None
        r = rpc3Control(RPC, RPCUSER)
        (status,name) = r.outlet_status(OUTLET)

        if (status == "True"):
                print status
        else:
                print status
