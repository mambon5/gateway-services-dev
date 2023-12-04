"""
File that updates the gateway software if necessary
"""

import global_vars as gvar
import subprocess
import otap_update_all_nodes as notap

def update_gw_software(msg, mode=None, interlocutor=None, scratchpad=None):
    """
    Function that updates the gateway software according to:
        1. the device
     
    :does:
        1. Starts a switch case, depending on the *MQTT super-topic*.
        2. Starts another switch case, depending on the *message type*
        3. Depending on whether the message type is *MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_GATEWAY* or *MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_NODES* it calls:
            - :py:meth:`~update_gw_software.update_gw_software_only` if we wish to update the gw software only
            - :py:meth:`~update_gw_software.update_node_software_otap` if we wish to update the nodes

    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param mode: either "listen" or "request"
    :type mode: string  
    :param interlocutor: whether node is "cloud" or "nodes" mode
    :type interlocutor: string
    :param scratchpad: address of the scratchpad file to send to nodes via OTAP
    :type scratchpad: string
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *bool* True if software is updated, False if no changes were made
            - [2] - *list* return arguments. Depending on the **message type** these arguments can be more or fewer
        """

    prefix = "<update software> "
    result = [False, False, []]

    # node - gateway message
    if interlocutor == "cloud":
        
        # CLOUD TO NODE REQUEST
        if msg.sub_supertopic == gvar.CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC:
            prefix = prefix + " cloud to node> "
            print(prefix + "no action needed")
            result = [True, False,[]]

        # CLOUD TO GATEWAY REQUEST
        elif msg.sub_supertopic == gvar.CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
            prefix = prefix + " cloud to gateway request> "
            # discriminate according to message type:
                                
            if msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_GATEWAY:
                result = update_gw_software_only(msg,prefix)
            elif msg.type == gvar.MSG_TYPE_CLOUD_TO_GATEWAY_UPDATE_NODES:
                result = update_node_software_otap(msg, scratchpad, mode, prefix)

            elif msg.type in gvar.MSG_CLOUD_TO_GATEWAY_REQUESTS_LIST:
                prefix = prefix + " other> "
                print(prefix + "no action needed yet")
                result = [True, False, []]
            else:
                print(prefix + "error: no action detected for given msg type: " + str(msg.type))
        
        # CLOUD RESPONSE TO GATEWAY REQUEST
        elif msg.sub_supertopic == gvar.CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_SUPERTOPIC:
            prefix = prefix + " cloud response to gateway request> "
            print(prefix + "no action needed")
            result = [True, False, []]

        # to be deleted from production: (simulates cloud behaviour)

        # GATEWAY REQUEST TO CLOUD (no gateway database update needed)
        elif msg.sub_supertopic == gvar.GATEWAY_REQUEST_TO_CLOUD_MQTT_SUPERTOPIC:
            prefix = prefix + " gateway request to cloud> "
            print(prefix + "no action needed for fake cloud simulation from the gateway")
            result = [True, False, []]

        else:
            print(prefix + "error: invalid message origin detected")
    
    else:
        print(prefix + "warning: only messages from cloud will update any kind of software.")

    if result[1]:
        print(prefix + "software updated!")

    return result

def update_node_software_otap(msg, scratchpad, mode=None, prefix = ""):
    """
    
    Function that sends an OTAP request to the nodes.

    :does:
        1. Calls the :py:meth:`~otap_update_all_nodes.main` function to perform the OTAP operation to all sinks and nodes.
        2. If no error is encountered, it returns a bool as *True*


    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param scratchpad: address of the scratchpad file to send to nodes via OTAP
    :type scratchpad: string
    :param mode: either "listen" or "request"
    :type mode: string
    :param prefix: prefix to every print of python
    :type prefix: string  
     
    
    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *bool* True if node OTAP is sent, False otherwise
            - [2] - *list* return arguments. Depending on the **message type** these arguments can be more or fewer        
        """
    
    prefix = prefix + "send OTAP to nodes> "
    result = [False, False, []]

    # do otap
    print(prefix + "starting OTAP...")
    try:
        # now the otap process will take place
        notap.main()
        print("{}OTAP finished successfully.".format(prefix))
        result = [True, True, []]
    except:
        print("{}OTAP process failed at some point.".format(prefix))

    return result
    


def update_gw_software_only(msg, prefix=""):
    """
    Function that updates the gateway software from Github and restarts the gateway services.

    :does:
        1. Runs the sh file *run_gateway_update_service.sh* which downloads the Github code and restarts the gateway services.
        2. Returns a bool as *True* if it succeeds, and *False* otherwise.
         
    :param msg: Message received class with all the arguments
    :type msg: RxMsg
    :param prefix: prefix to append to every message print
    :type prefix: string

    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *bool* True if software is updated, False if no changes were made
            - [2] - *list* return arguments. Depending on the **message type** these arguments can be more or fewer
        
        
        """
    
    prefix = prefix + "from cloud message> "
    result = [False, False, []]

    # update gateway software
    print(prefix + "starting gateway code update...")
   
    try:
        # now a local linux service that must be previously installed, will be executed
        # and will download the gateway code from github and restart the sink and gateway services.
        subprocess.run(["./run_gateway_update_service.sh"], shell=True, capture_output=True, text=True)
        print("{}gateway code updating...".format(prefix))
        result = [True, True, []]
    except:
        print("{}Gateway software update failed at some point.".format(prefix))

        # we can write here a line saying: gw updated once the gw is finished with otap

    return result
    