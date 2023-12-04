"""
Set of functions and cases that determine when and how the gateway database is read.
"""

import global_vars as gvar
import create_message_specific_functions as cmsgsp
import otap_specific_functions as ospef


def read_gw_database(msg, mode=None, interlocutor=None, interac=None):
    """
    
    Function that reads the gateway database.

    :does:
        1. It checks the interlocutor (cloud/nodes)
        2. It calls either the:
            - :py:meth:`~read_gw_database.read_gw_database_nodes` if the interlocutor is *nodes*
            - :py:meth:`~read_gw_database.read_gw_database_cloud` if the interlocutor is *cloud*
     
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param mode: either "listen" or "request"
    :type mode: string 
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* return arguments. Depending on the **message type** these arguments can be more or fewer
        """
    
    prefix = "<read gw database> "
    result = [False, []]

    # node - gateway message
    if interlocutor == "nodes":
        result = read_gw_database_nodes(msg, mode, prefix)
    elif interlocutor == "cloud":
        result = read_gw_database_cloud(msg,prefix, interac)
    else:
        print(prefix + "error: invalid message origin detected")

    return result

def read_gw_database_nodes(msg, mode, prefix=""):
    """
    Function that reads the gateway database according to:
        1. the message mode
        2. the message type
     
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param mode: either "listen" or "request"
    :type mode: string  
     
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* return arguments. Depending on the **message type** these arguments can be more or fewer

        """
    
    prefix = prefix + "from node message> "
    result = [False, []]

    # NODE RESPONSE TO GATEWAY REQUEST
    if mode == "request":
        prefix = prefix + " node response to gateway request> "
        # discriminate according to message type:
        if msg.type in [    gvar.MSG_TYPE_ERROR,
                            gvar.MSG_TYPE_GW_SET_LED_ON ,
                            gvar.MSG_TYPE_GW_SET_LED_OFF,
                            gvar.MSG_TYPE_GW_SET_DIMMING,
                            gvar.MSG_TYPE_GW_SET_BLINKING,
                            gvar.MSG_TYPE_GW_SET_STRATEGY,
                            gvar.MSG_TYPE_GW_ECHO,
                            gvar.MSG_TYPE_GW_SEND_NEW_STRAGEGY]:
            prefix = prefix + " send command> "
            print(prefix + "no action needed yet")
            result = [True, []]
        
        elif msg.type in [  gvar.MSG_TYPE_GW_GET_LED_STATUS,
                            gvar.MSG_TYPE_GW_GET_DIMMING_STATUS,
                            gvar.MSG_TYPE_GW_GET_NUMBER_OF_NEIGHBOURS,
                            gvar.MSG_TYPE_GW_GET_RSSI,
                            gvar.MSG_TYPE_GW_GET_NODE_STATUS]:
            prefix = prefix + " received node information> "
            print(prefix + "should read the database with the received information, but no database is available yet :/")
            result = [True, []]

        else:
            print(prefix + "error: no action detected for given msg type: " + str(msg.type))

    
    # NODE REQUEST TO GATEWAY
    elif mode == "listen":
        prefix = prefix + " node request to gateway> "
        # discriminate according to message type:
        
        if msg.type == gvar.MSG_TYPE_NODE_GET_TIME:
            prefix = prefix + " other> "
            print(prefix + "no action needed yet")
            result = [True, []]

        elif msg.type in [  gvar.MSG_TYPE_NODE_SEND_ALARM,
                            gvar.MSG_TYPE_NODE_SEND_CURRENT_VOLTAGE,
                            gvar.MSG_TYPE_NODE_SEND_ELECTRIC_PARAMETERS,
                            gvar.MSG_TYPE_NODE_SEND_SOLAR_PANEL_METRICS,
                            gvar.MSG_TYPE_NODE_SEND_NODE_STATUS]:
            prefix = prefix + " received node information> "
            print(prefix + "no action needed yet")
            result = [True, []]
            
        else:
            print(prefix + "error: no action detected for given msg type: " + str(msg.type))

    else:
        print(prefix + "error: invalid message mode detected")

    

    return result


