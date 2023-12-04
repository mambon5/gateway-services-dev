"""
 Specific message display functions. We have here the display functions corresponding to each specific message type.
 Each message type has different arguments and properties that require a unique and special way of displaying it to the user 
 that received the message.
"""
import global_vars as gvar


def display_2_element_message(msg, type=""):
    """ Display messages with 2 arguments (message id and message type)
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param type: label that will be printed for message type
    :type type: string

    :return:
        None    
    """
    print("<simple 3 byte message>" + '\n'
            + "Raw data -> " + gvar._bytes_to_str_hex_format(msg.payload) + '\n'
            + "Message id -> " + str(msg.id)+ '\n'
            + "Message (" + str(type) + ") TYPE -> " + str(msg.type) 
            )

def display_3_element_message(msg, label, units = ""):
    """ Display messages with 3 arguments (message id, message type and an additional argument)
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param label: label that will be printed for the message argument
    :type label: string
    :param units: units for the 3rd message argument to display
    :type units: string

    :return:
        None
    """
    print("<simple 3 element message>" + '\n'
            + "Raw data -> " + gvar._bytes_to_str_hex_format(msg.payload) + '\n'
            + "Message id -> " + str(msg.id)+ '\n'
            + "Message TYPE -> " + str(msg.type)+ '\n'
            + label + " received -> " + str(msg.args[0]) + " " + units)

def display_4_element_message(msg, label1, label2, units1 = "", units2 = "", type = ""):
    """ Display messages with 4 arguments (message id, message type and 2 additional arguments)
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param label1: label that will be printed for the first message argument
    :type label1: string
    :param label2: label that will be printed for the second message argument
    :type label2: string
    :param units1: units for the 1st extra message argument to display
    :type units1: string
    :param units2: units for the 2nd extra message argument to display
    :type units2: string
    :param type: label that will be printed for message type
    :type type: string

    :return:
        None
    """

    print("<simple 4 element message>" + '\n'
            + "Raw data -> " + gvar._bytes_to_str_hex_format(msg.payload) + '\n'
            + "Message id -> " + str(msg.id)+ '\n'
            + "Message TYPE " + type + " -> " + str(msg.type)+ '\n'
            + label1 + " received -> " + str(msg.args[0]) + " " + units1 + '\n'
            + label2 + " received -> " + str(msg.args[1]) + " " + units2
            )
    
def display_n_element_message(msg, labels, units=[], type = ""):
    """ Display messages with n arguments. "n" arguments besides the 2 main ones
    (message id, message type and n additional arguments)
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param labels: labels that will be printed for the message arguments
    :type labels: list
    :param units: units for the extra message arguments to display
    :type units: list
    :param type: label that will be printed for message type
    :type type: string

    :return:
        None
    """
    prefix = "<display n element message> "
    n = len(labels)
    if n != len(units):
        print(prefix + "error: label length and units array length don't mathc! " )
        return
    if units == []: # we initialize all units to nothing, in case no units are given
        units = ["" for x in range(n)]

    text = """<{} element message>" \n
    Raw data -> {}  \n
    Message id -> {}\n
    Message TYPE {} -> {} \n""".format(n, gvar._bytes_to_str_hex_format(msg.payload), 
                                                                      str(msg.id), type, str(msg.type))
    for i in range(n):
            text = text + """{} received -> {} {} \n""".format(labels[i], str(msg.args[i]), units[i])

    print(text)

def display_dimming_response(msg):
    """ Display dimming message.
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    
    :return:
        None
    """
    display_3_element_message(msg, "dimming", "%")

def display_strategy_response(msg):
    """ Display strategy message.
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    
    :return:
        None
    """    
    display_3_element_message(msg, "strategy")

def display_alarm_response(msg):
    """ Display alarm message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    
    :return:
        None
    """    
    display_3_element_message(msg, "alarm", units = "")

def display_echo_response(msg):
    """ Display echo message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    
    :return:
        None
    """
    display_3_element_message(msg, "echo", units = "ms")

def display_led_status_response(msg):
    """ Display led status message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    
    :return:
        None
    """
    display_3_element_message(msg, "led status")

def display_neighbour_number_response(msg):
    """ Display number of neighbours message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    
    :return:
        None
    """
    display_3_element_message(msg, "num neighbours", "neighbours")

def display_rssi_response(msg):
    """ Display rssi message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    
    :return:
        None
    """
    display_3_element_message(msg, "rssi", units = "dB")

