"""
Functions designed each for a specific message type. Each of this functions will take different arguments and create
specific payloads that might be combinded later by the calling functions to create the whole message payload.

1. There is a set of basic functions for general messages that just have 1 or 2 arguments.
2. The other functions (i.e. CRC, alarm, led on, etc) call the 1-argument message function, and 
    tell her that the only argument to put is *this alarm* or *this list of nodes* or whatever arguments they need to convert into bytes.
3. For messages that have many or a variable ammount of arguments, a specific function has been created for them.
"""
from struct import *
import random
import numpy as np

def set_1_arg_payload(args, packs="B"):
    """
    Set the argument payload for messages that only have 1 argument.
    
    :param args: argument to pack into bytes
    :type args: list
    :param packs: compression type
    :type packs: string

    :return:
        :payload: (bytes) -- packed argument

    :does:
        1. Checks whether the *arguments* is a *list* or an *int*
        2. According to each case, uses the **struct.pack** function to bring the *int* to *bytes* and returns the result

    """
    prefix = "set payload arguments "
    if type(args) == int :
        payload = pack("<"+packs, args)
    elif type(args) == list:
        if len(args) < 1:
            print(prefix + "error: no arguments specified" )   
            return
        payload = pack("<"+packs, args[0])
    else:
        print("error, args is not 'list' nor 'int'")
        payload = pack("<b", -1)
    return payload

def set_2_arg_payload(args, packs="BB"):
    """
    Set the argument payload for messages that only have 2 arguments.
    
    :param args: argument to pack into bytes
    :type args: list
    :param packs: compression type
    :type packs: string

    :return:
        :payload: (bytes) -- packed arguments
    """
    prefix = "set payload arguments "
    if type(args) == list:
        if len(args) < 2:
            print(prefix + "error: less than 2 arguments specified" )   
            return
        payload = pack("<"+packs, args[0], args[1])
    else:
        print("error, args is not 'list' nor 'int'")
        payload = pack("<b", -1)
    return payload

def gen_crc_message(args):
    """
    Transform the CRC into bytes from a normal message argument list

    :param args:  list of arguments containing CRC to use at position 0
    :type args: list

    :return:
        :payload: (bytes) -- generated payload corresonding to the crc

    """
    payload = pack_crc(args[0])
    return payload

def pack_crc(crc):
    """
    Put the CRC into bytes

    :param crc:  CRC to use
    :type crc: int
    :return:
        :payload: (bytes) -- generated payload corresonding to the crc
    """


    payload = pack("<I", crc)
    return payload

def set_dimming_msg_payload(args): 
    """
    Set the argument into bytes for dimming messages.
    
    :param args: dimming to pack into bytes
    :type args: list

    :return:
        :payload: (bytes) -- packed arguments
    """
    payload = set_1_arg_payload(args, "b")
    return payload


def set_strategy_msg_payload(args):    
    """
    Set the argument into bytes for strategy messages.
    
    :param args: strategy to pack into bytes
    :type args: list

    :return:
        :payload: (bytes) -- packed strategy
    """
    payload = set_1_arg_payload(args, "B")
    return payload

def set_echo_msg_payload(args=""):
    """
    Set the argument into bytes for echo messages.
    
    :param args: echo to pack into bytes
    :type args: list

    :return:
        :payload: (bytes) -- packed echo
    """
    if args=="":
        args = round(random.random()*400)*10 
    payload = set_1_arg_payload(args, "I")
    return payload

def send_node_status_msg_payload(args=[]):
    """
    Set the argument into bytes for node status list messages. So far it is inventing the status of the nodes, so
    this function should change.
    
    :param args: node status list to pack into bytes
    :type args: list containing: led status, dimming, num neighbours, rssi, hops

    :return:
        :payload: (bytes) -- packed node status list
    """
    if args == []:
        payload = pack("<BbIbB", round(random.random()), round(random.random()*101-0.5), 
                round(random.random()*420), round(random.random()*100-100), round(random.random()*256)
                )
    else :
        payload = pack("<BbIbB", args[0], args[1], args[2], args[3], args[4])
                
    return payload

