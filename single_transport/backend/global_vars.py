"""
Most used variables and functions throughout all the gateway's code. Any script uses or can use them. 
These simple functions included here include those that:

- unpack messages to bytes *(the packing to bytes is done in the send_message_function)*
- compute the CRC of a message
- extract a supertopic 
- create the Wirepas Network Interface
- create the OtapHelper
- get sink and gateway ids
- select element from the list
- and more

these functions are indiscriminately used 
in many classes, functions and files throughout the gateway backend app.
"""

import pathlib
from struct import * #: for pack and unpacking functions
import datetime                 #: to create timestamp for sent and received messages
import mqtt_credentials as creds
import sys
import time
try:
    from wirepas_mqtt_library import WirepasNetworkInterface, WirepasOtapHelper
except ModuleNotFoundError:
    print("Please install Wirepas mqtt library wheel: pip install wirepas-mqtt-library==1.0")
    sys.exit(-1)

#: Gateway's sink default network channel. This will be the default network channel to be used by the sinks of the gateway we put
#: this number is very improtant because in order to activate all the sinks of a gateway, we must specify the network channel first
#: the python scripts that activate automatically the sinks, use this value to detect the sinks connected to the network that we 
#: want to activate. So far, we decided to use network channel 5
NETWORK_DEFAULT_CHANNEL = 5

#: Message ID of Gateway Backend to Node communications:
MSG_TYPE_ERROR = 0

#: VERSION OF THE GATEWAY SOFTWARE WITH FORMAT "MAJOR.MINOR.REVISION.BUILDNUMBER"
#: MAJOR is a major release (usually many new features or changes to the UI or underlying OS)
#: MINOR is a minor release (perhaps some new features) on a previous major release
#: REVISION is usually a fix for a previous minor release (no new functionality)
#: BUILDNUMBER is incremented for each latest build of a revision.
GATEWAY_VERSION="0.2.3.0"
# major_release.minor_release.revision_fixes.build_number

#: GATEWAY TO NODE REQUESTS
#: "Set led On" message type.
MSG_TYPE_GW_SET_LED_ON = 1
#: "Set led Off" message
MSG_TYPE_GW_SET_LED_OFF = 2
MSG_TYPE_GW_SET_DIMMING = 3
MSG_TYPE_GW_SET_BLINKING = 4
MSG_TYPE_GW_SET_STRATEGY = 5

#: Get information messages from Gateway to node:
#: "send echo command" message type.
MSG_TYPE_GW_ECHO = 6
#: get led status
MSG_TYPE_GW_GET_LED_STATUS = 7
#: get dimming status
MSG_TYPE_GW_GET_DIMMING_STATUS = 8
#: get number of neighbours
MSG_TYPE_GW_GET_NUMBER_OF_NEIGHBOURS = 9
#: get rssi node signal strength
MSG_TYPE_GW_GET_RSSI = 10
#: get number of jumpts of the node until it reaches the sink
MSG_TYPE_GW_GET_HOPS = 11
#: get node status
MSG_TYPE_GW_GET_NODE_STATUS = 12
#: get new strategy
MSG_TYPE_GW_SEND_NEW_STRAGEGY = 13


#:list of different responses recieved by gw from node:
MSG_RESPONSE_RECEIVED_FROM_NODES_LIST = [
MSG_TYPE_ERROR,
MSG_TYPE_GW_SET_LED_ON ,
MSG_TYPE_GW_SET_LED_OFF,
MSG_TYPE_GW_SET_DIMMING,
MSG_TYPE_GW_SET_BLINKING,
MSG_TYPE_GW_SET_STRATEGY,
MSG_TYPE_GW_ECHO,
MSG_TYPE_GW_GET_LED_STATUS,
MSG_TYPE_GW_GET_DIMMING_STATUS,
MSG_TYPE_GW_GET_NUMBER_OF_NEIGHBOURS,
MSG_TYPE_GW_GET_RSSI,
MSG_TYPE_GW_GET_NODE_STATUS,
MSG_TYPE_GW_SEND_NEW_STRAGEGY
]


#: do we want to use this message id? the wirepas guys defined it in the original app?:
#: Unknown or unsupported message ID value.
MSG_TYPE_INVALID_UNSUPPORTED_MSG = -1


