#!/bin/bash
cd /var/homebridge/rpc3control && \
state=$(./state.py $1 $2);
if [ "$state" = 'True' ]; then
echo $state;
exit 0;
else
echo $state;
exit 1;
fi
