#!/usr/bin/env python

import sys
from rpc3Control import *

RPC=None
#RPCUSER= str(sys.argv[2])
RPCUSER= None
RPCPASS=None
OUTLET= int(sys.argv[1])

(RPC, RPCUSER, RPCPASS, WHITELIST) = load_credentials("/var/homebridge/rpc3control/.credentials")

#RPCUSER= str(sys.argv[2])
RPCUSER= None
r = rpc3Control(RPC, RPCUSER)
r.outlet(OUTLET, 'off')
