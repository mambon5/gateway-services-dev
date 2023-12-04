"""
Functions to create a message for the cloud. It also icludes some functions that create a message from the cloud to the gateway, buy theses 
are not meant for production.
"""

import global_vars as gvar
import create_message_specific_functions as cmsgspf
from struct import *
import compute_crc as get_crc


def gw_resp_to_cloud_req_to_node(msg_type, args, prefix=""):
    """
    Creates the payload for a gateway response to a cloud message that was sent to a node.

    :does:

    1. Depending on the *msg_type* it will call a specific function or another, to create the payload.
    2. It will return this payload to the main *create_message* function.
    
    :param msg_type: message type 
    :type msg_type: int
    :param args: arguments that we wish to include in the message 
    :type args: list
    :param prefix: string to prepend to all the prints/console logs
    :type prefix: string

    :return:
        :payload: (bytes) -- partial payload to be sent, without the message id and type, which are already sent

    
    """
    prefix = prefix + "create gw resp to cloud msg /n > "
    payload = b''

    if msg_type in [gvar.MSG_TYPE_CLOUD_TO_NODE_SET_LED_ON, gvar.MSG_TYPE_CLOUD_TO_NODE_SET_LED_OFF,
                        gvar.MSG_TYPE_CLOUD_TO_NODE_SET_BLINKING]:
        print(prefix + " no extra arguments needed,  led on/off/blink msg payload")
    elif msg_type in [gvar.MSG_TYPE_CLOUD_TO_NODE_SET_DIMMING, gvar.MSG_TYPE_CLOUD_TO_NODE_GET_DIMMING_STATUS]:
        print(prefix + " creating set/get dimming msg payload")
        payload =  cmsgspf.set_dimming_msg_payload(args[0])             # dimming
    elif msg_type == gvar.MSG_TYPE_CLOUD_TO_NODE_SET_STRATEGY:
        print(prefix + " creating set strategy msg payload")
        payload =  cmsgspf.set_strategy_msg_payload(args[0])            # strategy 
    elif msg_type == gvar.MSG_TYPE_CLOUD_TO_NODE_ECHO:
        print(prefix + " creating echo msg payload")
        payload =   cmsgspf.set_echo_msg_payload(args[0])    # echo
    elif msg_type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_LED_STATUS:
        print(prefix + " creating get led status msg payload")
        payload =  cmsgspf.set_1_arg_payload(args[0])                   # get led status
    elif msg_type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_NUMBER_OF_NEIGHBOURS:
        print(prefix + " creating get num neighbours msg payload")
        payload =  cmsgspf.set_1_arg_payload(args[0],"I")                   # num neighbours
    elif msg_type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_RSSI:
        print(prefix + " creating rssi msg payload")
        payload =  cmsgspf.set_1_arg_payload(args[0], "b")                   # rssi
    elif msg_type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_HOPS:
        print(prefix + " creating hops msg payload")
        payload =  cmsgspf.set_1_arg_payload(args[0])             # hops
    elif msg_type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_NODE_STATUS:
        print(prefix + " creating node status msg payload")
        payload =  cmsgspf.send_node_status_msg_payload(args)   
    elif msg_type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_VERSION:
        print(prefix + " creating node version msg payload")
        payload =  cmsgspf.send_node_version_msg_payload(args[0],args[1],args[2],args[3],
                                             args[4],args[5],args[6],args[7], packs="BBBBBBBB")                           # node status
    else :
        print(prefix + "wrong message type")
    
    return payload


def gw_resp_to_cloud_req_to_gw(msg_type, args, prefix=""):
    """
    Creates the payload for the gateway response to a cloud message directed to a gateway.
    
    :does:

    1. Depending on the *msg_type* it will call a specific function or another, to create the payload.
    2. It will return this payload to the main *create_message* function.

    :type msg_type: int
    :param args: arguments that we wish to include in the message 
    :type args: list
    :param prefix: string to prepend to all the prints/console logs
    :type prefix: string

    :return:
        :payload: (bytes) -- partial payload to be sent, without the message id and type, which are already sent

    
    """
    prefix = prefix + "create gw resp to cloud msg /gw > "
    payload = b''

          
    if msg_type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_NODE_LIST:
        print(prefix + " creating node list msg payload")
        payload =  cmsgspf.node_id_list_client_id_payload(args)             # node list
    elif msg_type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_REMOVE_NODES:
        print(prefix + " creating node list msg payload")
        payload =  cmsgspf.gen_crc_message(args)                                # REMOVE NODES
    elif msg_type in [gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_GATEWAY,gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_NODES]:
        print(prefix + " creating software update msg payload")
        pass   
    elif msg_type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_GET_GATEWAY_VERSION:
        print(prefix + " creating gw version msg payload")
        payload =  cmsgspf.gen_gw_version_message(args)                               # get gateway version
    
    else :
        print(prefix + "wrong message type")
        
    return payload


