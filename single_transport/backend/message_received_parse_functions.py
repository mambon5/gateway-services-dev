"""
this script contains the main parse functions for any received message. These functions are split depending on:

- the message origin
- the mqtt topic at which the message arrives

"""

import global_vars as gvar # import global variables
import message_specific_parse_functions as parspec

# CLOUD REQUEST TO NODE
def parse_cloud_request_to_node(msg, prefix):
    """ Parse the cloud request to a node

    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """

    result = [False,[]]
    payload = msg.payload
    type = msg.type
    print(prefix + "msg type: " + str(type))
    if type in [gvar.MSG_TYPE_CLOUD_TO_NODE_SET_LED_ON, gvar.MSG_TYPE_CLOUD_TO_NODE_SET_LED_OFF, 
                gvar.MSG_TYPE_CLOUD_TO_NODE_SET_BLINKING, gvar.MSG_TYPE_CLOUD_TO_NODE_ECHO, gvar.MSG_TYPE_CLOUD_TO_NODE_GET_LED_STATUS,
                gvar.MSG_TYPE_CLOUD_TO_NODE_GET_DIMMING_STATUS, gvar.MSG_TYPE_CLOUD_TO_NODE_GET_NUMBER_OF_NEIGHBOURS,
                gvar.MSG_TYPE_CLOUD_TO_NODE_GET_RSSI, gvar.MSG_TYPE_CLOUD_TO_NODE_GET_HOPS, 
                gvar.MSG_TYPE_CLOUD_TO_NODE_GET_NODE_STATUS, gvar.MSG_TYPE_CLOUD_TO_NODE_GET_VERSION
                ]:
        if len(payload) == gvar.EXPECTED_LENGTH_NO_ARGUMENTS:
            #no further parsing needed since message hass length 1 byte
            result = [True,[]]
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif type == gvar.MSG_TYPE_CLOUD_TO_NODE_SET_DIMMING:       # variable ammount of bytes
        if len(payload) == gvar.EXPECTED_LENGTH_SET_DIMMING_REQUEST_MSG:
            #no further parsing needed since message hass length 1 byte
            result = parspec.parse_dimming_message(payload,prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif type == gvar.MSG_TYPE_CLOUD_TO_NODE_SET_STRATEGY:
        if len(payload) == gvar.EXPECTED_LENGTH_SET_STRATEGY_REQUEST_MSG:
            #no further parsing needed since message hass length 1 byte
            result = parspec.parse_set_strategy_message(payload,prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    else:
        print(prefix+"invalid message type")    # invalid or unsupported payload received.
        result[1] = [gvar.ERROR_TYPE_INVALID_MSG_TYPE]

    return result


# CLOUD REQUEST TO GATEWAY
def parse_cloud_request_to_gateway(msg, prefix):
    """
    Parse the cloud request to a gateway

    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    result = [False,[]]
    good_length = False # bool to check if the expected length was met or not, assume not.

    if msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_NODE_LIST:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NODE_LIST_CLOUD_TO_GATEWAY_REQUEST:
            #no further parsing needed since message hass length 1 byte
            result = parspec.parse_cloud_to_gateway_request_generic_client_id(msg.payload, prefix)
            good_length = True

    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_REMOVE_NODES:          # variable ammount of bytes
        
        num_nodes = gvar.unpack_bytes('<H', msg.payload[3:5])           # num_nodes
        print(prefix+"num nodes " + str(num_nodes))
        if len(msg.payload) == gvar.expected_length_cloud_to_gw_remove_nodes(num_nodes) :
            result = parspec.parse_node_list(msg.payload, num_nodes, prefix)
            good_length = True

    elif msg.type in [gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_GATEWAY,gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_NODES]:        # update software
        print(prefix + "updating software parse message")
        if len(msg.payload) == gvar.EXPECTED_LENGTH_UPDATE_GW_SOFTWARE_CLOUD_TO_GATEWAY_REQUEST:
            #no further parsing needed since message hass length 1 byte
            result = [True, []]
            good_length = True

    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_GET_GATEWAY_VERSION:
        print("{} getting gateway software id...")
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_GW_VERSION_CLOUD_TO_GATEWAY_REQUEST:
            #no further parsing needed since message hass length 1 byte
            result = [True, []]
            good_length = True

    else:
        print(prefix + "invalid message type")
        result[1] = [gvar.ERROR_TYPE_INVALID_MSG_TYPE]
        return result

    if not good_length:
        print(prefix + "unexpected message length")
        result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]
    
    return result



# CLOUD RESPONSE TO GATEWAY REQUEST
def parse_cloud_response_to_gateway_req(msg, prefix) :
    """
    Parse the cloud response to a gateway request

    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    result = [False,[]]
    if msg.type == gvar.MSG_TYPE_ERROR:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_ERROR:
            result = parspec.parse_error_message(msg.payload)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]
    
    elif msg.type == gvar.MSG_TYPE_ALIVE_GW_TO_CLOUD:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NO_ARGUMENTS:
            #no further parsing needed since message hass length 1 byte
            result = [True,[]]
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type in [gvar.MSG_TYPE_ADD_NODES_GW_TO_CLOUD, gvar.MSG_TYPE_UNSEEN_NODES_GW_TO_CLOUD,
                      gvar.MSG_TYPE_NODE_STATUS_GW_TO_CLOUD, gvar.MSG_TYPE_ELECTRIC_PARAMETERS_GW_TO_CLOUD
                      ]:          # variable ammount of bytes
        if len(msg.payload) == gvar.EXPECTED_LENGTH_CLOUD_RESPONSE_TO_GATEWAY_ADD_NODES_REQUEST_MSG:
            #no further parsing needed since message hass length 1 byte
            result = parspec.parse_crc_response(msg.payload)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_ALARM_GW_TO_CLOUD:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_CLOUD_RESPONSE_TO_GATEWAY_ALARM_REQUEST_MSG:
            #no further parsing needed since message hass length 1 byte
            result = parspec.parse_alarm_response(msg.payload)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    else:
        print(prefix+"invalid message type")            # invalid msg type.
        result[1] = [gvar.ERROR_TYPE_INVALID_MSG_TYPE]

    return result

# NODE RESPONSES TO GATEWAY REQUESTS
def parse_node_to_gw_response(msg, prefix):
    """
    Parse node response to gateway request

    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    print(prefix + "node response to gw request > ")
    result = [False,[]]    

    if msg.type == gvar.MSG_TYPE_GW_SET_LED_ON:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NO_ARGUMENTS:
            #no further parsing needed since message hass length 1 byte
            result = [True,[]]
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_GW_SET_LED_OFF:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NO_ARGUMENTS:
            #no further parsing needed since message hass length 1 byte
            result = [True,[]]
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_GW_SET_DIMMING:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_SET_DIMMING_RESPONSE_MSG:
            result = parspec.parse_dimming_message(msg.payload, prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_GW_SET_BLINKING:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NO_ARGUMENTS:
            #no further parsing needed since message hass length 1 byte
            result = [True,[]]
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_GW_SET_STRATEGY:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_SET_STRATEGY_RESPONSE_MSG:
            result = parspec.parse_set_strategy_message(msg.payload, prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_GW_ECHO:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_SEND_ECHO_RESPONSE_MSG_FROM_NODE:
            result = parspec.parse_echo_response(msg.rawdata.travel_time_ms)
            # result = parspec.parse_echo_response(msg.payload)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_GW_GET_LED_STATUS:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_LED_STATUS_RESPONSE_MSG:
            result = parspec.parse_led_status_response(msg.payload, prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]
    
    elif msg.type == gvar.MSG_TYPE_GW_GET_DIMMING_STATUS:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_DIMMING_STATUS_RESPONSE_MSG:
            result = parspec.parse_dimming_message(msg.payload, prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_GW_GET_NUMBER_OF_NEIGHBOURS:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_NUMBER_OF_NEIGHBOURS_RESPONSE_MSG:
            result = parspec.parse_neighbour_number_response(msg.payload, prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_GW_GET_RSSI:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_RSSI_RESPONSE_MSG:
            result = parspec.parse_rssi_response(msg.payload, prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]
    
    elif msg.type == gvar.MSG_TYPE_GW_GET_HOPS:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_RSSI_RESPONSE_MSG:
            result = parspec.parse_hops_response_from_node(msg.rawdata.hop_count, prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]
    
    elif msg.type == gvar.MSG_TYPE_GW_GET_NODE_STATUS:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_NODE_STATUS_RESPONSE_MSG_MESH_NETWORK:
            result = parspec.parse_node_status_response_from_node(msg.payload, msg.rawdata, prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_GW_SEND_NEW_STRAGEGY:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_NEW_STRATEGY_RESPONSE_MSG_MESH_NETWORK:
            result = parspec.get_crc(msg.payload)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]
    
    elif msg.type == gvar.MSG_TYPE_ERROR:            # variable ammount of bytes
        if len(msg.payload) == gvar.EXPECTED_LENGTH_ERROR:
            result = parspec.parse_error_message(msg.payload)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    else:
        print(prefix+"invalid message type!")               # invalid msg type
        result[1] = [gvar.ERROR_TYPE_INVALID_MSG_TYPE]

    return result

# NODE REQUEST TO GATEWAY:
def parse_node_to_gw_request(msg, prefix):
    """
    Parse node to gateway requests.

    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    prefix = prefix + "node request to gw > "
    print(prefix + "msg received!")

    result = [False,[]]
    if msg.type == gvar.MSG_TYPE_NODE_GET_TIME:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NODE_TO_GATEWAY_GET_TIME_REQUEST:
            #no further parsing needed since message hass length 1 byte
            result = [True,[]]
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_NODE_SEND_ALARM:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NODE_TO_GATEWAY_ALARM_REQUEST:
            #no further parsing needed since message hass length 1 byte
            result = parspec.parse_alarm_response(msg.payload)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_NODE_SEND_CURRENT_VOLTAGE:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NODE_TO_GATEWAY_CURRENT_VOLTAGE_REQUEST:
            result = parspec.parse_current_voltage(msg.payload)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_NODE_SEND_ELECTRIC_PARAMETERS:
        print(prefix + "electrical parameters")
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NODE_TO_GATEWAY_ELECTRIC_PARAMETERS_REQUEST:
            result = parspec.parse_electric_parameters(msg.payload[3:15])
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_NODE_SEND_SOLAR_PANEL_METRICS:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NODE_TO_GATEWAY_SOLAR_METRICS_REQUEST:
            #no further parsing needed since message hass length 1 byte
            result = parspec.parse_node_solar_metrics_request(msg.payload)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_NODE_SEND_NODE_STATUS:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NODE_TO_NODE_STATUS_REQUEST:
            result = parspec.parse_node_status_request(msg.payload)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    else:
        print(prefix+"invalid message type!")   # invalid msg type
        result[1] = [gvar.ERROR_TYPE_INVALID_MSG_TYPE]

    return result





### >>>>> THE FOLLOWING FUNCTIONS SIMULATE THE CLOUD BEHAVIOUR, FOR PRODUCTION OF THE GATEWAY THEY CAN BE DELETED
# GATEWAY RESPONSE TO CLOUD REQUEST TO NODE
def parse_gateway_response_to_cloud_to_node_req(msg, prefix) :
    """
    Parse the gateway response to a cloud request to a specific node

    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    result = [False,[]]
    good_length = False

    print(prefix + "type: " + str(msg.type))
    if msg.type in [gvar.MSG_TYPE_CLOUD_TO_NODE_SET_LED_ON, gvar.MSG_TYPE_CLOUD_TO_NODE_SET_LED_OFF, 
                gvar.MSG_TYPE_CLOUD_TO_NODE_SET_BLINKING]:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NO_ARGUMENTS:
            #no further parsing needed since message hass length 1 byte
            result = [True,[]]
            good_length = True

    elif msg.type in [gvar.MSG_TYPE_GW_SET_DIMMING, gvar.MSG_TYPE_CLOUD_TO_NODE_GET_DIMMING_STATUS]:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_SET_DIMMING_RESPONSE_MSG:
            result = parspec.parse_dimming_message(msg.payload,prefix)
            good_length = True

    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_NODE_SET_STRATEGY:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_SET_STRATEGY_RESPONSE_MSG:
            result = parspec.parse_set_strategy_message(msg.payload,prefix)
            good_length = True
            
    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_NODE_ECHO:
        print(prefix + "message length: " + str(len(msg.payload)))
        if len(msg.payload) == gvar.EXPECTED_LENGTH_SEND_ECHO_RESPONSE_MSG_FROM_NODE:
            result = parspec.parse_echo_response_gw_to_cloud(msg.payload,prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]
            
    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_LED_STATUS:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_LED_STATUS_RESPONSE_MSG:
            result = parspec.parse_led_status_response(msg.payload,prefix)
            good_length = True
            
    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_NUMBER_OF_NEIGHBOURS:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_NUMBER_OF_NEIGHBOURS_RESPONSE_MSG:
            result = parspec.parse_neighbour_number_response(msg.payload, prefix)
            good_length = True
            
    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_RSSI:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_RSSI_RESPONSE_MSG:
            result = parspec.parse_rssi_response(msg.payload,prefix)
            good_length = True

    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_HOPS:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_HOPS_RESPONSE_MSG:
            result = parspec.parse_hops_response(msg.payload,prefix)
            good_length = True
            
    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_NODE_STATUS:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_NODE_STATUS_RESPONSE_MSG_CLOUD:
            result = parspec.parse_node_status_response(msg.payload,prefix)
            good_length = True

    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_VERSION:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_NODE_VERSION_RESPONSE_MSG_CLOUD:
            result = parspec.parse_node_version_response(msg.payload,prefix)
            good_length = True
            
    elif msg.type == gvar.MSG_TYPE_ERROR:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_ERROR:
            result = parspec.parse_error_message(msg.payload,prefix)
            good_length = True
            
    
    else:
        print(prefix+"invalid message type!")# invalid or unsupported payload received.
        result[1] = [gvar.ERROR_TYPE_INVALID_MSG_TYPE]

    if good_length == False: # if length was wrong
        print(prefix + "unexpected message length")
        result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]
    
    return result

# GATEWAY RESPONSE TO CLOUD REQUEST TO GATEWAY
def parse_gateway_response_to_cloud_to_gateway_req(msg, prefix):
    """
    Parse the gateway response to a cloud request to a gateway

    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) -- 
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    result = [False, []]
    prefix = prefix + "parsing gateway response to cloud to gateway request > "
    good_length = False # bool to check if the expected length was met or not, assume not.

    if msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_NODE_LIST:          # variable ammount of bytes
        num_nodes = gvar.unpack_bytes('<H', msg.payload[7:9])           # num_nodes
        print(prefix+"num nodes " + str(num_nodes))
        if len(msg.payload) == gvar.expected_length_node_list(num_nodes, head_length=9):
            #no further parsing needed since message hass length 1 byte
            result = parspec.parse_node_list_client_id(msg.payload, num_nodes, prefix)
            good_length = True

    elif msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_REMOVE_NODES:        # variable ammount of bytes
        if len(msg.payload) == gvar.EXPECTED_LENGTH_CLOUD_RESPONSE_TO_GATEWAY_ADD_NODES_REQUEST_MSG:
            #no further parsing needed since message hass length 1 byte
            result = parspec.parse_crc_response(msg.payload)
            good_length = True

    elif msg.type in [gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_GATEWAY,gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_NODES]:        # update software
        print(prefix + "updating software parse message")
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NO_ARGUMENTS:
            #no further parsing needed since message hass length 3 bytes
            result = [True, []]
            good_length = True

    elif msg.type  == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_GET_GATEWAY_VERSION:        # gateway version
        print(prefix + "parsing gw version message")
        if len(msg.payload) == gvar.EXPECTED_LENGTH_GET_GATEWAY_VERSION_RESPONSE_MSG_CLOUD:
            #no further parsing needed since message hass length 3 bytes
            result = parspec.parse_gw_version_response(msg.payload)
            good_length = True

    elif msg.type == gvar.MSG_TYPE_ERROR:            # variable ammount of bytes
        if len(msg.payload) == gvar.EXPECTED_LENGTH_ERROR:
            result = parspec.parse_error_message(msg.payload)
            good_length = True

    else:
        print(prefix+"invalid message type!")# invalid or unsupported payload received.
        result[1] = [gvar.ERROR_TYPE_INVALID_MSG_TYPE]
        return result

    if good_length == False: # if length was wrong
        print(prefix + "unexpected message length")
        result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    return result

