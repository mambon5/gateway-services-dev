"""
Prepares the response after a message is received and processed.
"""

import global_vars as gvar
import create_message_functions as creamsgf

def prepare_response(msg, parsed, update_db, read_db, mode, interlocutor, pubtopic, tunnel=None, software_update=None):
    """
    Function to prepare the response to the interlocutor. Based on the 

        1. original cloud/node message
        2. response from the node (if the original messages was from cloud > node)
        3. interlocutor (cloud or nodes)
        4. interaction mode
        5. the results of:
            - software update
            - database update
            - read database
            - initial parsing


    :does: 
        1. It checks if there has been any error while processing the:
            - parsing
            - tunneling (cloud to node or viceversa)
            - reading of the database
            - updating of the database
            - updating of the software
        2. If there has been a problem in any of the mentioned operations above, the message type is set to *Error*  and the 
           proper error type is stored in the message arguments *msg.args*.
        3. Depending on the interlocutor (cloud/nodes) one of the following functions is called to finish the preparation
           of the response:
                - :py:meth:`~prepare_response.prepare_response_nodes`
                - :py:meth:`~prepare_response.prepare_response_cloud`
        4. The prepared response is returned, which contains a bool (preparation of response was success/failure) and the 
           response (as the message payload, in bytes).
    

    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param parsed: True if parsing was successful, False otherwise
    :type parsed: bool
    :param db_update: result from the database update function call
    :type db_update: [bool, list]
    :param read_db: result from the database read function call
    :type read_db: [bool, list]
    :param mode: whether node is "listen" or "request" mode
    :type mode: string
    :param interlocutor: whether node is "cloud" or "nodes" mode
    :type interlocutor: string
    :param pubtopic: MQTT topic where the message is gonig to be published. It is None for node to gateway messages.
    :type pubtopic: string
    :param tunnel: result from the tunnel to node call, it returns True if call was successful, and the message received from the node
    :type tunnel: [bool, node_msg]
    :param soft_upd: result from the software update function call 
    :type soft_upd: [bool, bool, list]

    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *bytes* Message payload to respond with

    """
    prefix = "<prepare response> "
    result = [False, []]
    pub_supertopic = gvar.get_supertopic(pubtopic)

    # CHECKING POSSIBLE PROCESSING ERRORS:
    # parsing error:
    if not parsed:
        print(prefix + "error: message parsing failed")
        # the error arguments are already generated for this case automatically


    # tunnel error:
    elif tunnel != None and not tunnel[0]:
        # answer with error response
        msg.type = gvar.MSG_TYPE_ERROR
        if interlocutor == "cloud":
            print(prefix + "error: tunneling to nodes failed.")
            msg.args = [gvar.ERROR_TYPE_WHEN_TUNNELING_TO_NODE]
        elif interlocutor == "nodes":
            print(prefix + "error: tunneling to cloud failed.")
            msg.args = [gvar.ERROR_TYPE_WHEN_TUNNELING_TO_CLOUD]
        tunnel[1] = msg # we set the node message response arguments = the request messsage argument (which is the error code)
    
    # error while software update
    elif software_update != None and not software_update[0]:
        print(prefix + "error: update gateway software failed.")
        
        # answer with error response
        msg.type = gvar.MSG_TYPE_ERROR
        msg.args = [gvar.ERROR_TYPE_WHEN_UPDATING_GW_SOFTWARE]

    elif software_update != None and software_update[1]:
        print(prefix + "software updated!")

    # error while update database:
    elif not update_db[0]:
        print(prefix + "error: update gateway database failed.")
        # answer with error response
        msg.type = gvar.MSG_TYPE_ERROR
        msg.args = [gvar.ERROR_TYPE_WHEN_UPDATING_DATABASE]

    # error while reading database:
    elif not read_db[0]:
        print(prefix + "error: read gateway database failed. ")
        # answer with error response
        msg.type = gvar.MSG_TYPE_ERROR
        msg.args = [gvar.ERROR_TYPE_WHEN_READING_DATABASE]

    if interlocutor == "nodes":
        result = prepare_response_nodes(msg, tunnel[1], update_db[2], read_db[1], mode, prefix)

    elif interlocutor == "cloud":
        result = prepare_response_cloud(msg, tunnel[1], software_update[2], update_db[2], read_db[1], pub_supertopic, prefix)
    else:
        print(prefix + "not a valid interlocutor found")    

    return result


