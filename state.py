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
delta_init = 7200000
delta = 7200001

def file_exists(path, filename):
        for file_or_folder in os.listdir(path):
                if file_or_folder == filename:
                        return True
        return False

lock_filename = 'telnetrunning.txt'
fileexists = file_exists("/var/homebridge/rpc3control/", lock_filename)

#I'm using this scriot with homebridge plugin that calls this state file script for every outlet on the RPC3 unit. The RPC unit can only allow for admin user 4 telnet sessions at a time.
#Homekit will call the state script for all 8 outlets and i can't control the order they are called in. And i think  they are called in parallel.
#To minimize telnet sessions to the RPC unit I want the script call for outlet 1 state from homekit to be the only one allowed to create a status file for ALL  outlets state.
#In this script for any outlet other than outlet 1, I wait for the status file to be created by the outlet 1 state script execution from homekit if it does not exist.

if OUTLET != 1:
        i=0
        while (not fileexists and i<=50):
                try:
                        time.sleep(0.05)
                        fileexists = file_exists("/var/homebridge/rpc3control/", lock_filename)
                        i=i+1
                except:
                        raise

#if the status file already exists then I pull the state from the status file unless it has recently been updated by the on and off scripts for individual outlets.
#I do this to confirm that the on off commands actually worked. So if the status file was recently updated by and on off command i telnet in and get outlet status
#I also recheck outlet states from the RPC3 unit if it's been over 2 hours since the last telnet and status check on the unit.
if (fileexists):
        with open(lock_filename,'r') as my_file:
                while True:
                        try:
                                fcntl.flock(my_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
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
        delta = int(round(time.time() * 1000)) - int(statearray[0][0])
        status = statearray[OUTLET][1]
        #if it's been less than 2 hours since the last status check and if the status file does not have the updated flag marked, i skip telneting and just pull status from the status file.
        if (delta <= delta_init and statearray[0][1]!="updated"):
                print status

#Only outlet 1 is alloed to telnet and check/confirms updated status. It updates the status file with latest settings if the status file  was recently updated (doublechecking that the update succeed$
#It will also telnet in and upadte status if it's been over 2 hours since the last time the status file was updated
if ((delta > delta_init or statearray[0][1]=="updated") and OUTLET == 1):
        (RPC, RPCUSER, RPCPASS, WHITELIST) = load_credentials("/var/homebridge/rpc3control/.credentials")
        #RPCUSER = str(sys.argv[2])
        RPCUSER = None
        r = rpc3Control(RPC, RPCUSER)
        (status,name) = r.outlet_status(OUTLET)
        if (status == "True"):
                print status
        else:
                print status
#Outlets other than outlet 1  should get latest update from status file as outlet 1 status file update  may have updated things. see if statement above.
if ((delta > delta_init or statearray[0][1]=="updated") and OUTLET != 1):
        with open(lock_filename,'r') as my_file:
                while True:
                        try:
                                fcntl.flock(my_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
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
        status = statearray[OUTLET][1]
        print status