# GATEWAY REQUEST TO CLOUD
def parse_gateway_request_to_cloud(msg, prefix):
    """
    Parse the gateway request to a cloud

    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    prefix = prefix + "parsing gateway request to cloud > "
    result = [False,[]]

    if msg.type == gvar.MSG_TYPE_ALIVE_GW_TO_CLOUD:
        if len(msg.payload) == gvar.EXPECTED_LENGTH_NO_ARGUMENTS:
            result = [True,[]]
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_ADD_NODES_GW_TO_CLOUD or msg.type == gvar.MSG_TYPE_UNSEEN_NODES_GW_TO_CLOUD:  # add or remove nodes parsing
        num_nodes = gvar.unpack_bytes('<H', msg.payload[3:5])           # num_nodes
        print(prefix+"num nodes " + str(num_nodes))
        if len(msg.payload) == gvar.expected_length_node_list(num_nodes,head_length=5):
            result = parspec.parse_node_list(msg.payload, num_nodes, prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_NODE_STATUS_GW_TO_CLOUD:        # variable ammount of bytes
        num_nodes = gvar.unpack_bytes('<H', msg.payload[3:5])           # num_nodes
        print(prefix+"num nodes " + str(num_nodes))
        if len(msg.payload) == gvar.expected_length_node_status_list(num_nodes):
            result = parspec.parse_node_status_list(msg.payload, num_nodes, prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_ALARM_GW_TO_CLOUD:
        num_nodes = gvar.unpack_bytes('<H', msg.payload[4:6])           # num_nodes
        print(prefix+"num nodes " + str(num_nodes))
        if len(msg.payload) == gvar.expected_length_alarm_node_list(num_nodes) :
            result = parspec.parse_alarm_node_list(msg.payload, num_nodes, prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    elif msg.type == gvar.MSG_TYPE_ELECTRIC_PARAMETERS_GW_TO_CLOUD:            # variable ammount of bytes
        num_nodes = gvar.unpack_bytes('<H', msg.payload[3:5])           # num_nodes
        print(prefix+"num nodes " + str(num_nodes))
        if len(msg.payload) == gvar.expected_length_node_consum_list(num_nodes) :
            result = parspec.parse_node_electric_params_list(msg.payload, num_nodes, prefix)
        else:
            print(prefix + "unexpected message length")
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]

    else:
        print(prefix+"invalid message type")# invalid or unsupported payload received.
        result[1] = [gvar.ERROR_TYPE_INVALID_MSG_TYPE]

    return result



## END OF CLOUD SIMULATING PARSE FUNCTIONS <<<<