def prepare_response_cloud(msg, node_msg, soft_up_list, db_up_list, read_db_list, pub_supertopic, prefix="" ):
    """
    Creates the response message for a cloud-gateway interaction.

    :does:

        1. It sets the right message id and type
        2. It sets the right arguments 
        3. Calls the :py:meth:`~create_message_functions.message_to_bytes`  function to create the message
    
    :param msg: the message received from the cloud
    :type msg: RxMsg
    :param node_msg: the message received from the node, via tunneling
    :type node_msg: RxMsg
    :param soft_up_list: resulting list from the software update function call 
    :type soft_up_list: list
    :param db_up_list: resulting list from the database update function call
    :type db_up_list: list
    :param read_db_list: resulting list from the database update function call
    :type read_db_list: list
    :param pubtopic: MQTT topic where the message is going to be published. It is None for node to gateway messages.
    :type pubtopic: string
    :param prefix: text to prepend on each printed line on debug or console
    :type prefix: string

    :returns:
        :payload: *(bytes)* -- the message payload that we wanted to create as a response

    """

    prefix = prefix + "cloud> " 
    
    payload = b''   # empty message in bytes

    # payload = creamsgf.message_to_bytes(msg.id, msg.type, msg.args, pubtopic, prefix, msg)

    result = [False, None]

    # PARSING ERROR MSG
    if msg.type == gvar.MSG_TYPE_ERROR:
        payload = creamsgf.message_to_bytes(msg.id, msg.type, msg.args, pub_supertopic, prefix)
        result = [True, payload]

    # GATEWAY RESPONSE TO CLOUD REQUEST TO NODE
    elif pub_supertopic == gvar.GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC:
        prefix = prefix + " gw response to cloud to node> "

        if msg.type in gvar.MSG_CLOUD_TO_NODE_REQUESTS_LIST:   
            
            if msg.type == gvar.MSG_TYPE_CLOUD_TO_NODE_GET_VERSION: # for cloud requests of node version
                args = node_msg # this gives the list of the 8 node version numbers
                msg_type = msg.type
            else:   # rest of cloud requests to node
                args = node_msg.args
                msg_type = node_msg.type
            
            payload = creamsgf.message_to_bytes(msg.id, msg_type, args, pub_supertopic, prefix)
            result = [True, payload]
            
        else:
            print(prefix + "error: wrong msg type: " + str(msg.type))

    # GATEWAY RESPONSE TO CLOUD REQUEST TO GATEWAY
    elif pub_supertopic == gvar.GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
        prefix = prefix + " cloud to gateway> "
        # discriminate according to message type:
        if msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_REMOVE_NODES: # CLOUD -> GATEWAY: REMOVE NODES
            prefix = prefix + " remove nodes> "
            print(prefix + "right now nodes should be removed from the database, but no database is configured yet :(")
            
            args = db_up_list # db_up_list should be = [crc]
            print(prefix + "args: " + str(args) + ", msg.type: " + str(msg.type))
            payload = creamsgf.message_to_bytes(msg.id, msg.type, args, pub_supertopic, prefix, msg)
            result = [True, payload]
        elif msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_NODE_LIST:
            prefix = prefix + " other> "
            print(prefix + "nodes should have been read from the local database, but there is no one yet :') (ploro)")
            args = [msg.args[0], read_db_list[0]]
            payload = creamsgf.message_to_bytes(msg.id, msg.type, args, pub_supertopic, prefix, msg)
            result = [True, payload]
        elif msg.type in [gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_GATEWAY,gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_NODES]:
            prefix = prefix + " other> "
            print(prefix + "no action needed yet")
            payload = creamsgf.message_to_bytes(msg.id, msg.type, msg.args, pub_supertopic, prefix, msg)
            result = [True, payload]
        elif msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_GET_GATEWAY_VERSION:
            prefix = prefix + " gw version> "
            print(prefix + "gw version should've been read")
            payload = creamsgf.message_to_bytes(msg.id, msg.type, read_db_list, pub_supertopic, prefix, msg)
            # read_db_list contains a list with the 4 elements codifying the version of the gateway.
            result = [True, payload]
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

    # GATEWAY REQUEST TO CLOUD (no gateway database update needed)
    elif pub_supertopic == gvar.CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_SUPERTOPIC:
        prefix = prefix + " cloud response to gw request> "
        print(prefix + "fake cloud listening simulation: sending the msg arguments to the message to bytes function")
        payload = creamsgf.message_to_bytes(msg.id, msg.type, msg.args, pub_supertopic, prefix, msg)
        result = [True, payload]

    else:
        print(prefix + "error: invalid message origin detected")

    return result

def prepare_response_nodes(msg, cloud_interac, db_up_list, read_db_list, mode, prefix):
    """
    Creates the response message for a nodes-gateway interaction.
    
    :does:
        1. It checks the message type and calls the :py:meth:`~create_message_functions.message_to_bytes`  function to create the message

    :param msg: the message received
    :type msg: RxMsg
    :param prefix: text to prepend on each printed line on debug or console
    :type prefix: string
    :param db_up_list: resulting list from the database update function call
    :type db_up_list: list
    :param read_db_list: resulting list from the database update function call
    :type read_db_list: list
    
    :returns:
        :payload: *(bytes)* -- the message payload that we wanted to create as a response

    """
    prefix = prefix + "nodes> "
    payload = b''
    result = [False, None]

    # PREPARING RESPONSE FOR ANY KIND OF VALID MESSAGE
    if msg.type == gvar.MSG_TYPE_ERROR or msg.type in gvar.MSG_NODE_REQUESTS_LIST:
        pub_supertopic = None
        payload = creamsgf.message_to_bytes(msg.id, msg.type, msg.args, pub_supertopic, prefix, msg)
        result = [True, payload]
    else:
        print(prefix + "message type from nodes -> gateway not recognized")
        return
    
    return result

