"""
Simple MQTT chat app
To install, install:
    1. instalar python3
    2. instalar pip3 (seguramente)
    3. Instalar las librerias de python "threading" y "paho" (usando pip3) 
"""

import paho.mqtt.client as mqtt
from threading import Thread
import time
import datetime

lastgot = time.time()
fasties = 0
nolist = ["", " "]
room = input("Type a room to join:\n")
user = input("Type a user name:\n")

def get_timestamp():
    """generate a datetime format date and time which contains up to the milliseconds. This will
    be used throughout my code
    
    :return:
        timestamp (string) -- Current date and time with a format that includes up to the milliseconds
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return timestamp

def start_listen_thread(client):
    """Open a new processing thread for listening to incoming messages.        
    This function calls the :py:meth:`~mqtt_interaction_module.mqtt_interaction.start_listen_thread` in a new thread"""

    client.thread = Thread(target=listen)
    # self.thread.daemon = True
    client.thread.start()
    print("new thread running on background")

def listen():
    client.loop_forever()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(str(room))

def put_to_nolist(user):
    global fasties
    if user not in nolist:
        nolist.append(user)
        print("user: " + user + " expelled from the room for being 'molesto'. :)")
    fasties = 0

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global lastgot
    global nolist
    global fasties
    now = time.time()
    message = (msg.payload).decode("utf8")
    user = message.split(">")[0]
    try:
        text = message.split(">")[1:][0]
    except:
        text = ""
    if user not in nolist:
        hora = get_timestamp()
        print(msg.topic+": "+user + " at " +str(hora) + ": " + str(text))
    
        if (now - lastgot) < 0.3:
                fasties = fasties + 1
        if fasties > 4 or len(message.split(">")) == 1:
            put_to_nolist(user)
        lastgot = now

client = mqtt.Client()

def main():
   
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    start_listen_thread(client) 

    while True:
        message = input("> ")
        payload = user + "> " + message
        client.publish(topic=room, payload = payload)

if __name__ == "__main__":     
    main()