#: NODE to GATEWAY REQUESTS
#: "get time from connected gateway" message ID.
MSG_TYPE_NODE_GET_TIME = 201
#: send alarm
MSG_TYPE_NODE_SEND_ALARM = 202
#: send current node voltage to gateway
MSG_TYPE_NODE_SEND_CURRENT_VOLTAGE = 203
#: send current node electric parameters to gateway
MSG_TYPE_NODE_SEND_ELECTRIC_PARAMETERS = 204
#: send current node solar panel metrics to gateway
MSG_TYPE_NODE_SEND_SOLAR_PANEL_METRICS = 205
#: send node status to gateway
MSG_TYPE_NODE_SEND_NODE_STATUS = 206


#: list of node started messages or requeststs
MSG_NODE_REQUESTS_LIST = [
MSG_TYPE_NODE_GET_TIME,
MSG_TYPE_NODE_SEND_ALARM,
MSG_TYPE_NODE_SEND_CURRENT_VOLTAGE,
MSG_TYPE_NODE_SEND_ELECTRIC_PARAMETERS,
MSG_TYPE_NODE_SEND_SOLAR_PANEL_METRICS,
MSG_TYPE_NODE_SEND_NODE_STATUS
]


# CLOUD to NODE REQUESTS
#commands
#: cloud sends SET LED ON command to node
MSG_TYPE_CLOUD_TO_NODE_SET_LED_ON = 1
#: cloud sends SET LED OFF command to node
MSG_TYPE_CLOUD_TO_NODE_SET_LED_OFF = 2
#: cloud sends SET DIMMING command to node
MSG_TYPE_CLOUD_TO_NODE_SET_DIMMING = 3
#: cloud sends SET BLINKING command to node
MSG_TYPE_CLOUD_TO_NODE_SET_BLINKING = 4
#: cloud sends SET STRATEGY command to node
MSG_TYPE_CLOUD_TO_NODE_SET_STRATEGY = 5

# info messages
#: cloud sends GET TRAVELTIME command to node
MSG_TYPE_CLOUD_TO_NODE_ECHO = 6
#: cloud sends GET LED STATUS command to node
MSG_TYPE_CLOUD_TO_NODE_GET_LED_STATUS = 7
#: cloud sends GET DIMMING STATUS command to node
MSG_TYPE_CLOUD_TO_NODE_GET_DIMMING_STATUS = 8
#: cloud sends GET NUMBER OF NEIGHBOURS command to node
MSG_TYPE_CLOUD_TO_NODE_GET_NUMBER_OF_NEIGHBOURS = 9
#: cloud sends GET RSSI command to node
MSG_TYPE_CLOUD_TO_NODE_GET_RSSI = 10
#: cloud sends GET NUMBER OF HOPS command to node
MSG_TYPE_CLOUD_TO_NODE_GET_HOPS = 11
#: cloud sends GET ALL NODE STATUS VALUES command to node
MSG_TYPE_CLOUD_TO_NODE_GET_NODE_STATUS = 12
#: cloud sends GET USED STRATEGY NUMBER command to node
MSG_TYPE_CLOUD_TO_NODE_SEND_NEW_STRAGEGY = 13
#: cloud sends GET NODE VERSION command to node
MSG_TYPE_CLOUD_TO_NODE_GET_VERSION = 14

#: LIST OF valid message types
MSG_CLOUD_TO_NODE_REQUESTS_LIST = [
MSG_TYPE_CLOUD_TO_NODE_SET_LED_ON,
MSG_TYPE_CLOUD_TO_NODE_SET_LED_OFF,
MSG_TYPE_CLOUD_TO_NODE_SET_DIMMING,
MSG_TYPE_CLOUD_TO_NODE_SET_BLINKING,
MSG_TYPE_CLOUD_TO_NODE_SET_STRATEGY,
MSG_TYPE_CLOUD_TO_NODE_ECHO ,
MSG_TYPE_CLOUD_TO_NODE_GET_LED_STATUS,
MSG_TYPE_CLOUD_TO_NODE_GET_DIMMING_STATUS,
MSG_TYPE_CLOUD_TO_NODE_GET_NUMBER_OF_NEIGHBOURS ,
MSG_TYPE_CLOUD_TO_NODE_GET_RSSI,
MSG_TYPE_CLOUD_TO_NODE_GET_HOPS,
MSG_TYPE_CLOUD_TO_NODE_GET_NODE_STATUS,
MSG_TYPE_CLOUD_TO_NODE_SEND_NEW_STRAGEGY,
MSG_TYPE_CLOUD_TO_NODE_GET_VERSION
]