def send_node_version_msg_payload(s_major, s_minor, s_revision, s_build, app_maj, app_min, app_rev, app_build, packs="BBBBBBBB") :
    """
    Set the message  argument into bytes for sending the node version.
    The node software version consists of a list of 8 int ranging from 0-254 which codify:
                
        1. *stack_version* major.minor.revision.build. These are the first 4 ints of the list.
        2. *app_version* major.minor.revision.build. These are the last 4 ints of the list.

    :param args: node version list to pack into bytes
    :type args: list containing: s_major, s_minor, s_revision, s_build, app_maj, app_min, app_rev, app_build and packs

    :return:
        :payload: (bytes) -- 8 bytes codifying the node version in bytes
    """
    payload = pack("<"+packs, s_major, s_minor, s_revision, s_build, app_maj, app_min, app_rev, app_build)
    return payload

def set_electrim_params_msg_payload():
    """
    Set the message argument into bytes for node electric parameters. Change this function, right now it is inventing the electrical
    parameters.

    :return:
        :payload: (bytes) -- randomly generated node consumption metrics, and packed into bytes
    """
    payload = pack("<HHHBBI", 220, 340, 460, 40, 80, 6500300)
    return payload

def set_solar_metrics_msg_payload():
    """
    Set the message argument into bytes for a node solar panel metrics. Change this function, right now it is inventing the solar
    parameters.
    

    :return:
        :payload: (bytes) -- randomly generated node solar panel metrics, and packed into bytes
    """
    payload = pack("<HH",2400, 140)
    return payload

def set_electric_params_list_msg_payload(num_nodes):
    """
    Set the message argument into bytes for a node electric parameters list. Change this function, right now it is inventing the electrical
    parameters.
    
    :param num_nodes:  number of nodes to use
    :type args: int

    :return:
        :payload: (bytes) -- randomly generated node consumption metrics list, and packed into bytes
    """
    payload = pack("<HQHHHBBIQHHHBBIQHHHBBI",3, 141, 220, 340, 460, 40, 80, 6500300,142,220, 440, 160, 40, 20, 6506600,144, 220, 290, 190, 40, 28, 6502400)
    return payload

def node_id_list_payload(node_ids):
    """
    Set the message argument into bytes for a given node id list
    
    :param node_ids:  array containing all node id's
    :type node_ids: int array

    :return:
        :payload: (bytes) -- generated node id list, and packed into bytes
    """
    num_nodes = len(node_ids)
    payload = pack("<H",num_nodes)
    for i in range(num_nodes):
        payload = payload + pack("<Q", node_ids[i] )
    return payload

def random_node_id_list_payload(num_nodes):
    """
    Set the message argument into bytes for a random node id list. Change this function, right now it is inventing the node ids.
    
    :param num_nodes:  number of nodes to use
    :type args: int

    :return:
        :payload: (bytes) -- randomly generated node id list, and packed into bytes
    """
    node_ids = gen_random_node_id_list(num_nodes)
    payload = node_id_list_payload(node_ids)
    return payload

def random_node_status_list_payload(num_nodes):
    """
    Set the argument payload for random node status list messages.
    
    :param num:nodes:  number of nodes to use
    :type args: int

    :return:
        :payload: (bytes) -- randomly generated node list status, and packed into bytes
    """
    payload = pack("<H",num_nodes)
    for i in range(num_nodes):
        payload = payload + pack("<QBbIbB",140+i, round(random.random()), round(random.random()*101-0.5), 
                round(random.random()*420), round(random.random()*100-100), round(random.random()*256)
                )
    return payload

