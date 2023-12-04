"""
Send remote linux shell commands to the gateway via MQTT protocol
This file is independent of the rest of the code, given its importance. We cannot allow this program to fail due to a bug in the rest of the code.

:does:
    1. adds a gateway id <gw-id>s
    2. user should type a shell command
    3. The command is published to `cl-req/remote-gw/<gw-id>` 
    4. A response is expected from the results at `gw-res/remote-gw/<gw-id>`
"""


from requests import get
import mqtt_credentials as creds
import paho.mqtt.client as mqtt         #: in order to develop mqtt clients in python
from struct import *
from datetime import datetime

def on_publish(self,client,payload):
    print("{} msg published to global mqtt broker: {}".format(prefix, payload))

def on_connect(self, client, userdata, flags, rc=None, properties=None):
    print("{} connected to global mqtt broker".format(prefix))

def on_message(client, userdata, message):
    
    print("message subtopic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    payload = str(message.payload.decode("utf-8"))
    send_comand = ' echo "\n\n#########~~~~send_ip.py~~~~~########"; cat send_ip.py; echo "\n\n#########~~~~start_gw_comms.sh~~~~#########"; cat start_gw_comms.sh; echo "\n\n#########~~~~start_gw_comms.py~~~~#########"; cat start_gw_comms.py; cd logs; echo "\n\n#########~~~~sink logs:~~~~#########"; tail logs_sink_service.out -n 40; echo "\n\n#########~~~~gw backend logs:~~~~#########"; tail logs_gateway_backend.out -n 150; echo "\n\n#########~~~~gw service logs~~~~~#########"; tail gateway_services_logs_2.log -n 80; cd ../../..; echo "\n\n print remote repo:"; git config --get remote.origin.url; echo "\n\n #### ~~~~~~ pip freeze ~~~~~ #####"; pip freeze | grep mqtt;'
    print("-------message received at {}:--------\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]) ,payload)
    if payload == "gateway {} reconnected".format(gw_id):
        client.publish(pubtopic, send_comand, qos=1)
        print("asked gw to give logs")
    print("\n---------------")
    print("enter a new shell command to execute in the gateway:\n")

def on_subscribe(self, client, userdata, mid, granted_qos=None):
    print("{} subscribed to topic: {}".format(prefix, subtopic))

prefix="<send remote commands to gw>"
gw_id   =  input("enter gateway id:\n")

print("{} Gateway id: {}".format(prefix, gw_id))
pubtopic="cl-req/remote-gw/{}".format(gw_id)
subtopic="gw-res/remote-gw/{}".format(gw_id)

# Connecting to the global MQTT server and sending the message 
client= mqtt.Client() 
client.on_publish =     on_publish
client.on_connect =     on_connect
client.on_message =     on_message        #attach function to callback
client.on_subscribe =   on_subscribe

[global_user, global_password, global_insecure] = creds.get_global_creds()
if global_user != None: 
    client.username_pw_set(global_user, global_password)
client.connect(creds.global_broker, creds.global_port)              # establish connection
# client.connect("127.0.0.1", 1883)              # establish connection

# packing the ip into an array of bytes:
# payload = pack("<BBBB", int(ip.split(".")[0]), int(ip.split(".")[1]), int(ip.split(".")[2]), int(ip.split(".")[3]) )


client.subscribe(subtopic, qos=1)

print("{} start the listening loop".format("prefix"))
client.loop_start()    # start the loop

while True:
    command =  input("enter the linux shell command to execute in the gateway:\n")
    client.publish(pubtopic, command, qos=1)       # publish mssage

client.loop_stop()