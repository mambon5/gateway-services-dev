"""
Starts the interaction of the gateway with the nodes. It creates the user interface (in the terminal) for sending and receiving messages 
to/from the mesh network, respectively.
The interface is in the terminal and allows to select **one** of the following mqtt interaction modes:

    1.  Gateway listens to mesh network messages
    2.  Gateway sends requests to the mesh network

    In order to start any of the 2 interactions listed here, we should:

    - select an interaction mode (either *request* or *listen*)
    - create an interaction with the nodes, using the :class:`mqtt_interaction_node_main <mqtt_interaction_node_main.mqtt_interaction_node_main>` class 
      or the :class:`mqtt_interaction_node_temporal <mqtt_interaction_node_temporal.mqtt_interaction_node_temporal>` class, depending
      on the nature of the interaction. The *node main* class is more permanent and is supposed to constantly listen for any message from the nodes. While
      the *node temporal class* is designed to be created and destroyed instantaneosuly, and just used for tunneling a message from the cloud to the node. 
      It is created as a necessary way of sending the message form the gateway to the node in order to complete the cloud > node tunnel.
    
    Finally, the following is triggered depending on the interaction mode (listen or send):

    - *for listen modes*: the subscription sub loop starts
    - *for send modes*: the send message function is called.

    :references: We followed this guide to install the python backend to the gateway > https://developer.wirepas.com/support/solutions/articles/77000487992-how-to-communicate-with-a-wirepas-network-using-wirepas-gateway-ap 
    in order to know how to create a python backend to talk to the nodes.
"""

from struct import *
import local_settings as settings       # to import some global variables than we need to keep updated even if gateway stops
import global_vars as gvar              # import global variables
import database_functions as db_fs      # import functions for writing and reading of messages to/from the database

from mqtt_interaction_node_main import mqtt_interaction_node_main 
from mqtt_interaction_cloud import mqtt_interaction_cloud 
# from mqtt_interaction_module import mqtt_interaction_cloud 


"""
==== Script global variable ====
"""

#: interaction modes:
GW_REQUEST_TO_NODES = "request to nodes"
GW_LISTEN_TO_NODES = "listen to nodes"
GW_LISTEN_TO_NODES_RAW_DATA = "listen to nodes -raw_data"
FAKE_NODE_LISTENER = "fake node listener"
FAKE_NODE_REQUESTER = "fake node requester (doesn't work, can't fully simulate wirepas message)"

#: different interaction modes with the nodes
MODE_LIST = [GW_REQUEST_TO_NODES, GW_LISTEN_TO_NODES, GW_LISTEN_TO_NODES_RAW_DATA, FAKE_NODE_LISTENER, FAKE_NODE_REQUESTER]

FILE_SETTINGS = "local_settings.py"
#: get the current message id, saved in file "settings"
message_id = settings.msg_id

# path to gateway database:
#: DB_PATH = "/home/roma/smartec/gateway-services/single_transport/backend/bbdd/"
DB_PATH = db_fs.DB_PATH
#: name of database:
DB_NAME = db_fs.DB_NAME

datab = DB_PATH + DB_NAME

#table names:
TABLE_SUCCESS = db_fs.TABLE_SUCCESS
TABLE_FAILS = db_fs.TABLE_FAILS
TABLE_REQUESTS_SENT = db_fs.TABLE_REQUESTS_SENT
TABLE_RECEIVED_RESPONSES = db_fs.TABLE_RECEIVED_RESPONSES

#: save messages information to db or not
save_messages = 0

def run_node_comunications(mode="", wni=None, node_list = []):
    """
    Starts the interaction with the mesh net. It allows the user to select a mode.
    
    :does:

        1. You select a mode of the 5 available
        2. then a :class:`mqtt_interaction_node_main <mqtt_interaction_node_main.mqtt_interaction_node_main>` or 
           :class:`mqtt_interaction_cloud <mqtt_interaction_cloud.mqtt_interaction_node_main>` class is created
        3. Depending on the mode selected (*listen* or *request*) the function *.listen()* or *.send_message()*
           are called.
    
    """

    if mode == "":
        # user selects mqtt mode:
        print("select an interaction type with the nodes:")
        mode = gvar.display_and_set_interaction_mode(MODE_LIST)
    else :
        # mode already supplied
        print("input already supplied when calling this function")

    mode = MODE_LIST[mode]
    print("mode selected: " + mode)
    # main script -> publish/subscribe details:

    if mode == GW_REQUEST_TO_NODES:
        inter = mqtt_interaction_node_main(mode="request", wni=wni, node_list = node_list)        
        inter.send_message()
    
    elif mode == GW_LISTEN_TO_NODES or mode == GW_LISTEN_TO_NODES_RAW_DATA:
        print("listen to nodes")
        inter = mqtt_interaction_node_main(mode="listen", wni=wni, node_list = node_list)
        if mode == GW_LISTEN_TO_NODES_RAW_DATA:
            inter.print_raw_data = True
        inter.listen()

    # doesn't really work, because i can't simulate the entire message that wirepass receives either:
    elif mode == FAKE_NODE_LISTENER:
        inter = mqtt_interaction_cloud(
         subtopic="gw-request/#",
         pubtopic="gw-event/received_data/"+ gvar.gw_id +"/"+ gvar.sink +"/5/1/1", mode="listen", wni=wni)
        #          gw-event/received_data/  <gw-id>       /    <sink-id>/<net_id>/<src_ep>/<dst_ep>
        inter.listen()
    # run this mosquitto sub instead:
    # mosquitto_sub -P all_I_want_for_christmas_is_you -u roma_masana -h 127.0.0.1 -p 1883 -t gw-request/send_data/2486247681457/sink0

    # doesn't really work, because i can't simulate the entire message that wirepass publishes:
    elif mode == FAKE_NODE_REQUESTER:
        inter = mqtt_interaction_cloud(  
         subtopic="gw-request/#",
         pubtopic="gw-event/received_data/"+ gvar.gw_id +"/"+ gvar.sink +"/5/1/1", mode="request", wni=wni)
        inter.send_message()
    else :
        print("error: Unrecognized mode selected!")  
        return

def main():
    run_node_comunications()

if __name__ == "__main__":
    main()

