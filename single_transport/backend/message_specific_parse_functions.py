"""
    Script containing parsing functions that depend on the

    - message type

    For each message type a different parsing function is called. These functions are called by the more general
    parse script.
    """

import global_vars as gvar
from struct import *

def parse_error_message(payload, prefix=""):
    """
    Parse the error message

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    print(prefix+"parsing error message...")
    error = gvar.unpack_bytes('<B', payload[3:]) # error number
    args = [error]

    return [True, args]

def parse_echo_response(traveltime,prefix=""):
    """ 
    Parse the echo message. 
    
    :note: It is unclear whether we have to use the *travel_time_ms* as the travel time in milliseconds, 
           or whether we have to transform it using the documentation.
       

    :references: 
        - Check out how to pass traveltime to millisecons as described on page 17 of this manual: https://wirepas.github.io/wm-sdk/master/d6/d50/wms__data_8h.html#a458421a43d4f6dc515faf427bf579d00
            Basically we have to multiply the traveltime units by 1000/128 in order to obtain the value of travel time 
            in milliseconds
        - Understanding the difference between *propagation delay* and *transmission delay* : https://www.baeldung.com/cs/propagation-vs-transmission-delay

    :param traveltime: transmition delay from node to sink, in seconds / 128
    :type traveltime: int
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return: The travel time transmission delay in milliseconds
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    # Fill fields list with new payload data
    print(prefix+"parsing echo message...")
    travel_time = round(traveltime*1000/128) # echo request travel time
    args = [travel_time]

    return [True, args]

# to be deleted in production:
def parse_echo_response_gw_to_cloud(payload,prefix=""):
    """ Parse the echo response from a gateway for a simulated cloud. 
    It receives the payload in bytes and calls the standard *parse_echo_response* function.

    :param payload: message payload
    :type payload: bytes

    :return: The travel time transmission delay in milliseconds
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    trav_time = gvar.unpack_bytes("<I", payload[3:])
    result = parse_echo_response(trav_time, prefix)
    return result

def parse_led_status_response(payload, prefix=""):
    """ Parse the led status message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    # Fill fields list with new payload data
    print(prefix + "parsing led status message...")
    led_status = gvar.unpack_bytes('<b', payload[3:]) # led status
    args = [led_status]

    return [True, args]

def parse_neighbour_number_response(payload, prefix=""):
    """ Parse the number of neighbours message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """

    # Fill fields list with new payload data
    print(prefix+"parsing neighbour number message...")
    num_neighbours = gvar.unpack_bytes('<I', payload[3:]) # number of neighbours
    args = [num_neighbours]

    return [True, args]

def parse_rssi_response(payload, prefix=""):
    """ Parse the rssi message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    # Fill fields list with new payload data
    print(prefix+"parsing rssi message...")
    rssi = gvar.unpack_bytes('<b', payload[3:]) # rssi
    args = [rssi]

    return [True, args]


def parse_hops_response_from_node(hops, prefix):
    """ Parse the hops message from node to gateway.    

    :param hops: the number of hops, sent by wirepass automatically in the message header
    :type hops: int
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    # Fill fields list with new payload data
    print(prefix+"parsing hops message node to gateway...")
    args = [hops] # number of hops

    return [True, args]

def parse_hops_response(payload,prefix=""):
    """ Parse the hops message from gateway to cloud.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    # Fill fields list with new payload data
    print(prefix+"parsing hops message gw to cloud...")
    hops = gvar.unpack_bytes('<B', payload[3:]) # number of hops
    args = [hops]

    return [True, args]

def parse_node_status_response(payload, prefix=""):
    """ Parse the node status from message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    # Fill fields list with new payload data, here come 15 bytes with different kinds of info
    # the first byte contains the message type
    print(prefix + "parsing node status message...")
    led_status = gvar.unpack_bytes('<b', payload[3:4]) # led status
    dimming = gvar.unpack_bytes('<b', payload[4:5]) # dimming
    num_neighbours = gvar.unpack_bytes('<I', payload[5:9]) # number of neighbours
    rssi = gvar.unpack_bytes('<b', payload[9:10]) # rssi
    hops = gvar.unpack_bytes('<B', payload[10:11]) # number of hops
    args = [led_status, dimming, num_neighbours, rssi, hops]

    return [True, args]

