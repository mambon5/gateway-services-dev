"""
Set of specific functions that use the wirepas OTAP. 

The functions listed here allow the user to:
    1. Get the scratchpads of every node connected to the gateway's sink
    2. Upload an scratchpad to the sink
    3. Order the sink to propagate this scratchpad to all the nodes
    4. Delete any scratchpad that is stored in the sink
    5. Set a new sink configuration (change network channel, address, start/stop the sink)

Combining the 5 options above, and extracting different information in each of them, we delevopped a set of 14 different functions (so far)
that extract/send information and commands from the sink and the nodes without having to set up any custom program in the node that
reads and processess our custom requests. It is all handled by the built-in wirepas stack programs of the nodes and the sink
"""

import wirepas_mesh_messaging as wmm
import subprocess
from datetime import datetime
import time



# def type_to_str(type_int):
#     map_to_str = ("Blank", "Present", "Process")
#     try:
#         return map_to_str[type_int]
#     except IndexError:
#         return "Unknown {}".format(type_int)


# def status_to_str(status):
#     if status == 255:
#         return "New"
#     if status == 0:
#         return "Success"

#     return "Error {}".format(status)


def print_node_list(nodes):
    """
    Prints the list of current node ids.

    :param nodes: list of current node ids
    :type nodes: list
    """
    print("\nList of nodes:")

    id = 0
    for node_id in list(nodes):
        # Convert utc time to date
        node = nodes[node_id]
        timestamp = datetime.utcfromtimestamp(node["ts"] / 1000.0)
        print(" {:5d} | {:10d} | {} | {}".format(
            id,
            node_id,
            timestamp,
            node
        ));
        id += 1

    print()

def get_scratchpads(wni, otapHelper):
    """
    This function gets the scratchapd of every node connected to the sink. 
    
    :does:
        1. It uses the WNI to get a list of all the connected sinks to the gateway backend
        2. It sends a remote "scratchpad status" to all connected nodes, and awaits its response
        3. After 0 seconds, it gets or captures the response from the nodes to the sink

    :param wni: Wirepas network interface class, containign the MQTT broker connection
    :type wni: WirepasNetworkInterface
    :param otapHelper: Class to ease Otap operation containing the network address.
    :type otapHelper: WirepasOtapHelper
    """

    sinks = wni.get_sinks()
    print("displaying sinks:")
    print(sinks)
    print("displaying node scratchpads:")
    otapHelper.send_remote_scratchpad_status()
    #time.sleep(0.2)
    print_node_list(otapHelper.get_current_nodes_status())


def list_sinks(wni):
    """
    List all sinks and their gateway id. 
    
    :does:
        1. It uses the WNI to get a list of all the connected sinks to local MQTT broker
        2. It lists them one by one

    :param wni: Wirepas network interface class, containing the MQTT broker connection
    :type wni: WirepasNetworkInterface
    """
    line = ""
    for gw, sink, config in wni.get_sinks():
        line += "[gw: %s, sink: %s, net address: %s, net channel: %s, sink running: %s] " % (gw, sink, 
                            config["network_address"], config["network_channel"], config["started"])

    print(datetime.now())
    print(line)

    # def on_config_changed():
    #     line = ""
    #     for gw, sink, config in wni.get_sinks():
    #         line += "[gw: %s, sink: %s, net address: %s, net channel: %s, sink running: %s] " % (gw, sink, 
    #                             config["network_address"], config["network_channel"], config["started"])

    #     print(datetime.now())
    #     print(line)

    # wni.set_config_changed_cb(on_config_changed)

def list_gateways(wni):
    """
    List all gateways and their id. 
    
    :does:
        1. It uses the WNI to get a list of all the gateways ever connected to the local MQTT broker
        2. It lists them one by one

    :param wni: Wirepas network interface class, containing the MQTT broker connection
    :type wni: WirepasNetworkInterface

    :returns:
        :gws: *(list)* -- list of gateway ids ever connected to the MQTT broker
        
    """
    prefix= "<list gateways>"
    llista = wni.get_gateways(only_online=False)
    # print("{} gateway list: {}".format(prefix, llista))
    return(llista)

