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

RPC=None
#RPCUSER= str(sys.argv[2])
RPCUSER= None
RPCPASS=None
OUTLET= int(sys.argv[1])

(RPC, RPCUSER, RPCPASS, WHITELIST) = load_credentials("/var/homebridge/rpc3control/.credentials")

RPCUSER= None
#RPCUSER= str(sys.argv[2])
r = rpc3Control(RPC, RPCUSER)
r.outlet(OUTLET, 'on')
