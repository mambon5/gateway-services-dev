"""script containing the general display functions depending on the message origin (cloud or node)."""

import global_vars as gvar          # import global variables
import message_display_specific_functions as spdispf


# GENERAL FUNCTIONS

def display_cloud_request_to_node(msg,prefix):
    """ 
    Display a message sent by the cloud to a node
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    
    
    
    :return:
        None
    """    
    prefix = prefix + "gw resp to cl req to n > "
    # Print message data in a fancy way.
    if msg.type == gvar.MSG_TYPE_GW_SET_LED_ON:
        spdispf.display_2_element_message(msg, "led on")
    elif msg.type == gvar.MSG_TYPE_GW_SET_LED_OFF:
        spdispf.display_2_element_message(msg, "led off")
    elif msg.type == gvar.MSG_TYPE_GW_SET_BLINKING:
        spdispf.display_2_element_message(msg, "blink")
    elif msg.type == gvar.MSG_TYPE_GW_ECHO:
        spdispf.display_2_element_message(msg, "send echo")
    elif msg.type == gvar.MSG_TYPE_GW_GET_LED_STATUS:
        spdispf.display_2_element_message(msg, "get led status")
    elif msg.type == gvar.MSG_TYPE_GW_GET_DIMMING_STATUS:
        spdispf.display_2_element_message(msg, "get dimming")
    elif msg.type == gvar.MSG_TYPE_GW_GET_NUMBER_OF_NEIGHBOURS:
        spdispf.display_2_element_message(msg, "get number neighbours")
    elif msg.type == gvar.MSG_TYPE_GW_GET_RSSI:
        spdispf.display_2_element_message(msg, "get rssi")
    elif msg.type == gvar.MSG_TYPE_GW_GET_HOPS:
        spdispf.display_2_element_message(msg, "get hops")
    elif msg.type == gvar.MSG_TYPE_GW_GET_NODE_STATUS:
        spdispf.display_2_element_message(msg, "get node status")
    elif msg.type == gvar.MSG_TYPE_GW_SET_STRATEGY:
        spdispf.display_strategy_response(msg)
    elif msg.type in [gvar.MSG_TYPE_GW_SET_DIMMING]:
        spdispf.display_dimming_response(msg)
    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_VERSION:
        spdispf.display_2_element_message(msg, "get node version")
    else:
        print(prefix + "error: invalid msg type")
    # print('')  # separate each new message display by one empty line

def display_gateway_response_to_cloud_request_to_node(msg,prefix):
    """ Display the gateway response to a cloud request to a specific node
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string  
    
    :return:
        None
    """    
    prefix = prefix + "cloud request to node > "
    # Print message data in a fancy way.
    if msg.type in [gvar.MSG_TYPE_GW_SET_LED_ON, gvar.MSG_TYPE_GW_SET_LED_OFF, gvar.MSG_TYPE_GW_SET_BLINKING]:
        spdispf.display_2_element_message(msg)
    elif msg.type == gvar.MSG_TYPE_GW_SET_DIMMING:
        spdispf.display_dimming_response(msg)
    elif msg.type == gvar.MSG_TYPE_GW_SET_STRATEGY:
        spdispf.display_strategy_response(msg)
    elif msg.type == gvar.MSG_TYPE_GW_ECHO:
        spdispf.display_echo_response(msg)
    elif msg.type == gvar.MSG_TYPE_GW_GET_LED_STATUS:
        spdispf.display_led_get_state_response_message(msg)
    elif msg.type == gvar.MSG_TYPE_GW_GET_DIMMING_STATUS:
        spdispf.display_dimming_response(msg)
    elif msg.type == gvar.MSG_TYPE_GW_GET_NUMBER_OF_NEIGHBOURS:
        spdispf.display_neighbour_number_response(msg)
    elif msg.type == gvar.MSG_TYPE_GW_GET_RSSI:
        spdispf.display_rssi_response(msg)
    elif msg.type == gvar.MSG_TYPE_GW_GET_HOPS:
        spdispf.display_hops_response(msg)
    elif msg.type == gvar.MSG_TYPE_GW_GET_NODE_STATUS:
        spdispf.display_node_status_response(msg)
    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_VERSION:
        spdispf.display_node_version_response(msg)
    elif msg.type == gvar.MSG_TYPE_ERROR:
        spdispf.display_error_response(msg)
    else:
        print(prefix + "error: invalid msg type")

    # print('')  # separate each new message display by one empty line