# CLOUD to GATEWAY REQUESTS
# commands
#: cloud sends SET ALL LEDS ON command to gateway (COMMAND not used anymore)
# MSG_TYPE_CLOUD_TO_GATEWAY_ALL_LED_ON = 1        # <-- we decided not to use this message type
# MSG_TYPE_CLOUD_TO_GATEWAY_ALL_LED_OFF = 2       # <-- we decided not to use this message type
# MSG_TYPE_CLOUD_TO_GATEWAY_ALL_DIMMING = 3       # <-- we decided not to use this message type
# get info
#: send request to get the node list
MSG_TYPE_CLOUD_TO_GATEWAY_NODE_LIST = 4
#: send request to get the node status
# MSG_TYPE_CLOUD_TO_GATEWAY_NODE_STATUS = 5       # <-- we decided not to use this message type
#: tell gateway to remove nodes
MSG_TYPE_CLOUD_TO_GATEWAY_REMOVE_NODES = 6
#: tell gateway to update its software
MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_GATEWAY = 7
#: tell gateway to update its nodes using OTAP
MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_NODES = 8
#: ask gateway its software version
MSG_TYPE_CLOUD_TO_GATEWAY_GET_GATEWAY_VERSION = 9


#: list of valid messages from cloud to gateway
MSG_CLOUD_TO_GATEWAY_REQUESTS_LIST = [
# MSG_TYPE_CLOUD_TO_GATEWAY_ALL_LED_ON,       # <-- we decided not to use this message type
# MSG_TYPE_CLOUD_TO_GATEWAY_ALL_LED_OFF,       # <-- we decided not to use this message type
# MSG_TYPE_CLOUD_TO_GATEWAY_ALL_DIMMING,       # <-- we decided not to use this message type
#: get info
MSG_TYPE_CLOUD_TO_GATEWAY_NODE_LIST,
# MSG_TYPE_CLOUD_TO_GATEWAY_NODE_STATUS,       # <-- we decided not to use this message type
MSG_TYPE_CLOUD_TO_GATEWAY_REMOVE_NODES,
MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_GATEWAY,
MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_NODES,
MSG_TYPE_CLOUD_TO_GATEWAY_GET_GATEWAY_VERSION 
]

# GATEWAY TO CLOUD MESSAGE TYPES
MSG_TYPE_ALIVE_GW_TO_CLOUD = 1          #: gw tells its id to cloud
MSG_TYPE_ADD_NODES_GW_TO_CLOUD = 2      #: gw tells cloud to add some new nodes associated to this gateway
MSG_TYPE_UNSEEN_NODES_GW_TO_CLOUD = 3   #: gw tells cloud there are some nodes it doesnt see anymore
MSG_TYPE_NODE_STATUS_GW_TO_CLOUD = 4    #: gw tells cloud the node status of its nodes
MSG_TYPE_ALARM_GW_TO_CLOUD = 5          #: gw sends an alarm to the cloud
MSG_TYPE_ELECTRIC_PARAMETERS_GW_TO_CLOUD = 6    #: gw tells cloud the electrical parameters of its associated nodes

#: gateway to cloud list of valid message types
MSG_GATEWAY_TO_CLOUD_LIST = [
    MSG_TYPE_ALIVE_GW_TO_CLOUD,
    MSG_TYPE_ADD_NODES_GW_TO_CLOUD,
    MSG_TYPE_UNSEEN_NODES_GW_TO_CLOUD,
    MSG_TYPE_NODE_STATUS_GW_TO_CLOUD,
    MSG_TYPE_ALARM_GW_TO_CLOUD,
    MSG_TYPE_ELECTRIC_PARAMETERS_GW_TO_CLOUD
]

#expected message lengths:
#: error msg expected length:
EXPECTED_LENGTH_ERROR = 4

#: EXPECTED LENGTH NODE RESPONSE TO GATEWAY
#: NODE RESONSE TO GATEWAY
EXPECTED_LENGTH_NO_ARGUMENTS = 3
#: "SET DIMMING REPONSE" expected byte length.
EXPECTED_LENGTH_SET_DIMMING_RESPONSE_MSG = 4
#: "SET STRATEGY REPONSE" expected byte length.
EXPECTED_LENGTH_SET_STRATEGY_RESPONSE_MSG = 4
#: "SET STRATEGY REPONSE" expected byte length.
EXPECTED_LENGTH_SEND_ECHO_RESPONSE_MSG_FROM_NODE = 7
#: "get led status REPONSE" expected byte length.
EXPECTED_LENGTH_GET_LED_STATUS_RESPONSE_MSG = 4
#: "get dimming status REPONSE" expected byte length.
EXPECTED_LENGTH_GET_DIMMING_STATUS_RESPONSE_MSG = 4
#: "get number of neighbours REPONSE" expected byte length.
EXPECTED_LENGTH_GET_NUMBER_OF_NEIGHBOURS_RESPONSE_MSG = 7
#: "get rssi REPONSE" expected byte length.
EXPECTED_LENGTH_GET_RSSI_RESPONSE_MSG = 4
EXPECTED_LENGTH_GET_HOPS_RESPONSE_MSG = 4
#: "get NODE status REPONSE" expected byte length for mesh network
EXPECTED_LENGTH_GET_NODE_STATUS_RESPONSE_MSG_MESH_NETWORK = 10
EXPECTED_LENGTH_GET_NEW_STRATEGY_RESPONSE_MSG_MESH_NETWORK = 35

