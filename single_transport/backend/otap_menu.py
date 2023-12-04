"""
Perform an OTAP operation to a wirepas mesh network using the gateway backend.

It allows for a series of different otap operations, such as:

- get the list of nodes connected to the sink
- get their scratchpad version
- upload a scratchpad to the sink
- process a scratchpad to the sink
- propagate the new node firmare to all node


"""
import global_vars as gvar
from wirepas_mqtt_library import WirepasOtapHelper
import wirepas_mesh_messaging as wmm
import otap_specific_functions as remotap
import os

OTAP_MODE_PROPAGATE_ONLY = "Propagate only"
OTAP_MODE_IMMEDIATELY = "Propagate and process immediately"
OTAP_MODE_DELAYED = "Set propagate and process with 5 days delay"
OTAP_MODE_UPDATE_DELAY = "Change time delay to 30 minutes"
OTAP_MODE_NO_OTAP = "Set sink(s) to no otap"
OTAP_MODE_UPLOAD_ONLY = "Upload scratchpad to all sinks"
OTAP_MODE_SINK_ONLY = "Process scratchpad on all sink(s)"
OTAP_MODE_SCRATCHPAD_STATUS = "Display sink status and scratchpad status on all nodes"
OTAP_MODE_LIST_SINKS = "List all sink names and their gateway id"
OTAP_MODE_SET_SINK_CONFIG = "Set a new sink configuration"
OTAP_MODE_ACTIVATE_ALL_SINKS = "Activate all sinks that the gateway can see"
OTAP_MODE_RESTART_GATEWAY_SERVICES = "Restart all gateway services"
OTAP_MODE_NODE_VERSION = "Get the stack and app node versions"
OTAP_MODE_GET_NODE_LIST = "Get the list of nodes the gateway can reach"
OTAP_MODE_GET_GATEWAY_LIST = "Get the list of gateways ever connected to the local MQTT broker"


def main(mode="", curr_net_address=None):
    """
    Start OTAP process with the sink(s). Allow user to select a mode.
    
    :does:

    1. Sets up a mode list to select from. The available modes are:
        
        1. "Propagate only"
        2. "Propagate and process immediately"
        3. "Set propagate and process with 5 days delay"
        4. "Change time delay to 30 minutes"
        5. "Set sink(s) to no otap"
        6. "Upload scratchpad to all sinks"
        7. "Process scratchpad on all sink(s)"
        8. "Display sink status and scratchpad status on all nodes"
        9. "List all sink names and their gateway id"
        10. "Set a new sink configuration"
        11. "Activate all sinks that the gateway can see"
        12. "Restart all gateway services"
        13. "Get the stack and app node versions"
        14. "Get the list of nodes the gateway can reach"
        15. "Get the list of gateways ever connected to the local MQTT broker"

    2. Sets up a WNI and an OtapHelper entity with scratchpad data
    3. Get a new sequence number
    4. Set a network id and maybe a scratchpad file depending on the mode selected
    5. Execute the wirepas otap command selected.
    
    :param mode: one of the available otap mode
    :type mode: int
    :param curr_net_address: Current network channel of the sink
    :type curr_net_address: int

    """
    prefix = "<otap menu>"
    print("select an otap operation to perform:")

    MODE_LIST = [
                OTAP_MODE_PROPAGATE_ONLY, 
                OTAP_MODE_IMMEDIATELY, 
                OTAP_MODE_DELAYED, 
                OTAP_MODE_UPDATE_DELAY, 
                OTAP_MODE_NO_OTAP, 
                OTAP_MODE_UPLOAD_ONLY,
                OTAP_MODE_SINK_ONLY,
                OTAP_MODE_SCRATCHPAD_STATUS,
                OTAP_MODE_LIST_SINKS,
                OTAP_MODE_SET_SINK_CONFIG,
                OTAP_MODE_ACTIVATE_ALL_SINKS,
                OTAP_MODE_RESTART_GATEWAY_SERVICES,
                OTAP_MODE_NODE_VERSION,
                OTAP_MODE_GET_NODE_LIST,
                OTAP_MODE_GET_GATEWAY_LIST
                ]
    
    if mode == "":
        mode = gvar.display_and_set_interaction_mode(MODE_LIST)
    else:
        print("{} mode automatically selected".format(prefix))
    
    mode = int(mode)
    mode = MODE_LIST[mode]
    # initialize variables
    scratchpad = ""
    # initialize variables:
    new_net_channel = None
    new_net_address = None
    start_it = None
    
    if mode != OTAP_MODE_LIST_SINKS:
        if curr_net_address == None:
            curr_net_address = int(input("Input a target network address to affect:\n"))
        else:
            print("{} current network address already set!".format(prefix))


    if mode == OTAP_MODE_UPDATE_DELAY:
        pass

    elif mode == OTAP_MODE_NO_OTAP:
        pass
    
    elif mode == OTAP_MODE_UPLOAD_ONLY:
        filist = gvar.get_all_files_in_dir("otap/scratchpads/")
        print("\nSelect a scratchpad:\n")
        scratchpad = gvar.select_elem_from_list(filist, "file")
        

    elif mode == OTAP_MODE_SINK_ONLY:
        pass

    elif mode == OTAP_MODE_PROPAGATE_ONLY:
       pass

    elif mode == OTAP_MODE_IMMEDIATELY:
        pass

    elif mode == OTAP_MODE_DELAYED:
        pass

    elif mode == OTAP_MODE_SCRATCHPAD_STATUS:
        pass
    
    elif mode in [OTAP_MODE_LIST_SINKS, OTAP_MODE_GET_GATEWAY_LIST]:
        pass

    elif mode == OTAP_MODE_SET_SINK_CONFIG:
        
        new_net_channel = input("enter the new network channel:\n")
        new_net_address = input("enter the new network address:\n")
        start_it = input("Do you want to start the sink after configuration? (y/n):\n")
        if start_it in ["y","Y", "yes", "YES"]:
            start_it = True
        else:
            start_it = False

    elif mode == OTAP_MODE_ACTIVATE_ALL_SINKS:
        pass
 
    elif mode == OTAP_MODE_RESTART_GATEWAY_SERVICES:
        pass
    
    elif mode == OTAP_MODE_NODE_VERSION:
        pass

    elif mode == OTAP_MODE_GET_NODE_LIST:
        pass

    else :
        print("error: Unrecognized mode selected!")  
        return

    result = do_otap_action( mode, curr_net_address, new_net_channel , new_net_address , start_it, scratchpad )
    return result