def gw_request_to_cloud(msg_type, args, prefix=""):
    """
    Creates the payload for the gateway request to the cloud. These functions need to be developped further, since right now,
    they invent the nodes to add/remove from the cloud database.
    
    :does:

    1. Depending on the *msg_type* it will call a specific function or another, to create the payload.
    2. It will return this payload to the main *create_message* function.

    :param msg_type: message type 
    :type msg_type: int
    :param args: arguments that we wish to include in the message 
    :type args: list

    :param prefix: string to prepend to all the prints/console logs
    :type prefix: string
    

    :return:
        :payload: (bytes) -- partial payload to be sent, without the message id and type, which are already sent

    """

    prefix = prefix + "create gw req to cloud"
    payload = b''

    if msg_type == gvar.MSG_TYPE_ALIVE_GW_TO_CLOUD:
        print(prefix + " no extra arguments needed,  alive msg payload")
    elif msg_type == gvar.MSG_TYPE_ADD_NODES_GW_TO_CLOUD:
        print(prefix + " creating add nodes msg payload")
        payload =  cmsgspf.random_node_id_list_payload(10)             # gw to cl request add nodes
    elif msg_type == gvar.MSG_TYPE_UNSEEN_NODES_GW_TO_CLOUD:
        print(prefix + " creating remove nodes msg payload")
        payload =  cmsgspf.random_node_id_list_payload(14)             # gw to cl request remove nodes
    elif msg_type == gvar.MSG_TYPE_NODE_STATUS_GW_TO_CLOUD:
        print(prefix + " creating node status list msg payload")
        payload =  cmsgspf.random_node_status_list_payload(6)             # gw to cl request node status list
    elif msg_type == gvar.MSG_TYPE_ALARM_GW_TO_CLOUD:
        print(prefix + " creating alive msg payload")
        payload =  cmsgspf.random_alarm_node_list_payload(15)             # gw to cl request electric parameters
    elif msg_type == gvar.MSG_TYPE_ELECTRIC_PARAMETERS_GW_TO_CLOUD:
        print(prefix + " creating send consumptions msg payload")
        payload =  cmsgspf.set_electric_params_list_msg_payload(21)             # gw to cl send consums
    else :
        print(prefix + "wrong message type")
    
    return payload


def cloud_request_to_node(msg_type, args, prefix=""):
    """
    Creates the payload for the cloud request to a specific node. This function is not meant for production, only for testing purposes.
    
    :does:

    1. Depending on the *msg_type* it will call a specific function or another, to create the payload.
    2. It will return this payload to the main *create_message* function.
    
    :param msg_type: message type 
    :type msg_type: int
    :param args: arguments that we wish to include in the message 
    :type args: list
    :param prefix: string to prepend to all the prints/console logs
    :type prefix: string

    :return:
        :payload: (bytes) -- partial payload to be sent, without the message id and type, which are already sent

    """
    
    prefix = prefix + "create cloud req to node > "
    payload = b''

    if msg_type in [gvar.MSG_TYPE_CLOUD_TO_NODE_SET_LED_ON, gvar.MSG_TYPE_CLOUD_TO_NODE_SET_LED_OFF, gvar.MSG_TYPE_CLOUD_TO_NODE_SET_BLINKING,
                        gvar.MSG_TYPE_CLOUD_TO_NODE_ECHO, gvar.MSG_TYPE_CLOUD_TO_NODE_GET_LED_STATUS, gvar.MSG_TYPE_CLOUD_TO_NODE_GET_DIMMING_STATUS,
                        gvar.MSG_TYPE_CLOUD_TO_NODE_GET_NUMBER_OF_NEIGHBOURS , gvar.MSG_TYPE_CLOUD_TO_NODE_GET_RSSI, gvar.MSG_TYPE_CLOUD_TO_NODE_GET_HOPS, 
                        gvar.MSG_TYPE_CLOUD_TO_NODE_GET_NODE_STATUS
                        ] :
        print(prefix + " no extra arguments needed")
    elif msg_type == gvar.MSG_TYPE_CLOUD_TO_NODE_SET_DIMMING:
        payload =  cmsgspf.set_dimming_msg_payload(args[0])              # dimming
    elif msg_type == gvar.MSG_TYPE_CLOUD_TO_NODE_SET_STRATEGY:
        payload =  cmsgspf.set_strategy_msg_payload(args[0])            # strategy

    else :
        print(prefix + "wrong message type")
        
    
    return payload