def read_gw_database_cloud(msg, prefix="", interac=None):
    """
    Function that reads the gateway database according to:
        1. message type
     
    This function is also responsible for extracting the gateway version from the file `global_vars.py` when required.
        
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: prefix to append to every message print
    :type prefix: string

    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* return arguments. Depending on the **message type** these arguments can be more or fewer
        
        
        """
    
    prefix = prefix + "from cloud message> "
    result = [False, []]

    # CLOUD TO NODE REQUEST
    if msg.sub_supertopic == gvar.CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC:
        prefix = prefix + " cloud to node> "
        if msg.type == gvar.MSG_TYPE_GW_SEND_NEW_STRAGEGY:
            prefix = prefix + " new strategy> "
            print(prefix + "right now a new strategy should be inserted into the database, but no database is configured yet :(")
            result = [True, []]
        elif msg.type in [  gvar.MSG_TYPE_ERROR,
                            gvar.MSG_TYPE_GW_SET_LED_ON ,
                            gvar.MSG_TYPE_GW_SET_LED_OFF,
                            gvar.MSG_TYPE_GW_SET_DIMMING,
                            gvar.MSG_TYPE_GW_SET_BLINKING,
                            gvar.MSG_TYPE_GW_SET_STRATEGY,
                            gvar.MSG_TYPE_GW_ECHO,
                            gvar.MSG_TYPE_GW_GET_LED_STATUS,
                            gvar.MSG_TYPE_GW_GET_DIMMING_STATUS,
                            gvar.MSG_TYPE_GW_GET_NUMBER_OF_NEIGHBOURS,
                            gvar.MSG_TYPE_GW_GET_RSSI,
                            gvar.MSG_TYPE_GW_GET_HOPS,
                            gvar.MSG_TYPE_GW_GET_NODE_STATUS,
                            gvar.MSG_TYPE_CLOUD_TO_NODE_GET_VERSION]:

            prefix = prefix + " other> "
            print(prefix + "no action needed yet")
            result = [True, []]          
        else:
            print(prefix + "error: no action detected for given msg type: " + str(msg.type))

    # CLOUD TO GATEWAY REQUEST
    elif msg.sub_supertopic == gvar.CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
        prefix = prefix + " cloud to gateway> "
        # discriminate according to message type:
        if msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_NODE_LIST: # CLOUD -> GATEWAY: read node list
            prefix = prefix + " get node list> "
            print(prefix + "right now nodes should be read from the database, but no database is configured yet, so we will try to get them",
                  "directly from the sink, and if that fails we will invent them!")
            node_list = None
            try:
                otapHelper = gvar.create_otaphelper(interac.wni)
                node_list = ospef.get_node_list(otapHelper)
            except Exception as err:
                print("{} failed to create OtapHelper or extract node list from sink, error {}".format(prefix, err))
            if node_list != None and node_list != []:
                print("{} could extract a non-emtpy node list form the sink!".format(prefix))
            else:
                num_nodes = 9
                node_list = cmsgsp.gen_random_node_id_list(num_nodes)
                print("{} generating random node list".format(prefix))
            
            print(prefix + "nodes 'read' from database: " + str(node_list))
            result = [True, [node_list]]

        elif msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_GET_GATEWAY_VERSION:
            # extract the gateway version from database or global var
            prefix = "{} gw version >".format(prefix)
            gw_version = gvar.GATEWAY_VERSION.split(".")
            gw_version = list(map(int, gw_version))
            print("{} version: {}".format(prefix, gw_version))
            result = [True, [gw_version]]
    
        elif msg.type in gvar.MSG_CLOUD_TO_GATEWAY_REQUESTS_LIST:
            prefix = prefix + " other> "
            print(prefix + "no action needed yet")
            result = [True, False, []]
        else:
            print(prefix + "error: no action detected for given msg type: " + str(msg.type))
    
    # CLOUD RESPONSE TO GATEWAY REQUEST
    elif msg.sub_supertopic == gvar.CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_SUPERTOPIC:
        prefix = prefix + " cloud response to gateway request> "
        # discriminate according to message type:
        if msg.type in [ gvar.MSG_TYPE_ALIVE_GW_TO_CLOUD,
                        gvar.MSG_TYPE_ADD_NODES_GW_TO_CLOUD,
                        gvar.MSG_TYPE_UNSEEN_NODES_GW_TO_CLOUD,
                        gvar.MSG_TYPE_NODE_STATUS_GW_TO_CLOUD,
                        gvar.MSG_TYPE_ALARM_GW_TO_CLOUD,
                        gvar.MSG_TYPE_ELECTRIC_PARAMETERS_GW_TO_CLOUD]:
            prefix = prefix + " other> "
            print(prefix + "no action needed yet")
            result = [True, []]
        else:
            print(prefix + "error: no action detected for given msg type: " + str(msg.type))

    # to be deleted from production: (simulates cloud behaviour)

    # GATEWAY REQUEST TO CLOUD (no gateway database read needed)
    elif msg.sub_supertopic == gvar.GATEWAY_REQUEST_TO_CLOUD_MQTT_SUPERTOPIC:
        prefix = prefix + " gateway request to cloud> "
        print(prefix + "no action needed for fake cloud simulation from the gateway")
        result = [True, []]

    else:
        print(prefix + "error: invalid message origin detected")

    

    return result