# expected length for NODE REQUESTS TO GATEWAY:
EXPECTED_LENGTH_NODE_TO_GATEWAY_GET_TIME_REQUEST = 3                #: expected message length for node GET TIME request to gateway
EXPECTED_LENGTH_NODE_TO_GATEWAY_ALARM_REQUEST = 4                   #: expected message length for node send ALARM to gateway
EXPECTED_LENGTH_NODE_TO_GATEWAY_CURRENT_VOLTAGE_REQUEST = 8         #: expected message length for node send CURRENT & VOLTAGE to gateway
EXPECTED_LENGTH_NODE_TO_GATEWAY_ELECTRIC_PARAMETERS_REQUEST = 15    #: expected message length for node send ELECTRIC PARAMETERS to gateway
EXPECTED_LENGTH_NODE_TO_GATEWAY_SOLAR_METRICS_REQUEST = 7           #: expected message length for node send SOLAR METRICS to gateway
EXPECTED_LENGTH_NODE_TO_NODE_STATUS_REQUEST = 10                    #: expected message length for node send ALL NODE STATUS VALUES to gateway

# EXPECTED MSG LENGTH CLOUD REQ TO NODE
EXPECTED_LENGTH_SET_DIMMING_REQUEST_MSG = EXPECTED_LENGTH_SET_DIMMING_RESPONSE_MSG
EXPECTED_LENGTH_SET_STRATEGY_REQUEST_MSG = EXPECTED_LENGTH_SET_STRATEGY_RESPONSE_MSG
EXPECTED_LENGTH_CLOUD_TO_NODE_GET_VERSION_REQUEST = 3


# EXPECTED MSG LENGTH CLOUD REQ TO GATEWAY
EXPECTED_LENGTH_ALL_LED_ON_CLOUD_TO_GATEWAY_REQUEST = 7
EXPECTED_LENGTH_ALL_LED_OFF_CLOUD_TO_GATEWAY_REQUEST = 7
EXPECTED_LENGTH_ALL_DIMMING_CLOUD_TO_GATEWAY_REQUEST = 8
EXPECTED_LENGTH_NODE_LIST_CLOUD_TO_GATEWAY_REQUEST = 7
EXPECTED_LENGTH_NODE_STATUS_CLOUD_TO_GATEWAY_REQUEST = 7
EXPECTED_LENGTH_UPDATE_GW_SOFTWARE_CLOUD_TO_GATEWAY_REQUEST = 3
EXPECTED_LENGTH_UPDATE_NODES_SOFTWARE_CLOUD_TO_GATEWAY_REQUEST = 3
EXPECTED_LENGTH_GET_GW_VERSION_CLOUD_TO_GATEWAY_REQUEST = 3

#: CLOUD RESPONSE TO GATEWAY REQUEST
#: "get dimming status REPONSE" expected byte length.
EXPECTED_LENGTH_CLOUD_RESPONSE_TO_GATEWAY_ADD_NODES_REQUEST_MSG = 7
#: "get number of neighbours REPONSE" expected byte length.
EXPECTED_LENGTH_CLOUD_RESPONSE_TO_GATEWAY_REMOVE_NODES_REQUEST_MSG = 7
#: "get rssi REPONSE" expected byte length.
EXPECTED_LENGTH_CLOUD_RESPONSE_TO_GATEWAY_NODE_STATUS_REQUEST_MSG = 7
#: "get number of hops REPONSE" expected byte length.
EXPECTED_LENGTH_CLOUD_RESPONSE_TO_GATEWAY_ALARM_REQUEST_MSG = 8
#: "get NODE status REPONSE" expected byte length.
EXPECTED_LENGTH_CLOUD_RESPONSE_TO_GATEWAY_CONSUMS_REQUEST_MSG = 7