def display_hops_response(msg):
    """ Display hops message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    
    :return:
        None
    """
    display_3_element_message(msg,"hops")

def display_node_status_response(msg):
    """ Display node status message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    
    :return:
        None
    """
    print("<node status>" + '\n'
            + "Raw data -> " + gvar._bytes_to_str_hex_format(msg.payload) + '\n'
            + "Message id -> " + str(msg.id)+ '\n'
            + "Message TYPE -> " + str(msg.type) + '\n'
            + "led status received -> " + str(msg.args[0])+ '\n'
            + "Dimming received -> " + str(msg.args[1]) + '\n'
            + "num_neighbours received -> " + str(msg.args[2])+ '\n'
            + "rssi received -> " + str(msg.args[3])+ '\n'
            + "hops received -> " + str(msg.args[4]))

def display_node_version_response(msg):
    """ Display node version message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    
    :return:
        None
    """
    print("<node version>" + '\n'
            + "Raw data -> " + gvar._bytes_to_str_hex_format(msg.payload) + '\n'
            + "Message id -> " + str(msg.id)+ '\n'
            + "Message TYPE -> " + str(msg.type) + '\n'
            + "stack version -> v{}.{}.{}.{} \n".format(msg.args[0],msg.args[1],msg.args[2],msg.args[3])
            + "app version -> v{}.{}.{}.{} \n".format(msg.args[4],msg.args[5],msg.args[6],msg.args[7])
    )


def display_crc_response(msg, prefix=""):
    """ Display CRC message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    
    :return:
        None
    """
    display_3_element_message(msg, "crc")

def display_error_response(msg):
    """ Display error message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    
    :return:
        None
    """
    display_3_element_message(msg, "error")

def display_led_get_state_response_message(msg):
    """ Display led status message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    
    :return:
        None
    """
    display_3_element_message(msg, "led status")

def display_current_voltage_response(msg, args, prefix):
    """ Display current and voltage message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    :param args: estra message arguments
    :type args: list
    
    :return:
        None
    """    
    display_2_element_message(msg,"current and voltage")
    print(prefix + "details: " + '\n'
    + " voltage -> " + str(args[0])+ " V"+ '\n'
    + " current -> " + str(args[1]) + " mA")

def display_electrim_parameters_response(msg, args, prefix):
    """ Display node electrim parameters message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    :param args: estra message arguments
    :type args: list
    
    :return:
        None
    """    
    display_2_element_message(msg,"electric parameters")
    print(prefix + "details: " + '\n'
    + " voltage -> " + str(args[0])+ " V"+ '\n'
    + " current -> " + str(args[1]) + " mA" '\n'
    + " power -> " + str(args[2])+ " W"+ '\n'
    + " frequency -> " + str(args[3])+ " Hz" '\n'
    + " light level -> " + str(args[4]) + " %"+ '\n'
    + " running hours -> " + str(args[5]) + " min")

def display_solar_metrics_response(msg, prefix):
    """ Display the solar metrics message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    
    :return:
        None
    """    
    display_4_element_message(msg, "charge", "production", units1 = "Wh", units2 = "mW", type = "solar panel metrics")
    

def display_node_list(msg,  prefix="", type="", num_nodes = "", node_ids = ""): 
    """ Display the node id list message
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    :param type: label that will be printed for message type
    :type type: string
    :param num_nodes: number of nodes contained in the message
    :type num_nodes: int
    :param node_ids: list containing all the node ids to display
    :type node_ids: list

    :return:
        None
    """    
    prefix = prefix + type + " node list > " 
    if num_nodes == "":
        num_nodes = msg.args[0]
    if node_ids == "" :
        node_ids = msg.args[1]
    if num_nodes != len(node_ids) :
        print(prefix + "error, number of nodes mismatch in the parsed arguments")
        return    

    print(prefix + "node list contains " + str(num_nodes) + " node ids.")
    for node_id in node_ids:
        print(prefix + "node " + str(node_id))