def parse_node_status_response_from_node(payload, rawdata, prefix=""):
    """ Parse the node status from message, for node responses to gw.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param rawdata: raw data sent by wirepas automatically from the node to the sink in the message.
    :type rawdata: JSON
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    # Fill fields list with new payload data, here come 15 bytes with different kinds of info
    # the first byte contains the message type
    print(prefix + "parsing node status message...")
    led_status = gvar.unpack_bytes('<b', payload[3:4]) # led status
    dimming = gvar.unpack_bytes('<b', payload[4:5]) # dimming
    num_neighbours = gvar.unpack_bytes('<I', payload[5:9]) # number of neighbours
    rssi = gvar.unpack_bytes('<b', payload[9:10]) # rssi
    hops = rawdata.hop_count                 # number of hops
    args = [led_status, dimming, num_neighbours, rssi, hops]

    return [True, args]


def parse_node_version_response(payload, prefix=""):
    """ Parse the node version from message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. In particular a list of 8 elements, each of them an int (0-254 possible values)
            representing the stack and app version of the node software.
    """
    # Fill fields list with new payload data, here come 15 bytes with different kinds of info
    # the first byte contains the message type
    print(prefix + "parsing node version message...")
    stack_major = gvar.unpack_bytes('<B', payload[3:4]) # stack major
    stack_minor = gvar.unpack_bytes('<B', payload[4:5]) # stack minor
    stack_revision = gvar.unpack_bytes('<B', payload[5:6]) # stack revision
    stack_build = gvar.unpack_bytes('<B', payload[6:7]) # stack build
    app_major = gvar.unpack_bytes('<B', payload[7:8]) # app major
    app_minor = gvar.unpack_bytes('<B', payload[8:9]) # app minor
    app_revision = gvar.unpack_bytes('<B', payload[9:10]) # app revision
    app_build = gvar.unpack_bytes('<B', payload[10:11]) # app build
    args = [stack_major, stack_minor, stack_revision, stack_build, app_major, app_minor, app_revision, app_build]

    return [True, args]


def get_crc(payload, ini=3, fi=5):    
    """ Parse the crc from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param ini: first byte where the crc is
    :type ini: int    
    :param fi: lst byte where the crc is
    :type fi: int    

    :return:
        **args** (*list*) --  the CRC number
    """
    crc = gvar.unpack_bytes('<H', payload[ini:fi]) # crc
    args = [crc]
    return args


# CLOUD REQUEST to NODE
def parse_set_strategy_message(payload, prefix):
    """ Parse the strategy from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    print(prefix+"parsing (node) strategy cloud request...")
    strategy = gvar.unpack_bytes('<B', payload[3:4]) # strategy
    args = [strategy]
    return [True, args]

def parse_dimming_message(payload, prefix):
    """ Parse the dimming from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    print(prefix+"parsing dimming cloud request...")
    dimming = gvar.unpack_bytes('<b', payload[3:4]) # dimming
    print(prefix+"found a dimming of " + str(dimming))
    args = [dimming]
    return [True, args]


# CLOUD TO GATEWAY REQUEST

def parse_cloud_to_gateway_request_generic_client_id(payload, prefix):
    """ Parse the client id from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* List of parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """

    print(prefix+"parsing client id from cloud to gw request...")
    id_client = get_client_id(payload)           # client id
    args = [id_client]
    return [True, args]

def parse_dimming_message_client_id(payload, prefix):
    """ Parse the client id and dimming from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """

    print(prefix+"parsing client id and dimming...")
    id_client = get_client_id(payload)           # client id
    dimming = gvar.unpack_bytes('<b', payload[7:8])           # dimming
    args = [id_client, dimming]
    return [True, args]

def parse_node_list_client_id(payload, num_nodes, prefix, firstb=9):
    """ Parse the node id list and client id from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes 
    :param num_nodes: number of nodes
    :type num_nodes: int
    :param prefix: text to append to each console log or print
    :type prefix: string 
    :param firstn: first byte of the node id list to parse
    :type firstn: int 
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1][0] - client id
            - [1][1] - number of nodes
            - [1][2] - node id list
    """

    print(prefix+"parsing client id and node list...")
    id_client = get_client_id(payload)           # client id
    preresult = parse_node_list(payload, num_nodes, prefix, firstb=firstb)
    node_list = preresult[1][1]           # node id list
    args = [id_client, num_nodes, node_list]
    return [True, args]

def parse_node_status_list_client_id(payload, num_nodes, prefix, firstb=9):
    """ Parse the node status list and client id from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes 
    :param num_nodes: number of nodes
    :type num_nodes: int
    :param prefix: text to append to each console log or print
    :type prefix: string 
    
    :return:
        **result** (*list*) --  [0] - bool (True if successful, False if failed)
                                [1][0] - client id
                                [1][1] - number of nodes
                                [1][2] - node status list
    """
    print(prefix+"parsing client id and node status list...")
    id_client = get_client_id(payload)           # client id
    preresult = parse_node_status_list(payload, num_nodes, prefix, firstb=firstb)
    node_stat_list = preresult[1][1]           # node id list
    args = [id_client, num_nodes, node_stat_list]
    return [True, args]

# def parse_update_software(payload, prefix=""):
#     """ Parse the device number from the message.    