def random_alarm_node_list_payload(num_nodes):
    """
    Set the message argument into bytes for a random alarm and node id list. Change this function, right now it is inventing the node alarms.
    
    :param num:nodes:  number of nodes to use
    :type args: int

    :return:
        :payload: (bytes) -- randomly generated alarm and node id list, and packed into bytes
    """
    payload = pack("<BH", round(random.random()*7+1), num_nodes)
    for i in range(num_nodes):
        payload = payload + pack("<Q",140+i )
    return payload

def set_remove_nodes_msg_payload(num_nodes):
    """
    Set the message argument into bytes for a remove nodes list. Right now it is inventing the node ids.
    
    :param num:nodes:  number of nodes to use
    :type args: int

    :return:
        :payload: (bytes) -- randomly generated node id list, and packed into bytes
    """
    payload = random_node_id_list_payload(num_nodes)
    return payload

# gw response to clodu request to gw

def respond_remove_nodes_msg_payload(args):
    """
    Set the message argument into bytes for a remove nodes list. argument into bytes
    
    :param args:  list containig the arguments to use when answering the cloud
    :type args: list

    :return:
        :payload: (bytes) -- crc generated message, this is just a crc message!
    """
    payload = random_node_id_list_payload(args[0])
    return payload


# create functions gateway <<>> cloud response

# def set_dimming_with_client_id_msg_payload(args): 
#     """
#     Set the argument argument into bytes for dimming with client id messages.
    
#     :param args: [client_id, dimming] to pack into bytes
#     :type args: list

#     :return:
#         :payload: (bytes) -- packed arguments
#     """
#     print("set dimming> args: " + str(args))
#     payload = set_2_arg_payload(args, "Ib")
#     return payload

def set_client_id_msg_payload(args):
    """
    Set the message argument into bytes for the client id    

    :return:
        :payload: (bytes) -- randomly generated node consumption metrics, and packed into bytes
    """
    client_id = args[0]
    payload = pack("<I",client_id)
    return payload


def node_id_list_client_id_payload(args):
    """
    Set the message argument into bytes for a message with client id and node id list
    
    ::param args:  list of 2 elements containing the *client_id* and the *node_id_list* to send to cloud
    :type args: list

    :return:
        :payload: (bytes) -- generated node id list, and packed into bytes
    """
    prefix = "<creating node id list with client id payload> "
    client_id = args[0]
    node_ids = args[1]
    num_nodes = len(node_ids)
    payload = pack("<IH",client_id, num_nodes)
    print(prefix + " client_id: " + str(client_id) + ", num_nodes: " + str(num_nodes) + ", node list: " + str(node_ids))
    print(prefix)
    for i in range(num_nodes):
        payload = payload + pack("<Q", node_ids[i] )
    return payload



# auxiliary functions for creating the message payload

def gen_random_node_id_list(num_nodes):
    """
    Generate a random list of node ids, of length given by the argument
    
    :param num_nodes:  number of nodes to use
    :type num_nodes: int
    :return:
        :list: (np.array) -- generated node id list, as a numpy array
    """

    list = np.arange(num_nodes) + 140
    return list


# simulated, ready to be deleted:
# cloud response to gateway request
def set_alarm_and_crc_msg(alarm, crc):
    """
    Set the message argument into bytes for a cloud response to a previous gateway request with an alarm and many nodes to it
    
    :param alarm:  the alarm that the gateway sent to the cloud
    :type alarm: int
    :param payload: received message payload that we want to transform into a CRC
    :type payload: bytes

    :return:
        :payload: (bytes) -- generated node id list, and packed into bytes
    """
    args = [alarm, crc]
    payload = set_2_arg_payload(args, "BI")
    return payload
    
def gen_gw_version_message(args):
    """
    Set the message argument into bytes for a cloud response to a previous gateway request with the gateway version
    
    :param alarm:  the alarm that the gateway sent to the cloud
    :type alarm: int
    :param payload: received message payload that we want to transform into a CRC
    :type payload: bytes

    :return:
        :payload: (bytes) -- generated node id list, and packed into bytes
    """
    version = args[0]
    payload = pack("<BBBB", version[0], version[1], version[2], version[3])
    return payload