#: GATEWAY RESPONSE TO CLOUD TO NODE
EXPECTED_LENGTH_GET_NODE_STATUS_RESPONSE_MSG_CLOUD = 11
EXPECTED_LENGTH_GET_NODE_VERSION_RESPONSE_MSG_CLOUD = 11
EXPECTED_LENGTH_GET_GATEWAY_VERSION_RESPONSE_MSG_CLOUD = 7



# Error types
ERROR_TYPE_UNRESPONSIVE_DRIVER = 1                  #: unresponsive driver
ERROR_TYPE_UNRESPONSIVE_NODE = 2                    #: unresponsive node
ERROR_TYPE_NODE_ROM_FULL = 3                        #: node rom is full
ERROR_TYPE_GATEWAY_ROM_FULL = 4                     #: gateway ROM is full
ERROR_TYPE_GATEWAY_DATABASE_CONNECTION_ERROR = 5    #: database connection error
ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH = 6            #: unexpected message length
ERROR_TYPE_PARAMETERS_OUT_OF_RANGE = 7              #: parameters out of range
ERROR_TYPE_NODE_NOT_IN_GATEWAY = 8                  #: node not in gateway node list
ERROR_TYPE_INVALID_CRC = 9                          #: invalid CRC
ERROR_TYPE_STRATEGY_NOT_FOUND = 10                  #: strategy not found
ERROR_TYPE_WHEN_UPDATING_DATABASE = 11              #: error when updating database
ERROR_TYPE_WHEN_READING_DATABASE = 12               #: error when reading database
ERROR_TYPE_WHEN_UPDATING_GW_SOFTWARE = 13           #: while updating gateway software
ERROR_TYPE_WHEN_TUNNELING_TO_NODE = 14              #: when tunneling to node
ERROR_TYPE_INVALID_MSG_TYPE = 15                    #: invalid message type
ERROR_TYPE_PAYLOAD_NOT_IN_BYTES = 16                #: payload not in bytes
ERROR_TYPE_INVALID_MSG_ORIGIN_MQTT_TOPIC = 17       #: invalid mqtt topic
ERROR_TYPE_OTAP_FAILED = 18                         #: OTAP failed
ERROR_TYPE_WHEN_TUNNELING_TO_CLOUD = 19             #: when tunneling to the cloud


def expected_length_node_list(num_nodes, head_length=9): 
    """expected length for gateway response to cloud requests:"""
    return head_length + 8*num_nodes   


def expected_length_node_status_list(num_nodes):
    """expected length node status list:"""
    return 5 + 16*num_nodes


def expected_length_alarm_node_list(num_nodes):
    """alarm with nodes"""
    return 6 + 8*num_nodes


def expected_length_node_consum_list(num_nodes):
    """expected length node consumption list:"""
    return 5 + 20*num_nodes

def expected_length_cloud_to_gw_remove_nodes(num_nodes):
    """expected length remove nodes, cloud to gateway req"""
    return 5 + 8*num_nodes


#: LED is switched OFF.
LED_STATE_OFF = 0
#: LED is switched ON.
LED_STATE_ON = 1



#: List of all supported message ID gateway <> node
MSG_SUPPORTED_LIST_NODE = MSG_RESPONSE_RECEIVED_FROM_NODES_LIST + MSG_NODE_REQUESTS_LIST + MSG_GATEWAY_TO_CLOUD_LIST
#: List of all supported message ID gateway <> cloud
MSG_SUPPORTED_LIST_CLOUD = MSG_CLOUD_TO_NODE_REQUESTS_LIST + MSG_CLOUD_TO_GATEWAY_REQUESTS_LIST + MSG_GATEWAY_TO_CLOUD_LIST

""" Application payload endianness."""
MSG_PAYLOAD_ENDIANNESS = "little" #: for using int.to_bytes( , MSG_PAYLOAD_ENDIANNESS)
MSG_PAYLOAD_ENDIANNESS_v2 = "<"     #: for using pack("<b", number) for the same purpose
    
#: Endpoint where data coming from node running the evaluation application are expected.
UPLINK_PACKET_EVAL_APP_ENDPOINT = 1


# SETTINGS FILE/MODULES
FILE_SETTINGS_LOCAL = "local_settings.py" #: file where the local message id is stored
FILE_SETTINGS_GLOBAL = "cloud_settings.py" #: file where the global message id is stored