def display_cloud_request_to_gateway(msg,prefix):
    """ 
    Display the message sent by the cloud to a gateway
    The type of display depends on the message type.

    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    
    :return:
        None
    """    
    prefix = prefix + "cloud req to gateway> "
    # Print message data in a fancy way.
    if msg.type in [gvar.MSG_TYPE_CLOUD_TO_GATEWAY_NODE_LIST]:
        spdispf.display_client_id_msg(msg, "node list")
    elif msg.type in [gvar.MSG_TYPE_CLOUD_TO_GATEWAY_REMOVE_NODES]:
        spdispf.display_remove_nodes_msg(msg, prefix)
    elif msg.type in [gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_GATEWAY, gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_NODES,
                      gvar.MSG_TYPE_CLOUD_TO_GATEWAY_GET_GATEWAY_VERSION]:
        spdispf.display_2_element_message(msg)
    else:
        print(prefix + "error: invalid msg type")

    # print('')  # separate each new message display by one empty line

def display_gateway_response_to_cloud_request_to_gateway(msg,prefix):
    """ Display the response from a gateway to a cloud request to the gateway itself. 
    The type of display depends on the message type.
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    
    
    
    :return:
        None
    """    
    prefix = prefix + "gw resp to cl req to gw > "
    # Print message data in a fancy way.
    if msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_REMOVE_NODES:
        spdispf.display_crc_response(msg, prefix)
    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_NODE_LIST:
        spdispf.display_node_list_client_id(msg, prefix)
    elif msg.type in [gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_GATEWAY, gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_NODES]:
        spdispf.display_2_element_message(msg, msg.type)
    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_GET_GATEWAY_VERSION:
        spdispf.display_version_message(msg, prefix)
    elif msg.type == gvar.MSG_TYPE_ERROR:
        spdispf.display_error_response(msg)
    else:
        print(prefix + "error: invalid msg type")

    # print('')  # separate each new message display by one empty line

def display_gateway_request_to_cloud(msg, prefix):
    """ 
    Display the request sent by a gateway to the cloud.
    The type of display depends on the message type.
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    
    :return:
        None
    """    
    prefix = prefix + "gateway req to cloud> "
    # Print message data in a fancy way.
    if msg.type == gvar.MSG_TYPE_ALIVE_GW_TO_CLOUD:
        spdispf.display_2_element_message(msg, "alive")
    elif msg.type in [gvar.MSG_TYPE_ADD_NODES_GW_TO_CLOUD]:
        spdispf.display_node_list(msg, prefix, "add nodes")
    elif msg.type in [ gvar.MSG_TYPE_UNSEEN_NODES_GW_TO_CLOUD]:
        spdispf.display_node_list(msg, prefix, "remove nodes")
    elif msg.type == gvar.MSG_TYPE_NODE_STATUS_GW_TO_CLOUD:
        spdispf.display_node_status_list(msg, prefix)
    elif msg.type == gvar.MSG_TYPE_ALARM_GW_TO_CLOUD:
        spdispf.display_alarm_node_list(msg, prefix)
    elif msg.type == gvar.MSG_TYPE_ELECTRIC_PARAMETERS_GW_TO_CLOUD:
        spdispf.display_electrim_param_list(msg, prefix)
    else:
        print(prefix + "error: invalid msg type")

    # print('')  # separate each new message display by one empty line

def display_cloud_response_to_gateway_req(msg, prefix) :
    """ 
    Display the response message sent by a cloud to a gateway request.
    The type of display depends on the message type.
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        None
    """    
    prefix = prefix + "cloud resp to gateway req> "
    if msg.type == gvar.MSG_TYPE_ERROR:
        spdispf.display_error_response(msg)
    elif msg.type == gvar.MSG_TYPE_ALIVE_GW_TO_CLOUD:
        spdispf.display_2_element_message(msg, "alive")
    elif msg.type in [gvar.MSG_TYPE_ADD_NODES_GW_TO_CLOUD, gvar.MSG_TYPE_UNSEEN_NODES_GW_TO_CLOUD, gvar.MSG_TYPE_NODE_STATUS_GW_TO_CLOUD,
                       gvar.MSG_TYPE_ELECTRIC_PARAMETERS_GW_TO_CLOUD ]:
        spdispf.display_crc_response(msg)
    elif msg.type == gvar.MSG_TYPE_ALARM_GW_TO_CLOUD:
        spdispf.display_4_element_message(msg, "alarm", "crc")
    else:
        print(prefix + "error: invalid msg type")