def cloud_request_to_gateway(msg_type, args, prefix=""):
    """
    Creates the payload for the cloud request to a gateway. This function is not meant for production, only for testing purposes.
    
    :does:

    1. Depending on the *msg_type* it will call a specific function or another, to create the payload.
    2. It will return this payload to the main *create_message* function. 
   
    :param msg_type: message type 
    :type msg_type: int
    :param args: arguments that we wish to include in the message 
    :type args: list
    :param prefix: string to prepend to all the prints/console logs
    :type prefix: string

    :return:
        :payload: (bytes) -- partial payload to be sent, without the message id and type, which are already sent
    """
    
    prefix = prefix + "create cloud req to node > "
    payload = b''

    client_id = 73871
    if msg_type in [gvar.MSG_TYPE_CLOUD_TO_GATEWAY_NODE_LIST
                    ] :                     
        payload =  cmsgspf.set_client_id_msg_payload([client_id])          # led on, led off, node list, node status list
        print(prefix + " set the payload for client id message.")
    elif msg_type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_REMOVE_NODES:
        num_nodes = 12
        payload =  cmsgspf.set_remove_nodes_msg_payload(num_nodes)              # remove nodes
    
    elif msg_type in  [gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_GATEWAY, gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_NODES]:
        print(prefix + "no extra arguments needed")                        # update software

    else :
        print(prefix + "wrong message type")
        
    return payload





def cloud_resp_to_gateway(msg_type, args, prefix="", msg=None):
    """
    Creates the payload for the cloud response to a gateway request. This function is not meant for production, only for testing purposes.
    
    :does:

    1. Depending on the *msg_type* it will call a specific function or another, to create the payload.
    2. It will return this payload to the main *create_message* function. 
   
    :param msg_type: message type 
    :type msg_type: int
    :param args: arguments that we wish to include in the message 
    :type args: list
    :param prefix: string to prepend to all the prints/console logs
    :type prefix: string
    :param msg: messge received class RxMsg, only when creating response messages to a previous request! This field will be *None* for request mode
    :type msg: RxMsg

    :return:
        :payload: (bytes) -- partial payload to be sent, without the message id and type, which are already sent

    """
    
    prefix = prefix + "create cloud req to node > "
    payload = b''

    if msg_type == gvar.MSG_TYPE_ALIVE_GW_TO_CLOUD:
        print(prefix + " no extra arguments needed")
        pass
    elif msg_type in [gvar.MSG_TYPE_ADD_NODES_GW_TO_CLOUD, gvar.MSG_TYPE_UNSEEN_NODES_GW_TO_CLOUD,
                    gvar.MSG_TYPE_NODE_STATUS_GW_TO_CLOUD, gvar.MSG_TYPE_ELECTRIC_PARAMETERS_GW_TO_CLOUD
                    ] :
        args = [get_crc.compute_crc(msg.payload)]
        payload =  cmsgspf.gen_crc_message(args) # send crc
    elif msg_type == gvar.MSG_TYPE_ALARM_GW_TO_CLOUD:
        payload =  cmsgspf.set_2_arg_payload(msg.args[0], get_crc.compute_crc(msg.payload))             # alarm and crc

    else :
        print(prefix + "wrong message type")      
    
    return payload