#     :param payload: Message payload in bytes that we wish to parse
#     :type payload: bytes 
#     :param prefix: text to append to each console log or print
#     :type prefix: string 
    
#     :return:
#         **result** (*list*) --  [0] - bool (True if successful, False if failed)
#                                 [1] - no parameters yet
#     """
#     print(prefix+"parsing extra parameters for the software update...")
    
#     return [True, []]



# RESPONSE from CLOUD to GATEWAY request to cloud
def parse_alarm_response(payload):
    """ Parse the alarm and crc from the response .    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes

    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    print("parsing alarm cloud response...")
    alarm = gvar.unpack_bytes('<B', payload[3:4]) # alarm
    crc = get_crc(payload,4,6)[0]          # should specify the byte positions that contain the crc code
    args = [alarm, crc]
    return [True, args]

def parse_crc_response(payload):
    """ Parse the CRC number for a response message

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes

    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *int* parsed CRC. 
    """
    print("parsing crc response...")
    args = get_crc(payload)
    return [True, args]

def parse_gw_version_response(payload):
    """ 
    Parse the gateway version number for a response message

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes

    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* list with the 4 integer numbers represenenting together the version id number
    """
    print("parsing gateway version response...")
    version = unpack('<BBBB', payload[3:7]) # gateway version 
    args = [version]
    return [True, args]

# def _parse_cloud_to_gateway_dimming_request(msg):
#     print("parsing dimming cloud to gateway request...")
#     msg.dimming = gvar.unpack_bytes('<B', msg.payload[3:4]) # alarm
#     msg.args = [msg.dimming]

#  NODE REQUESTS to GATEWAY parsing functions 
def parse_node_alarm_request(payload):
    """ Parse the node alarm from the request.

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes 
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    print("parsing alarm node request...")
    alarm = gvar.unpack_bytes('<B', payload[3:4]) # alarm
    args = [alarm]

    return [True, args]

def parse_current_voltage(payload):
    """ Parse the node electric parameters from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes 
    /watch
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    voltage = gvar.unpack_bytes('<H', payload[0:2]) # voltage
    current = gvar.unpack_bytes('<H', payload[2:4]) # current
    change_type = gvar.unpack_bytes('<B', payload[4:5]) # change type

    args = [voltage, current, change_type]
    return [True, args]

def parse_electric_parameters(payload):
    """ Parse the node electric parameters from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes 
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    voltage = gvar.unpack_bytes('<H', payload[0:2]) # voltage
    current = gvar.unpack_bytes('<H', payload[2:4]) # current
    power = gvar.unpack_bytes('<H', payload[4:6]) # power
    frequency = gvar.unpack_bytes('<B', payload[6:7]) # frequency
    light_lev = gvar.unpack_bytes('<B', payload[7:8]) # light_lev
    run_hours = gvar.unpack_bytes('<I', payload[8:12]) # run_hours
    
    args = [voltage, current, power, frequency, light_lev, run_hours]
    return [True, args]


def parse_electric_parameters_from_message(payload):
    """ Parse the node consumptions from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes 
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    print("parsing basic consumption node request...")
    
    args = parse_electric_parameters(payload[3:15])

    return[True, args]

def parse_node_solar_metrics_request(payload):
    """ Parse the node solar metrics from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes 
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    print("parsing solar panel metrics node request...")
    charge = gvar.unpack_bytes('<H', payload[3:5]) # charge
    production = gvar.unpack_bytes('<H', payload[5:7]) # production
    
    args = [charge, production]

    return [True, args]

def parse_node_status_request(payload, prefix=""):
    """ Parse the node status from message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes
    :param prefix: text to append to each console log or print
    :type prefix: string    
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* Parsed arguments. Depending on the **message type** these arguments can be more or fewer
    """
    # Fill fields list with new payload data, here come 15 bytes with different kinds of info
    # the first byte contains the message type
    print(prefix + "parsing node status message...")
    led_status = gvar.unpack_bytes('<b', payload[3:4]) # led status
    dimming = gvar.unpack_bytes('<b', payload[4:5]) # dimming
    num_neighbours = gvar.unpack_bytes('<I', payload[5:9]) # number of neighbours
    rssi = gvar.unpack_bytes('<b', payload[9:10]) # rssi
    args = [led_status, dimming, num_neighbours, rssi]

    return [True, args]


