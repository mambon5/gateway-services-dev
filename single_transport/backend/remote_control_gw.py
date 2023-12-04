"""
Receive, process and respond to remote commands send from the cloud to the gateway via MQTT protocol
This file is independent of the rest of the code, given its importance. We cannot allow this program to fail due to a bug in the rest of the code.

:does:
    1. Gets machine's public Ipv4 IP.
    2. Gets the gateway's id.
    3. Listens to messages published at `cl-req/remote-gw/<gw-id>` and interprets them as linux shell commands
    4. Executes the <command>.
    5. Returns the results to `gw-res/remote-gw/<gw-id>`
"""


from requests import get
import mqtt_credentials as creds
import sys
import paho.mqtt.client as mqtt         #: in order to develop mqtt clients in python
from struct import *
import subprocess
 


try:
    from wirepas_mqtt_library import WirepasNetworkInterface
except ModuleNotFoundError:
    print("Please install Wirepas mqtt library wheel: pip install wirepas-mqtt-library==1.0")
    sys.exit(-1)

def on_publish(self,client,payload):
    print("{} msg published to global mqtt broker".format(prefix))

def on_connect(client, userdata, flags, rc=None, properties=None):
    print("{} connected to global mqtt broker".format(prefix))
    client.subscribe(subtopic, qos=1)
    print("{} start the listening loop".format("prefix"))
    client.publish(pubtopic, "gateway {} reconnected".format(gw_id), qos=1)
    
   
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message subtopic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    print("{} running cloud command on terminal...".format(prefix))
    output = subprocess.run([message.payload.decode("utf-8")], shell=True, capture_output=True, text=True)
    client.publish(pubtopic, output.stderr + "\n"+ output.stdout, qos=1)       # publish mssage

   

def on_subscribe(self, client, userdata, mid, granted_qos=None):
    print("{} subscribed to topic: {}".format(prefix, subtopic))

prefix="<remote control>"

# ip = get('https://api.ipify.org').content.decode('utf8')
# print('{} public IP address is: {}'.format(prefix, ip))

[local_user, local_password, global_insecure] = creds.get_local_creds()
wni = WirepasNetworkInterface(
                                creds.local_broker,
                                creds.local_port,
                                local_user,
                                local_password,
                                insecure=creds.local_insecure,
                                strict_mode=True
                                ) #insecure=FALSE implies that a secure connection 


# now getting the real gateway using the get_sinks() function
gw_id = None
gws = list(wni.get_gateways())
n = len(gws)
gw_id = gws[n-1]
print("{} Gateway id: {}".format(prefix, gw_id))
print("{} rest of gw's ids: {}".format(prefix, gws))
try:
    try:
        print("{} first attempt to get sink config".format(prefix))
        sink_list = wni.get_sinks()
        gw_id = sink_list[0][0]
        print("{} real gateway id: {}".format(prefix, gw_id))

    except:
        print("{} second attempt to get sink config".format(prefix))
        sink_list = wni.get_sinks()
        gw_id = sink_list[0][0]
        print("{} real gateway id: {}".format(prefix, gw_id))

except:
    # if gateway has no sink, use just the first gateway name it can find
    gws = list(wni.get_gateways())
    n = len(gws)
    try:
        gw_id = gws[n-1]
        print("{} Gateway id: {}".format(prefix, gw_id))
    except:
        print("{} no valid gw id found".format(prefix))
    print("{} failed to get sink config, using default gateway id value {}".format(prefix, gw_id))

subtopic="cl-req/remote-gw/{}".format(gw_id)
pubtopic="gw-res/remote-gw/{}".format(gw_id)



# Connecting to the global MQTT server and sending the message 
client= mqtt.Client() 
client.on_publish =     on_publish
client.on_connect =     on_connect
client.on_message =     on_message        #attach function to callback
client.on_subscribe =   on_subscribe

print("{} basic functions set".format(prefix))

[global_user, global_password, global_insecure] = creds.get_global_creds()
if global_user != None: 
    client.username_pw_set(global_user, global_password)

client.will_set(pubtopic, "gateway {} disconnected".format(gw_id), 0, False)
client.connect(creds.global_broker, creds.global_port, keepalive=6000)              # establish connection
# client.connect("127.0.0.1", 1883)              # establish connection
# packing the ip into an array of bytes:
# payload = pack("<BBBB", int(ip.split(".")[0]), int(ip.split(".")[1]), int(ip.split(".")[2]), int(ip.split(".")[3]) )
# client.publish("gw-req/gw-init/{}".format(gw_id), payload, 1)       # publish mssage
client.loop_forever()    #start the loop