#: interaction variables (to be deleted in production)
# sink= "sink0"
# node_id="1195333106"
#: wirepass address for a broadcast to all nodes
broadcast_address="0xFFFFFFFF"         
# node_id="1767199611"
# node_id="2727"
# node_id="31415"
# gw_id="193853683731279"

# mqtt super topics:
#: cloud requests to a specific node
CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC=                          "cl-req/n/"
#: cloud requests to a gateway
CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC=                       "cl-req/gw/"
#: gateway response to a cloud request to a specific node
GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC =     "gw-res/n/"
#: gateway responds to a cloud request to the gateway
GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC =  "gw-res/gw/"
#: gateway makes a request to the cloud
GATEWAY_REQUEST_TO_CLOUD_MQTT_SUPERTOPIC=                       "gw-req/gw/"
#: cloud responds to the previous request the gateway made
CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_SUPERTOPIC=             "cl-res/gw/"
#: node requests something to the gateway:
NODE_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC =                       "gw-event/received_data/"
#: gateway connected to cloud topic:
GATEWAY_CONNECTED_MSG_MQTT_SUPERTOPIC =                       "gw-req/gw-init/"
#: last will message topic:
GATEWAY_LAST_WILL_MSG_MQTT_SUPERTOPIC =                       "gw-disconnected/"

#: list of MQTT topics used by the simulated cloud
FAKE_CLOUD_PUB_SUPERTOPIC_LIST = [CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC, 
                                  CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC, 
                                  CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_SUPERTOPIC]


#: MQTT supertopic list
SUPERTOPIC_LIST = [CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC,
                   CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC,
                   GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC,
                   GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC,
                   GATEWAY_REQUEST_TO_CLOUD_MQTT_SUPERTOPIC,
                   CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_SUPERTOPIC,
                   NODE_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC]

def pack_into_bytes(format, llista):
    """
    Uses the library "struct" in ordre to pack a list of numbers with the given format, into a byte payload

    :param format: one of the different decompression from bytes options according to the reference 
    :type format: string
    :param llista: list of numbers to convert into bytes
    :type llista: list

    :does:
        1. Gets the list of numbers
        2. Uses the "*" option to tell the pack() function that "llista" is not a single argument, but that it contains all the arguments to use.
        3. Returns the payload

    :return: 
        payload (*bytes*) -- message content in bytes 
    """

    payload = pack(format, *llista)
    return payload

def unpack_bytes(format, buffer) :
    """
    Converts bytes package to decimal.
    The format is according to the reference `https://docs.python.org/3/library/struct.html <https://docs.python.org/3/library/struct.html>`__ .
    Format can be unsigned char (B), signed char (b), unsigned int (I) i signed int (i) usually either *b,B,h,H,i,I,q,Q*
    
    :param format: one of the different decompression from bytes options according to the reference 
    :type format: string
    :param buffer: message payload in bytes that we wish to unpack
    :type buffer: bytes

    :return:
        element (int) -- uncompressed number
    
    """
    if format == "<I":      #: unsigned int, 4 bytes
        return list(unpack('<I', buffer)).pop()
    elif format == "<i":    #: signed int, 4 bytes
        return list(unpack('<i', buffer)).pop()
    elif format == "<b":    #: signed char, 1 byte
        return list(unpack('<b', buffer)).pop()
    elif format == "<B":    #: unsigned char, 1 byte
        return list(unpack('<B', buffer)).pop()
    elif format == "<Q":    #: unsigned char, 8 byte
        return list(unpack('<Q', buffer)).pop()
    elif format == "<H":    #: unsigned char, 2 byte
        return list(unpack('<H', buffer)).pop()
    else:
        print("unpack_bytes error: Format is not any of <i, <I, <b, <B, <H")

def _bytes_to_str_hex_format(bytes_data):
    """ Returns a string of byte expressed in hexadecimal from a bytearray."""
    return "".join("{:02X} ".format(x) for x in bytes_data)