# 134 3 141 220 340 460 40 80 6500300 142 220 440 160 40 20 6506600 144 220 290 190 40 28 650240

def display_gateway_node_messages(msg, prefix):
    """ Display the messages from/to the mesh network and the gateway.
    The type of display depends on the message type.

    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    
    
    
    :return:
        None
    """    
    print(prefix + "gateway to node messaging") 

    # NODE RESPONSE TO GATEWAY
    if msg.type in [gvar.MSG_TYPE_GW_SET_LED_ON, gvar.MSG_TYPE_GW_SET_LED_OFF, gvar.MSG_TYPE_GW_SET_BLINKING
                    ] :
        print(prefix + "displaying message payload for type: " +str(msg.type)+ ", no extra arguments needed")
        spdispf.display_2_element_message(msg, msg.type)
    
    elif msg.type in [gvar.MSG_TYPE_GW_SET_DIMMING, gvar.MSG_TYPE_GW_GET_DIMMING_STATUS]:
        print(prefix + " dimming")
        spdispf.display_dimming_response(msg)    # dimming
    elif msg.type == gvar.MSG_TYPE_GW_SET_STRATEGY:
        print(prefix + " strategy")
        spdispf.display_strategy_response(msg)  # strategy

    elif msg.type == gvar.MSG_TYPE_GW_ECHO:
        print(prefix + " echo")
        spdispf.display_echo_response(msg)    # echo
    elif msg.type == gvar.MSG_TYPE_GW_GET_LED_STATUS:
        print(prefix + " get led status")
        spdispf.display_led_status_response(msg)  # get led status
    elif msg.type == gvar.MSG_TYPE_GW_GET_NUMBER_OF_NEIGHBOURS:
        print(prefix + " num neighbours")
        spdispf.display_neighbour_number_response(msg)    # num neighbours
    elif msg.type == gvar.MSG_TYPE_GW_GET_RSSI:
        print(prefix + " rssi")
        spdispf.display_rssi_response(msg)  # rssi

    elif msg.type == gvar.MSG_TYPE_GW_GET_HOPS:
        print(prefix + " hops msg")
        spdispf.display_hops_response(msg)    # hops
    elif msg.type == gvar.MSG_TYPE_GW_GET_NODE_STATUS:
        print(prefix + " node status")
        spdispf.display_node_status_response(msg)  # node status
    elif msg.type == gvar.MSG_TYPE_ERROR:
        print(prefix + " error")
        spdispf.display_error_response(msg)  # error

    # NODE REQUEST TO GATEWAY
    elif msg.type == gvar.MSG_TYPE_NODE_GET_TIME:
        print(prefix + " get time")
        spdispf.display_2_element_message(msg, "get time")                            # get time
    elif msg.type == gvar.MSG_TYPE_NODE_SEND_ALARM:
        print(prefix + "send alarm")
        spdispf.display_alarm_response(msg)                                          # alarm
    elif msg.type == gvar.MSG_TYPE_NODE_SEND_CURRENT_VOLTAGE:
        print(prefix + "send alarm")
        spdispf.display_current_voltage_response(msg, msg.args, prefix)                                          # current and voltage
    elif msg.type == gvar.MSG_TYPE_NODE_SEND_ELECTRIC_PARAMETERS:
        print(prefix + " creating crc basic electrim parameters msg payload")       # electrim parameters
        spdispf.display_electrim_parameters_response(msg, msg.args, prefix)                   
    elif msg.type == gvar.MSG_TYPE_NODE_SEND_SOLAR_PANEL_METRICS:       
        print(prefix + " creating crc solar panel metrics msg payload")      # solar panel metrics 
        spdispf.display_solar_metrics_response(msg, prefix)
    else :
        print(prefix + "wrong message type")
  