def display_node_list_client_id(msg,  prefix="", type="", num_nodes = "", node_ids = ""): 
    """ Display the node id list message together with the client id
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    :param type: label that will be printed for message type
    :type type: string
    :param num_nodes: number of nodes contained in the message
    :type num_nodes: int
    :param node_ids: list containing all the node ids to display
    :type node_ids: list

    :return:
        None
    """    
    prefix = prefix + type + " node list > " 
    client_id = msg.args[0]
    if num_nodes == "":
        num_nodes = msg.args[1]
    if node_ids == "" :
        node_ids = msg.args[2]
    if num_nodes != len(node_ids) :
        print(prefix + "error, number of nodes mismatch in the parsed arguments")
        return    

    print(prefix + "client id: " + str(client_id)+ ", node list contains " + str(num_nodes) + " node ids.")
    for node_id in node_ids:
        print(prefix + "node " + str(node_id))



def display_node_status_list(msg, prefix) :   # node status list
    """ Display the node status list
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    
    
    
    :return:
        None
    """    
    prefix = prefix + "node status list > "
    num_nodes = msg.args[0]
    nodes = msg.args[1]
    if num_nodes != len(nodes) :
        print(prefix + "error, number of nodes mismatch in the parsed arguments")
        return    

    print(prefix + "node list contains " + str(num_nodes) + " node ids.")
    for node in nodes:              # each node has a led status, dimming , id, etc inside, given by the parsing function.
        print(prefix + "node " + str(node[0]) +" :" + '\n'
            + " led status -> " + str(node[1])+ '\n'
            + " dimming -> " + str(node[2]) + "%" '\n'
            + " num_neighbours -> " + str(node[3])+ '\n'
            + " rssi -> " + str(node[4])+ " dBm" + '\n'
            + " hops -> " + str(node[5]) + " jumps")

def display_alarm_node_list(msg, prefix) :
    """ Display the alarm and node list
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    
    :return:
        None
    """    
    prefix = prefix + "alarm node list > "
    alarm = msg.args[0]
    num_nodes = msg.args[1]
    nodes = msg.args[2]
    print(prefix + "alarm type: " + str(alarm))
    display_node_list(msg, prefix, num_nodes = num_nodes, node_ids = nodes)

def display_electrim_param_list(msg, prefix) :
    """ Display the list of node electric parameters
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    
    
    
    :return:
        None
    """    
    prefix = prefix + "consums node list > "
    num_nodes = msg.args[0]
    nodes = msg.args[1]
    if num_nodes != len(nodes) :
        print(prefix + "error, number of nodes mismatch in the parsed arguments")
        return    

    print(prefix + "node list contains " + str(num_nodes) + " node ids.")
    for node in nodes:              # each node has a led status, dimming , id, etc inside, given by the parsing function.
        print(prefix + "node " + str(node[0]) +" :" + '\n'
            + " voltage -> " + str(node[1])+ " V"+ '\n'
            + " current -> " + str(node[2]) + " mA" '\n'
            + " power -> " + str(node[3])+ " W"+ '\n'
            + " frequency -> " + str(node[4])+ " Hz" '\n'
            + " light level -> " + str(node[5]) + " %"+ '\n'
            + " running hours -> " + str(node[6]) + " min")


# DISPLAY CLOUD TO GATEWAY REQUESTS:

def display_client_id_msg(msg, prefix) :
    """ Display the cloud -> gateway messages with a client id.
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    
    :return:
        None
    """    
    prefix = prefix + "client id message > "
    display_3_element_message(msg, "client id", units = "")

def display_dimming_with_client_id_msg(msg, prefix) :
    """ Display the cloud -> gateway messages of dimming with a client id.
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    
    :return:
        None
    """    
    prefix = prefix + "client id message > "
    display_4_element_message(msg, "client id", "dimming", units1 = "", units2 = "%", type = prefix)

def display_remove_nodes_msg(msg, prefix) :
    """ Display the cloud -> gateway remove nodes message.
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    
    :return:
        None
    """    
    prefix = prefix + "remove nodes > "
    print(prefix + "remove node list received")
    display_node_list(msg,  prefix)

    
    
# DISPLAY GW RESPONSES TO CLOUD REQUESTS TO GATEWAY

def display_version_message(msg, prefix):
    """ 
    Display the gateway > cloud response for displaying gateway version message.
    
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: text to append to each console log or print
    :type prefix: string
    
    :return:
        None
    """    
    prefix = prefix + "gateway version > "
    print("{} gateway received")
    args = msg.args
    vers = args[0]
    version = "v{}.{}.{}.{}".format(vers[0],vers[1],vers[2],vers[3])
    msg.args = [version]
    display_3_element_message(msg, "version", units = "")