def configure_sink(current_net_ad, net_channel=5, net_address=5, start_it=True, wni=None):
    """
    Sets up a new configuration for the sink. 

    :does:
        1. First of all, it gets all the sinks connected to the gateway using the wirepas function *get_sinks()*.
        2. Then it sets the sink configuration according to the input arguments, using the wirepas *set_sink_config()* function.
        3. It restarts the sink by calling the shell script *start_sinks.sh*

    :param current_net_ad: Current network channel of the sink
    :type current_net_ad: int
    :param net_channel: New network channel to set the sink to
    :type net_channel: int
    :param net_address: New network address to set the sink to
    :type net_address: int
    :param start_it: Whether to start the sink configuration or not, after changing the rest of the parameters
    :type start_it: bool
    :param wni: Wirepas network interface class, containign the MQTT broker connection
    :type wni: WirepasNetworkInterface
    """
    prefix = "<sink config>"
    print("{} Configuring all sinks of the gateway to new network address: {}, new channel: {} and start it: {}".format(prefix, 
                                                                                                                            net_channel, net_address, start_it))                                                                                         
    # try:
    for gw, sink, config in wni.get_sinks():
    #for gw, sink, config in wni.get_sinks(network_address=int(current_net_ad)):
        print("Set new config to %s:%s" % (gw, sink))
        try:
            res = wni.set_sink_config(gw, sink, {"network_channel": int(net_channel), "network_address": int(net_address),
                                                "started":start_it})
            print("res: ")
            print(res)
            if res != wmm.GatewayResultCode.GW_RES_OK:
                print("{} Cannot set new config to %s:%s res=%s" % (prefix, gw, sink, res))
            else:
                print("{} New configuration set for sink {} from gateway {} to network address: {} and network channel: {}".format(
                    prefix, sink, gw, net_address, net_channel))
                if start_it:
                    print("{} Sink started".format(prefix))
                else:
                    print("{} Sink not started".format(prefix))
        except TimeoutError:
            print("{} Cannot set new config to %s:%s" % (prefix, gw, sink))
    print("{} Ended iterating through all sinks of the gateway".format(prefix))

    # restart sink
    try:
        subprocess.call(['sh', './start_sinks.sh'])
    except:
        print("error: Shell script 'start_sinks.sh' couldn't start.")

    # except:
    #     print("error: while setting the new sink configuration")


def activate_all_sinks(wni):
    """
    Activate all sinks in gateway range. 

    :does:
        1. using the WNI command "get_sink()" the function collects all the information regarding the sink: *gateway id, sink id, network address,
            network channel, is sink active?*
        2. with this information it calls the *configure_sink* function with argument *start_it* set to *True* which activates the sink.

    :param wni: Wirepas network interface class, containign the MQTT broker connection
    :type wni: WirepasNetworkInterface
    """
    prefix = "<activate all sinks> "
    print(prefix + " activating ... ")


    line = ""
    for gw, sink, config in wni.get_sinks():
        line += "[gw: %s, sink: %s, net address: %s, net channel: %s, sink running: %s] " % (gw, sink, 
                            config["network_address"], config["network_channel"], config["started"])
        print(prefix + "starting: " + line)
        try:
            configure_sink(config["network_address"], config["network_channel"], config["network_address"], start_it=True, wni=wni)
            print(prefix + "sink started successfully")
        except:
            print(prefix + "error: failed to start the sink")


def get_node_version(otapHelper, node_id):
    """
    Gets the stack and app version of the node. 

    :does:
        1. A wirepas-specific python function is called, "send_remote_scratchpad_status" in order to send a scratchpad information 
        request to a specific node.
        2. After 0 seconds, another python function is executed to extract that information from the sink.
        3. From the stratchpad status of the node, the stack and app version are extracted and returned.

    :param node_id: address of the node from which we want the software version
    :type node_id: int
    :param otapHelper: Class to ease Otap operation containing the network address.
    :type otapHelper: WirepasOtapHelper

    :return: 
        :result: *(list)* with:
        1. :success: *bool* - whether the node version could be retrieved or not using otap.
        2. :node_software_version: *(list[int])* consists of a list of 8 int ranging from 0-254 which codify:
                1. *stack_version* major.minor.revision.build. These are the first 4 ints of the list.
                2. *app_version* major.minor.revision.build. These are the last 4 ints of the list.
    """
    prefix = "<get node version> "
    print(prefix + " getting it ... ")
    result = [False, []]
    
    node_id = int(node_id)
    print("displaying node version for node {}:".format(node_id))
    otapHelper.send_remote_scratchpad_status(node_id)
    
    time.sleep(0.2)

    try:
        node_status = otapHelper.get_current_nodes_status()[node_id]
        stack_version = node_status["stack_version"]
        app_version = node_status["app_version"]
        # print_node_version(otapHelper.get_current_nodes_status()[node_id])
        result = [True, stack_version + app_version]
    except:
        print("{} error: failed to load software version for node {}. maybe the node is not reachable by the sink?".
              format(prefix, node_id))
    return result

    


def get_node_list(otapHelper):
    """
    Gets the list of nodes connected to the gateway
    the function does 2 things:
        1. It sends a remote "scratchpad status" to all connected nodes, and awaits its response
        2. After 2 seconds, it sends a command that gets or captures the response from the nodes to the sink
    
    :param otapHelper: Class to ease Otap operation containing the network address.
    :type otapHelper: WirepasOtapHelper

    :return: 
        :node list: *(list[int])* consists of a list of nodes ids connected to the sink.
    """
    prefix = "<get node list> "
    print(prefix + " getting it ... ")
    otapHelper.send_remote_scratchpad_status()
    time.sleep(3)
    node_list = otapHelper.get_current_nodes_status()
    node_list = list(node_list.keys()) # getting just the node ids.
    return node_list