def do_otap_action(mode, curr_net_addr = None, new_net_chan = None, 
                   new_net_addr = None, start_sink = True, scratchpad = None, wni = None):
    """
    Does the otap operation. 
    
    :note: This function can be called by itself or the main function in this script.

    :does: One of the following actions according to what is selected:

        1. Propagate scratchpad from sink to nodes
        2. Process scratchpad to the sink and propagate to nodes
        3. Propagate and process with some delay
        4. Change the delay time
        5. Eras the scratchpad from the sink's memory so it cannot propagate it anymore
        6. Upload scratchpad to the sink
        7. Process scratchpad on all sinks of the gateway
        8. Get the current scratchpad of the sink and every node connected to it
        9. list all sinks within gateway control
        10. Change the configuration of the sink (network channel and addres, start/stop sink, etc)
        11. Start all sinks within gateway control
        12. Restart the gateway services
        13. Get the stack & app software version of a specific node (of its scratchpad) 
        14. "Get the list of nodes the gateway can reach"
        15. "Get the list of gateways ever connected to the local MQTT broker"

    :param mode: Action to perform
    :type mode: string
    :param curr_net_addr: network address to affect. Nodes and sinks in this network will be affected by the otap action performed.
    :type curr_net_addr: int
    :param new_net_chan: New network channel, if applicable
    :type new_net_chan: int
    :param new_net_addr: New network address, if applicable
    :type new_net_addr: int
    :param start_sink: If you want to start the sink after changing its network address and channel, if applicable
    :type start_sink: bool
    :param scratchpad: Scratchpad file path, to upload to the sink, if applicable.
    :type scratchpad: string
          
    :returns: Depending on the mode selected, it might return something or not
        **node_list** *(list of int)*: In the case of mode == list int
        
    """
    prefix = "<otap_menu>"

    if wni == None:
        print("{} setting the WNI...".format(prefix))
        wni = gvar.create_wni()
        sinks = gvar.get_sink_and_gw(wni)
    else:
        print("{} wni already given by calling function".format(prefix))
        
    if mode != OTAP_MODE_LIST_SINKS:
        global otapHelper
        otapHelper = WirepasOtapHelper(wni,
                                   int(curr_net_addr))

    if mode not in [OTAP_MODE_SCRATCHPAD_STATUS, OTAP_MODE_LIST_SINKS, OTAP_MODE_SET_SINK_CONFIG] :
        # find good sequence number
        seq = find_good_seq_number(otapHelper)
    

    if mode == OTAP_MODE_UPDATE_DELAY:
        delay = wmm.ProcessingDelay.DELAY_THIRTY_MINUTES
        print("Set new delay to %s" % delay)
        if not otapHelper.set_propagate_and_process_scratchpad_to_all_sinks(delay=delay):
            print("Cannot update delay")
        else:
            print("command executed successfully")

    elif mode == OTAP_MODE_NO_OTAP:
        print("Setting target to no otap")
        if not otapHelper.set_no_otap_to_all_sinks():
            print("Cannot set no otap on all sinks")
        else:
            print("No-otap set for all sinks")
    
    elif mode == OTAP_MODE_UPLOAD_ONLY:
    
        print("Uploading scratchpad to all sink(s). Please wait...")
        if not otapHelper.load_scratchpad_to_all_sinks(scratchpad, seq):
            print("Cannot load scratchpad to all sinks")
        else :
            print("Scratchpad uploaded to all sink(s)!")

    elif mode == OTAP_MODE_SINK_ONLY:
        print("Processing scratchpad on all sinks")
        if not otapHelper.process_scratchpad_on_all_sinks():
            print("Cannot process scratchpad on all sinks")
        else:
            print("command executed successfully")

    elif mode == OTAP_MODE_PROPAGATE_ONLY:
        print("Set propagate only")
        if not otapHelper.set_propagate_scratchpad_to_all_sinks():
            print("Cannot set propagate")
        else:
            print("command executed successfully")

    elif mode == OTAP_MODE_IMMEDIATELY:
        print("Set propagate and process. Now the sink will propagate the new firmware OTAP and will reboot. Please give a few good minutes before attempting to reach a node.")
        if not otapHelper.set_propagate_and_process_scratchpad_to_all_sinks():
            print("Cannot set propagate and process only for delay %s" % delay)
        else:
            print("command executed successfully")

    elif mode == OTAP_MODE_DELAYED:
        print("Set propagate and process with 5 days delay")
        if not otapHelper.set_propagate_and_process_scratchpad_to_all_sinks(delay=wmm.ProcessingDelay.DELAY_FIVE_DAYS):
            print("Cannot set propagate and process only for 5 days")
        else:
            print("command executed successfully")

    elif mode == OTAP_MODE_SCRATCHPAD_STATUS:
        print("get the remote scratchpad status and sequence number for each node connected to the sink")
        remotap.get_scratchpads(wni, otapHelper)
    
    elif mode == OTAP_MODE_LIST_SINKS:
        print("list all sinks with their gateway id")
        remotap.list_sinks(wni)

    elif mode == OTAP_MODE_SET_SINK_CONFIG:
        prefix = "<trying otap mode: set sink config> "
        print(prefix + "Set the network channel, network address and either if you want to restart the sink or not")
        # try:
        remotap.configure_sink(curr_net_addr, new_net_chan, 
                   new_net_addr, start_sink, wni)
        # except:
        #     print(prefix + "some of the arguments might be wrong, maybe you didn't enter a number for the network parameters?" )
        
    elif mode == OTAP_MODE_ACTIVATE_ALL_SINKS:
        prefix = "<trying otap mode: activate all sinks> "
        print("Start all the sinks that the gateway can see")

        # try:
        remotap.activate_all_sinks(wni)
        # except:
        #     print(prefix + "some of the arguments might be wrong, maybe you didn't enter a number for the network parameters?" )
    
    elif mode == OTAP_MODE_RESTART_GATEWAY_SERVICES:
        prefix = "<trying otap mode: restart all gateway services> "
        print("Restart all the gateway services")

        # try:
        os.system("echo admin | sudo -S systemctl restart gateway_services.service")
        # except:
        #     print(prefix + "some of the arguments might be wrong, maybe you didn't enter a number for the network parameters?" )
        
    elif mode == OTAP_MODE_NODE_VERSION:
        prefix = "<trying otap mode: get node version> "
        print("{} computing node version...")
        node_id = input("enter node id:\n")
        node_id = int(node_id)
        # try:
        version = remotap.get_node_version(otapHelper, node_id)
        print("{} stack version: {}, app version: {}. For node {}".format(prefix, version[0:4], version[4:], node_id))
        # except:
        # print(prefix + "some of the arguments might be wrong, maybe you didn't enter a number for the network parameters?" )
    
    elif mode == OTAP_MODE_GET_NODE_LIST:
        prefix = "<otap mode: get node list> "
        print("{} computing node list...")
        try:
            node_list = remotap.get_node_list(otapHelper)
            print("{} Noice! Got node list with otap!\nnode list: {}".format(prefix, node_list ))
            return node_list
        except:
            print("{} warning: failed to get node list from otap..".format(prefix))
            return None

    elif mode == OTAP_MODE_GET_GATEWAY_LIST:
        prefix = "<otap mode: get gateway id list>"
        print("{} computing gateway id list".format(prefix))
        try:
            gw_ids = remotap.list_gateways(wni)
            print("{} Noice! Got gateway list with otap!\ngw id list: {}".format(prefix, gw_ids ))
            return gw_ids
        except Exception as error:
            print("{} got the following error: {}".format(prefix, error))
            return None

    else :
        print("error: Unrecognized mode selected!")  
        return "error"

    return None
    

def find_good_seq_number(otapHelper):
    """
    Gets a new sequence number to add to the scratchpad that will be sent to the nodes. 
    
    :does:
        1. It gets the current scratchpad's sequence number
        2. It computes a new valid one.
    """
    prefix = "<find good seq number>"
    # Optional: find a "good" sequence number
    current_target_seq_set = otapHelper.get_target_scratchpad_seq_list()

    print("Sequences already in use: ", current_target_seq_set)
    # Take a sequence from 1-254 that is not in the current set
    # seq = choice([i for i in range(1,254) if i not in current_target_seq_set])
    print("{} current target: {}".format(prefix, current_target_seq_set))
    if current_target_seq_set != None and len(current_target_seq_set) > 0:
        seq  = max(current_target_seq_set) + 1
    else : 
        seq = 1
    if seq > 254:
        seq = 1
    print("Sequence chosen: ", seq)
    
    return seq


if __name__ == "__main__":
    main()
