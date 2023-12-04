#!/bin/bash



if [ $(pidof mosquitto | wc -l) -eq 0 ] ; then
    mosquitto -c /etc/mosquitto/conf.d/default.conf -v
else
    echo "<mosquitto info> " `date` ": mosquitto broker already running"
fi