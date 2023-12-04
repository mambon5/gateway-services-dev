"""
Set of functions that will take care of updating the gateway database according to the message type received.

"""

import global_vars as gvar
import compute_crc as get_crc


def update_gw_database(msg, mode=None, interlocutor=None, interac=None):
    
    """
    Function that updates the gateway database.
     
     :does:
        1. It checks the interlocutor (cloud/nodes)
        2. It calls either the:
            - :py:meth:`~update_gw_database.update_gw_database_nodes` if the interlocutor is *nodes*
            - :py:meth:`~update_gw_database.update_gw_database_cloud` if the interlocutor is *cloud*

    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param mode: either "listen" or "request"
    :type mode: string  
    :param interlocutor: whether node is "cloud" or "nodes" mode
    :type interlocutor: string
     
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *bool* True if database is changed, False if no changes were made
            - [2] - *list* return arguments. Depending on the **message type** these arguments can be more or fewer
        
        
        """
    
    prefix = "<update gw database> "
    result = [False, False, []]

    # node - gateway message
    if interlocutor == "nodes":
        result = update_gw_database_nodes(msg, mode, prefix, interac)
    elif interlocutor == "cloud":
        result = update_gw_database_cloud(msg,prefix)
    else:
        print(prefix + "error: invalid message origin detected")

    return result

def update_gw_database_nodes(msg, mode, prefix="", interac=None):
    """

    Function that updates the gateway database according to:
        1. the message mode
        2. message type
    
    :does:
        1. Starts a switch case, depending on *mode* (listen or request) and *message type*.
     
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param mode: either "listen" or "request"
    :type mode: string
    :param interac: MQTT node interaction (it can be deleted once we have a proper database and we don't need to store the node list on RAM)
    :type interac: mqtt_interaction_meshnet  
     
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *bool* True if database is changed, False if no changes were made
            - [2] - *list* return arguments. Depending on the **message type** these arguments can be more or fewer        
        """
    
    prefix = prefix + "from node message> "
    result = [False, False, []]

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
                            gvar.MSG_TYPE_GW_SEND_NEW_STRAGEGY
                            ]:
            prefix = prefix + " send command> "
            print(prefix + "no action needed yet")
            result = [True, False, []]
        
        elif msg.type in [  gvar.MSG_TYPE_GW_GET_LED_STATUS,
                            gvar.MSG_TYPE_GW_GET_DIMMING_STATUS,
                            gvar.MSG_TYPE_GW_GET_NUMBER_OF_NEIGHBOURS,
                            gvar.MSG_TYPE_GW_GET_RSSI,
                            gvar.MSG_TYPE_GW_GET_NODE_STATUS]:
            prefix = prefix + " received node information> "
            print(prefix + "should update the database with the received information, but no database is available yet :/")
            result = [True, False, []]

        else:
            print(prefix + "error: no action detected for given msg type: " + str(msg.type))

    
    # NODE REQUEST TO GATEWAY
    elif mode == "listen":
        prefix = prefix + " node request to gateway> "
        # discriminate according to message type:
        interac.update_node_list(msg.node_id)   # updates the list of nodes storen in RAM
        print(prefix + "node id list: " + str(interac.node_id_list))

        if msg.type == gvar.MSG_TYPE_NODE_GET_TIME:
            prefix = prefix + " other> "
            print(prefix + "no action needed yet")
            result = [True, False, []]

        elif msg.type in [  gvar.MSG_TYPE_NODE_SEND_ALARM,
                            gvar.MSG_TYPE_NODE_SEND_CURRENT_VOLTAGE,
                            gvar.MSG_TYPE_NODE_SEND_ELECTRIC_PARAMETERS,
                            gvar.MSG_TYPE_NODE_SEND_SOLAR_PANEL_METRICS,
                            gvar.MSG_TYPE_NODE_SEND_NODE_STATUS]:
            prefix = prefix + " received node information> "
            print(prefix + "should update the database with the received information, but no database is available yet :/")
            result = [True, False, []]
            
        else:
            print(prefix + "error: no action detected for given msg type: " + str(msg.type))

    else:
        print(prefix + "error: invalid message mode detected")

    

    return result


def update_gw_database_cloud(msg, prefix=""):
    """
    Function that updates the gateway database according to:
        1. message MQTT supertopic
        2. message type
     
    :does:
        1. Starts a switch case, depending on the *MQTT super-topic*.
        2. Starts another switch case, depending on the *message type*
        
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
    result = [False, False, []]

    # CLOUD TO NODE REQUEST
    if msg.sub_supertopic == gvar.CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC:
        prefix = prefix + " cloud to node> "
        if msg.type == gvar.MSG_TYPE_GW_SEND_NEW_STRAGEGY:
            prefix = prefix + " new strategy> "
            print(prefix + "right now a new strategy should be inserted into the database, but no database is configured yet :(")
            result = [True, False, []]
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
            result = [True, False, []]
        
        else:
            print(prefix + "error: no action detected for given msg type: " + str(msg.type))

    # CLOUD TO GATEWAY REQUEST
    elif msg.sub_supertopic == gvar.CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
        prefix = prefix + " cloud to gateway> "
        # discriminate according to message type:
        if msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_REMOVE_NODES: # CLOUD -> GATEWAY: REMOVE NODES
            prefix = prefix + " remove nodes> "
            print(prefix + "should update the database with the received information, but no database is available yet :/.")
            print(prefix + "warning: we will assume they were successfully removed from it.")
            result = [True, False, [get_crc.compute_crc(msg.payload)]]

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
        if msg.type in [ 
                        gvar.MSG_TYPE_ALIVE_GW_TO_CLOUD,
                        gvar.MSG_TYPE_ADD_NODES_GW_TO_CLOUD,
                        gvar.MSG_TYPE_UNSEEN_NODES_GW_TO_CLOUD,
                        gvar.MSG_TYPE_NODE_STATUS_GW_TO_CLOUD,
                        gvar.MSG_TYPE_ALARM_GW_TO_CLOUD,
                        gvar.MSG_TYPE_ELECTRIC_PARAMETERS_GW_TO_CLOUD
                        ]:
            prefix = prefix + " other> "
            print(prefix + "no action needed yet")
            result = [True, False, []]
        else:
            print(prefix + "error: no action detected for given msg type: " + str(msg.type))

    # to be deleted from production: (simulates cloud behaviour) 

    # GATEWAY REQUEST TO CLOUD (no gateway database update needed)
    elif msg.sub_supertopic == gvar.GATEWAY_REQUEST_TO_CLOUD_MQTT_SUPERTOPIC:
        prefix = prefix + " gateway request to cloud> "
        print(prefix + "no action needed for fake cloud simulation from the gateway")
        result = [True, False, []]

    else:
        print(prefix + "error: invalid message origin detected")

    

    return result