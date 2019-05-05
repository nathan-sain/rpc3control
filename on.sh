#!/bin/bash
cd /var/homebridge/rpc3control && \
./on.py $1 $2;
echo "ON";
echo "This is flag Switch ON" > /var/homebridge/rpc3control/script$1.flag;
