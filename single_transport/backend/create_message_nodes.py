"""
Functions to create a message for the nodes. 
"""

import compute_crc as get_crc
import global_vars as gvar
import create_message_specific_functions as cmsgspf
from struct import *

def gateway_request_to_nodes(msg_type, args, prefix=""):
    """
    Creates the partial payload for the gateway request to a mesh network
    
    :does:
        1. Depending on the message type, uses a scpecific create message function or another
        2. Once a specific create message function is selected, the payload corresponding just to the message arguments is computed
        3. This payload is returned, It can also be empty payload '', if there was no argument in the message to be sent

    :param msg_type: message type 
    :type msg_type: int
    :param args: arguments that we wish to include in the message 
    :type args: list
    :param prefix: string to prepend to all the prints/console logs
    :type prefix: string

    :return:
        :payload: (bytes) -- partial payload to be sent, without the message id and type, which are already sent
    """
    prefix = prefix + "create gw request to the nodes > "
    payload = b''

    if msg_type in [gvar.MSG_TYPE_GW_SET_LED_ON, gvar.MSG_TYPE_GW_SET_LED_OFF, gvar.MSG_TYPE_GW_SET_BLINKING,
                        gvar.MSG_TYPE_GW_ECHO, gvar.MSG_TYPE_GW_GET_LED_STATUS, gvar.MSG_TYPE_GW_GET_DIMMING_STATUS,
                        gvar.MSG_TYPE_GW_GET_NUMBER_OF_NEIGHBOURS , gvar.MSG_TYPE_GW_GET_RSSI, 
                        gvar.MSG_TYPE_GW_GET_NODE_STATUS
                        ]:
        
        print(prefix + "setting message payload for type: " +str(msg_type)+ ", no extra arguments needed")
    
    elif msg_type == gvar.MSG_TYPE_GW_SET_DIMMING:
        if len(args) != 1:
            print(prefix + "error: arguments provided for message type "+ str(msg_type) + " is: " + str(len(args)) + " and 1 dimming is needed")
            return payload
        dimming = args[0]
        print(prefix + " creating set dimming msg payload with dimming: " + str(dimming) +"%")
        payload =  cmsgspf.set_dimming_msg_payload(dimming)    # dimming
    elif msg_type == gvar.MSG_TYPE_GW_SET_STRATEGY:
        if len(args) != 1:
            print(prefix + "error: arguments provided for message type "+ str(msg_type) + " is: " + str(len(args)) + " and 1 strategy is needed")
            return payload
        strategy = args[0]
        print(prefix + " creating strategy msg payload, with strategy: " + str(strategy))
        payload =  cmsgspf.set_strategy_msg_payload(strategy)  # strategy

    else :
        print(prefix + "wrong message type")


    return payload


def gateway_response_to_nodes(msg, args, prefix=""):
    """
    Creates the partial payload for the gateway response to a mesh network request
    
    :does:
        1. Depending on the message type, uses a scpecific create message function or another
        2. Once a specific create message function is selected, the payload corresponding just to the message arguments is computed
        3. This payload is returned, It can also be empty payload '', if there was no argument in the message to be sent

    :param msg_type: message type 
    :type msg_type: int
    :param args: arguments that we wish to include in the message 
    :type args: list
    :param prefix: string to prepend to all the prints/console logs
    :type prefix: string

    :return:
        :payload: (bytes) -- partial payload to be sent, without the message id and type, which are already sent
    """

    prefix = prefix + "create gw request to the nodes > "
    payload = b''

    if msg.type == gvar.MSG_TYPE_NODE_GET_TIME:
        print(prefix + " creating GET TIME msg payload")
        payload =  cmsgspf.set_1_arg_payload(gvar.get_timestamp(),"I")    # get time
    elif msg.type == gvar.MSG_TYPE_NODE_SEND_ALARM:
        print(prefix + " creating send alarm msg payload")
        payload =  cmsgspf.set_1_arg_payload(args[0])    # alarm
    elif msg.type == gvar.MSG_TYPE_NODE_SEND_CURRENT_VOLTAGE:
        print(prefix + " creating current and voltage msg payload")
        payload =  cmsgspf.set_1_arg_payload( get_crc.compute_crc(msg.payload), packs="I" )                              # CURRENT and voltage
    elif msg.type == gvar.MSG_TYPE_NODE_SEND_ELECTRIC_PARAMETERS:
        print(prefix + " creating crc electric parameters msg payload")                    # basic consumption (crc)
        payload =  cmsgspf.set_1_arg_payload( get_crc.compute_crc(msg.payload), packs="I" )                        
    elif msg.type == gvar.MSG_TYPE_NODE_SEND_SOLAR_PANEL_METRICS:       
        print(prefix + " creating crc solar panel metrics msg payload")                    # solar panel metrics (crc)
        payload =  cmsgspf.set_1_arg_payload( get_crc.compute_crc(msg.payload), packs="I" )
    elif msg.type == gvar.MSG_TYPE_NODE_SEND_NODE_STATUS:       
        print(prefix + " creating crc node status msg payload")                    # node status (crc)
        payload =  cmsgspf.set_1_arg_payload( get_crc.compute_crc(msg.payload), packs="I" )

    else :
        print(prefix + "wrong message type")

    return payload
   
# to be deleted for not being used:
def node_request_to_gateway(msg_type, args, prefix=""):
    """
    Creates the partial payload for the node request to the gateway. This function is not for production, since it is simulating the nodes from
    the gateway backend.
    
    :does:
        1. Depending on the message type, uses a scpecific create message function or another
        2. Once a specific create message function is selected, the payload corresponding just to the message arguments is computed
        3. This payload is returned, It can also be empty payload '', if there was no argument in the message to be sent
    
    :param msg_type: message type 
    :type msg_type: int
    :param args: arguments that we wish to include in the message 
    :type args: list
    :param prefix: string to prepend to all the prints/console logs
    :type prefix: string

    :return:
        :payload: (bytes) -- partial payload to be sent, without the message id and type, which are already sent
    """
    prefix = prefix + "create gw request to the nodes > "
    payload = b''

    if msg_type == gvar.MSG_TYPE_NODE_GET_TIME:
        print(prefix + " creating GET TIME msg payload")
    elif msg_type == gvar.MSG_TYPE_NODE_SEND_ALARM:
        print(prefix + " creating send alarm msg payload")
        payload = cmsgspf.set_1_arg_payload(args[0])    # alarm
    elif msg_type == gvar.MSG_TYPE_NODE_SEND_ELECTRIC_PARAMETERS:
        print(prefix + " creating crc basic consumptions msg payload")                    # basic node consumption 
        payload = cmsgspf.set_consums_msg_payload()                        
    elif msg_type == gvar.MSG_TYPE_NODE_SEND_SOLAR_PANEL_METRICS:       
        print(prefix + " creating crc solar panel metrics msg payload")                    # node solar panel metrics 
        payload = cmsgspf.set_solar_metrics_msg_payload()
    else :
        print(prefix + "wrong message type")

    return payload