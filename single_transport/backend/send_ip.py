"""
This file is independent of the rest of the code, given its importance. We cannot allow this program to fail due to a bug in the rest of the code.

:does:
    1. Gets machine's public Ipv4 IP.
    2. Gets the gateway's id.
    3. Sends the gateway IP public address to the mqtt topic `gw-req/gw-init/<gw-id>`
"""


from requests import get
import mqtt_credentials as creds
import sys
import paho.mqtt.client as mqtt         #: in order to develop mqtt clients in python
from struct import *

try:
    from wirepas_mqtt_library import WirepasNetworkInterface
except ModuleNotFoundError:
    print("Please install Wirepas mqtt library wheel: pip install wirepas-mqtt-library==1.0")
    sys.exit(-1)

def on_publish(client, userdata, mid):
    print("{} msg published to global mqtt broker".format(prefix))

def on_connect(client, userdata, flags, rc):
    """
    On connect is when we are going to send the ip, and actually publish a message to the MQTT broker.
    
    """
    print("{} connected to global mqtt brokerr".format(prefix))
    # packing the ip into an array of bytes:
    payload = pack("<BBBB", int(ip.split(".")[0]), int(ip.split(".")[1]), int(ip.split(".")[2]), int(ip.split(".")[3]) )
    client.publish("gw-req/gw-init/{}".format(gw_id), payload, 1)       # publish mssage


prefix="<send gateway IP and ID>"

# ip = get('https://api.ipify.org').content.decode('utf8')
ip = "0.0.0.0"
print('{} public IP address is: {}'.format(prefix, ip))



[local_user, local_password, global_insecure] = creds.get_local_creds()
wni = WirepasNetworkInterface(
                                creds.local_broker,
                                creds.local_port,
                                local_user,
                                local_password,
                                insecure=creds.local_insecure,
                                strict_mode=True
                                ) #insecure=FALSE implies that a secure connection 
print("{} wni created (in theory) {}".format(prefix, wni))
gws = list(wni.get_gateways())
n = len(gws)
gw_id = gws[0]
print("{} Gateway id: {}".format(prefix, gw_id))
print("{} rest of gw's ids: {}".format(prefix, gws))
try:
    try:
        print("{} first attempt to get sink config".format(prefix))
        sink_list = wni.get_sinks()
        gw_id = sink_list[0][0]
    except:
        print("{} second attempt to get sink config".format(prefix))
        sink_list = wni.get_sinks()
        gw_id = sink_list[0][0]
except:
    print("{} failed to get sink config")
print("{} returned gws and sinks: {}".format(prefix, sink_list))


# Connecting to the global MQTT server and sending the message 
client= mqtt.Client() 
client.on_connect = on_connect
client.on_publish = on_publish


[global_user, global_password, global_insecure] = creds.get_global_creds()
if global_user != None: 
    client.username_pw_set(global_user, global_password)
print("{} About to connect".format(prefix))
client.connect(creds.global_broker, creds.global_port)              # establish connection
print("{} It should have connected now".format(prefix))

# a blocking forever loop is missing here