# GATEWAY RESPONSE TO CLOUD request to gateway

def parse_node_list(payload, num_nodes, prefix, firstb=5): 
    """ Parse the node id list from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes 
    :param num_nodes: number of nodes
    :type num_nodes: int
    :param prefix: text to append to each console log or print
    :type prefix: string 
    :param firstn: first byte of the node id list to parse
    :type firstn: int 
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1][0] - number of nodes
            - [1][1] - node id list
    """
    print(prefix + "parsing node list..")
    node_ids = []
    if num_nodes > 0 :
        for i in range(num_nodes):
            ini = firstb + 8*i # first byte of the list of nodes
            fi = ini + 8
            node_id = gvar.unpack_bytes('<Q', payload[ini:fi]) # node id
            node_ids.append(node_id) 
    return [True, [num_nodes, node_ids]]



# function that unpacks a node status list into an array [true, [num_nodes, node_list]]
def parse_node_status_list(payload, num_nodes, prefix, firstb=5) :   # node status list
    """ Parse the node status list from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes 
    :param num_nodes: number of nodes
    :type num_nodes: int
    :param prefix: text to append to each console log or print
    :type prefix: string 
    
    :return:
        **result** (*list*) --  [0] - bool (True if successful, False if failed)
                                [1][0] - number of nodes
                                [1][1] - node status list
    """
    
    print(prefix + "parsing node status list..")
    nodes = []
    if num_nodes > 0 :
        for i in range(num_nodes):
            ini = firstb + 16*i
            fi = ini + 16 
            node_id = gvar.unpack_bytes('<Q', payload[ini:ini+8]) # node id
            led_state = gvar.unpack_bytes('<B', payload[ini+8:ini+9]) # led state
            dimming = gvar.unpack_bytes('<b', payload[ini+9:ini+10]) # dimming
            neighb = gvar.unpack_bytes('<I', payload[ini+10:ini+14]) # neighbours
            rssi = gvar.unpack_bytes('<b', payload[ini+14:ini+15]) # rssi
            hops = gvar.unpack_bytes('<B', payload[ini+15:fi]) # hops
            nodes.append([node_id, led_state, dimming, neighb, rssi, hops]) 
    return [True, [num_nodes, nodes]]

def parse_node_electric_params_list(payload, num_nodes, prefix, firstb=5) :
    """ Parse the node electrical parameters list from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes 
    :param num_nodes: number of nodes
    :type num_nodes: int
    :param prefix: text to append to each console log or print
    :type prefix: string 
    
    :return:
        **result** (*list*) --  [0] - bool (True if successful, False if failed)
                                [1][0] - number of nodes
                                [1][1] - node id list
    """
    print(prefix + "parsing node consum list..")
    nodes = []
    if num_nodes > 0 :
        for i in range(num_nodes):
            ini = firstb + 20*i
            fi = ini + 20
            node_id = gvar.unpack_bytes('<Q', payload[ini:ini+8]) # node id
            node_id= [node_id]
            electricp = parse_electric_parameters(payload[ini+8:fi])
            node_id.extend(electricp)
            nodes.append(node_id) 
    return [True, [num_nodes, nodes]]

def parse_alarm_node_list(payload, num_nodes, prefix) :
    """ Parse the alarm and node id list from the message.    

    :param payload: Message payload in bytes that we wish to parse
    :type payload: bytes 
    :param num_nodes: number of nodes
    :type num_nodes: int
    :param prefix: text to append to each console log or print
    :type prefix: string 
    
    :return:
        **result** (*list*) --  [0] - bool (True if successful, False if failed)
                                [1][0] - alarm type
                                [1][1] - number of nodes
                                [1][2] - node id list
    """
    print(prefix + "parsing node alarm list..")
    alarm = gvar.unpack_bytes('<B', payload[3:4]) # alarm
    result1 = parse_node_list(payload, num_nodes, prefix, firstn=6) # node ids
    bool = result1[0]
    num_nodes = result1[1][0]
    node_list = result1[1][1] 
    return [bool, [alarm, num_nodes, node_list]] # result is [True, [alarm, num_nodes, node_list]]

def get_client_id(payload) :
    id_client = gvar.unpack_bytes('<I', payload[3:7])   
    return id_client