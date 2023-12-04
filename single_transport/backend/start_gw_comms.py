"""
Gateway communications main script. This is the first python script that is run when starting the gateway's communications.
"""

import backend_script_node_comms as comnodes
import backend_script_cloud_comms as comcloud
import time
import global_vars as gvar
from threading import Thread
import otap_specific_functions as ospef

def main():
    """
    Main function for running the gateway communications. 
    
    :does: It consists of the following steps:
        1. the WNI is generated
        2. The gateway gets the "sink" and "gateway id" from the sink
        3. The gateway gets the nodes connected to the sink using the sink WNI
        4. Starts the cloud communications using the WNI, sink and gw_id.
        5. Waits 4 seconds, in order to allow the gateway to use the WNI to stablish the necessary cloud/node connections 
        6. Starts the node communications using the WNI and the node list.
    """
    # activate the sink:
    # omenu.do_otap_action(mode=omenu.OTAP_MODE_ACTIVATE_ALL_SINKS, curr_net_addr = gvar.NETWORK_DEFAULT_CHANNEL)
    
    # start listening to the nodes:
    prefix = "<start listen nodes>"

    # get gateway id & node list:
    wni = None
    gw_id = None
    try: 
        # maybe check wirepas docu on this > https://github.com/wirepas/wirepas-mqtt-library/blob/main/README.rst
        wni = gvar.create_wni()
        print("{} wni created OK".format(prefix))
        gws = list(wni.get_gateways(only_online=True)) # I would say this function doesn't work
        print("{} gws created OK. List of gws: {}".format(prefix, gws))
        n = len(gws)
        gw_id = gws[n-1]

        wni.clear_gateway_status("618671184831")
        wni.clear_gateway_status("2485770510562")
        wni.clear_gateway_status("2485725601092")

        print("{} gw showed OK {}".format(prefix, gws[0]))
        print("{} Gateway id: {}".format(prefix, gw_id))
        print("{} rest of gw's ids: {}".format(prefix, gws))
        [sink, gw_id] = gvar.get_sink_and_gw(wni)
        otapHelper = gvar.create_otaphelper(wni)
        node_list = ospef.get_node_list(otapHelper)
        print("{} wni created with gw_id: {} and sink: {}. With node list: {}".format(prefix, gw_id, sink, node_list))
    except Exception as err:
        print("{} error: failed to create wni and {}".format(prefix, err))

    print("starting cloud comms ------------------------------------------------------------------")
    thread = Thread(target=comcloud.run_cloud_comunications, args=(1, wni, gw_id, sink))
    thread.start()
    time.sleep(1) # wait 1000ms in order to allow the gateway to start its gateway <> cloud functionality
    print("finished start of cloud comms ---------------------------------------------------------")

    comnodes.run_node_comunications(2, wni, node_list = node_list)   

if __name__ == "__main__":
    main()