def get_timestamp():
    """generate a datetime format date and time which contains up to the milliseconds. This will
    be used throughout my code
    
    :return:
        timestamp (string) -- Current date and time with a format that includes up to the milliseconds
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    return timestamp

#: update the external variable (in local_settings.py) message_id, to keep track of it.
def update_msg_id(file_settings):
    """
    Updates the message id. It gets the message id from the "settings" file, updates it, and returns the value. 
    
    :param file_settings: file where the variable containing the mesage id is stored. This variable is updated every time a message is sent.
    :type file_settings: string

    :return:
        msg_id (string) -- updated mesage id
    
    """
    
    f = open(file_settings, "r")
    line = f.readline()
    message_id = int(line.split("=")[1])
    f.close()

    msg_id = message_id + 1
    if msg_id > 65535:  # we use 2 bytes for storing the message id number
        msg_id=1        # we reserve the message id of 0 for node messages to gateway


    f = open(file_settings, "w")
    text="msg_id="+str(msg_id)
    f.write(text)
    f.close()
    return msg_id


def display_and_set_interaction_mode(mode_list) :
    """
    Create a user input prompt for selecting an interaction mode
    
    :param mode_list: List of the different modes to select from
    :type mode_list: list

    :return:
        mode (string) -- interaction mode selected
    
    """
   
    return select_index_from_list(mode_list, "mode")


def get_supertopic( mqtt_topic):
    """
    cut the mqtt topic (if applicable) and return the segmented string:
    
    :param mqtt_topic: MQTT topic
    :type mqtt_topic: list

    :return:
        mqtt_supertopic (string) -- MQTT topic without the node or gateway id. It helps identify the origen of the messages
    
    """
    prefix = "<computing mqtt supertopic> "
    print(prefix + "topic: " + str(mqtt_topic))
    mqtt_supertopic = None
    if mqtt_topic != None:
        if len(mqtt_topic.split("/")) > 1 :  #: if it contains the character "/"
            mqtt_topic = mqtt_topic.split("/")[0:2]
            mqtt_supertopic = "/".join(mqtt_topic)+"/"
    
    return mqtt_supertopic


def get_all_files_in_dir(path="."):
    """
    get a list of all files within the current dir and subdirs.

    :param path: path where to start looking for files
    :type path: string

    :return:
        :llista: a list of file paths
    """
    folder = pathlib.Path(path)
    llist = folder.rglob("*")
    llista = list(map(str, list(llist)))
    
    return llista

def select_index_from_list(list, label="file"):
    """
    Create a user input prompt for selecting an index from a list
    
    :param list: List of the different elements to select from
    :type list: list

    :return:
        index (string) -- index of the list selected
    
    """
    i=1
    for a in list :
        print(str(i) + ": " + a)
        i=i+1
    ind = input("choose one "+label+" from above: ")
    print("index '" + ind + "' selected")
    ind = int(ind)-1
    return ind


def select_elem_from_list(list, label="file"):
    """
    Create a user input prompt for selecting an element from a list
    
    :param list: List of the different elements to select from
    :type list: list
    :param label: Name we want to show to the user, regarding the type of objects displayed inside the list
    :type label: string

    :return:
        element (string) -- element selected
    
    """
    ind = int(select_index_from_list(list, label))
    elem = list[ind-1]
    print(label + " '" + elem + "' selected")
    return elem

# callback functions on publish/subscribe: 
def get_sink_and_gw( wni ):
    """
    Find the gateway id and sink id. Store them in the mqtt_interaction class in order to use them later on.
    We find the gateway and sink ids, in the following steps:
        
        1. We try first to exploit the construction of the WNI class, to quickly get the needed information, without using the wirepas
        recommended functions. This is, we directly call the *wni._gateways.values()* function to get all the available gateways.
        2. In case this returns an empty list, it is likely that the reason is that not enough time ellapsed between the creations
        of the WNI interface, and the call to get its gateways. If that is the case, then wait 300ms, and try again. Wirepas guys say 
        this can be because the WNI is destroyed before the connexion with the local MQTT broker is made.
        3. If this approach fails, use the classic wirepas *get_sinks()* function in order to get the gateway and 
        sink ids.
        4. Once one of the methods above worked, the job is done.

    :param wni: Wirepas network interface object
    :type wni: wirepas_mqtt_library.WirepasNetworkInterface

    :return: a list containing:
        sink (string) -- sink id of the gateway
        gateway_id (int) -- gateway id

    """

    prefix = "<get sink & gw from wni> "
    # node interaction class mqtt broker credentials
    # Create "Wirepas Network Interface" and enable its logger
    # declare the wirepass network interface global variable
    gw_id = None
    sink = None

    # try:
    #     gws = list(wni._gateways.values())
    #     # if we get no gateways after calling the WNI, it means we run this command before the WNI was properly formed.
    #     # we should wait a few seconds and try again:
    #     attempts = 10
    #     while attempts > 0 and (len(gws) == 0 or gw.sinks == []):
    #         print("{} we waited 300ms extra, to get the list of gateways, attempts {}!".format(prefix, attempts))
    #         time.sleep(0.3)
    #         gws = list(wni._gateways.values())
    #         print("{} gw id's found: {}".format(prefix, len(gws)))
    #         for i in range(len(gws)):
    #             print("{} gw id: {} which has sinks: {}".format(prefix, gws[0].id, gws[0].sinks))

    #         attempts = attempts - 1
        
    #         gw = gws[0]
    #         gw_id = gw.id
    #         print("{} gw id: {}".format(prefix, gw_id))
    #         if gw.sinks != []:
    #             sink = list(gw.sinks)
    #             print("{} sink: {}".format(prefix, sink))
    #             sink = sink[0]["sink_id"]
    #             print("{} Got the following gateway id: {} and for the first gateway, got the following sink: {}".format(
    #                 prefix, gw_id, sink))
    #         else :
    #             print("{} vaya, sink list of gateway {} is empty, trying again... attemps left: {}".format(prefix, gw_id, attempts))
            
    #     if attempts == 0:
    #         raise Exception("{} sink list of gateway {} is empty, defaulting to normal wni.get_sinks() extraction...".format(prefix, gw_id))
    # except:
    #     print("{} Failed when extracting gateway values from WNI using an observed wirepas code shortcut".format(prefix))

    try:
        try: # time.sleep(1)
            print("{} trying to get sinks first attempt".format(prefix))
            sink_list = wni.get_sinks()
            print("{} returned gws and sinks: {}".format(prefix, sink_list))
            
            gw_id = sink_list[0][0]
            sink = sink_list[0][1]
        except Exception as err:
            print("{} trying to get sinks second attempt, the first attempt had error: {}".format(prefix, err))
            sink_list = wni.get_sinks()
            print("{} returned gws and sinks: {}".format(prefix, sink_list))
            
            gw_id = sink_list[0][0]
            sink = sink_list[0][1]
    except Exception as err:
        print("{} Failed when extracting gateway values from WNI using the wirepas suggested functions, error: {}".format(prefix, err))
        # print("{} setting sink to 'sink0' manually...".format(prefix))
        # if(sink == None):
        #     sink="sink0"

    print(prefix + "gw_id: '" + str(gw_id)+"'")
    print(prefix + "sink_id: '" + str(sink)+"'")
    if gw_id == None or sink == None:
        print("{} ERROR: no gateway id detected")
    return([sink, gw_id])


def create_wni():
    """
    Create wirepass network interface. This function gets the local credentials stored in the mqtt credentials py file, and returns a wni that can be used
    to establish a connection between the gateway backend and the sink.

    It works in the following way:

        1. It creates a wirepas network interface
        2. It waits at least 0.2 seconds for the wirepas network interface to be properly created


    :param local_broker: IP address of the local broker we want to connect to
    :type local_broker: IP address
    :param local_port: port of the local broker that accepts the MQTT connection
    :type local_port: int
    :param local_user: user (if authentication is ON)
    :type local_user: string
    :type local_password: password (if authentication is ON)
    :type local_password: string
    :param insecure: if you want to use a secure or insecure connection, and use session keys
    :type insecure: bool

    :returns:
        wni (*wirepas_mqtt_library.WirepasNetworkInterface*) object -- 
    """
    prefix = "<creating WNI>"
    [local_user, local_password, global_insecure] = creds.get_local_creds()
    wni = WirepasNetworkInterface(
                                  creds.local_broker,
                                  creds.local_port,
                                  local_user,
                                  local_password,
                                  insecure=creds.local_insecure,
                                  strict_mode=True
                                  ) #insecure=FALSE implies that a secure connection 
                                  # between client-broker is established using session keys
    # time.sleep(0.2)   # we wait 0.1 seconds to ensure all the wni setup is set properly, before starting to use it.
    print("{} wni created (in theory) {}".format(prefix, wni))
    return wni

def create_otaphelper(wni, network = NETWORK_DEFAULT_CHANNEL):
    """
    brief function that converts a WNI interface to an OtapHelper object, after selecting a network channel
    
    :param wni: Wirepas network interface that allows the connection from the gateway backend to the sink, via the local MQTT broker
    :type wni: wirepas_mqtt_library.WirepasNetworkInterface
    :param network: Network channel to which we want to create the Otap to.
    :type network: int

    :returns:
        otapHelper (*wirepas_mqtt_library.WirepasOtapHelper*) object -- 
        
    """
    prefix = "<otap helper>"
    try:
        print("{} creating otap helper with network: {}".format(prefix, network))
        otapHelper = WirepasOtapHelper(wni,
                                   int(network))
    except:
        print("{} failed to create otap helper".format(prefix))
        return None
    return otapHelper



