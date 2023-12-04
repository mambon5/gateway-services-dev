"""
Script responsible for updating the node software using OTAP.

Main idea of propagate and process a scratchpad is the following one:

1. Upload a scratchpad to the sink(s). The scratchpad is the byte-format firmware that has to be flashed into the nodes.
2. *Process* the scratchpad to the sink and *propagate* it to all nodes connected directly (or indirectly via jumps or hops) to the sink
3. Wait for the sink to restart (around 4min total) and the node to adopt the new scratchpad.
4. After some minutes, all nodes related to the sink(s) will reboot and they will be running with the new firmware.
"""

import time
import os
import otap_menu as omenu
import global_vars as gvar

def main(wni=None):
    """
    This function uploads the selected scratchpad and propagates it to all the visible nodes.

    :does:
        1. It gets the scratchpad filename that is stored in the file "otap/stratchpad_to_use.txt".
        2. Then it sets the sink to *no otap* mode to erase any possibly conflicting scratchpad already loaded in the sink memory
        3. uploads the scratchpad to the sink
        4. Waits 6 seconds
        5. It processes the scratchpad in the sink and propagates it to all connected nodes, forever or until a command to stop the propagation is received
        6. it waits 2 minutes for the process and propagation to finish
        7. Then it restarts all the gateway services by invoking the linux systemd service *restart gateway_services.service*

    :param wni: Wirepas network interface class, containign the MQTT broker connection
    :type wni: WirepasNetworkInterface

    """

    prefix = "<performing otap>"
    file_settings = "otap/stratchpad_to_use.txt"
    f = open(file_settings, "r")
    line = f.readline()
    scratchpad = int(line.split("=")[1])
    f.close()

    otappath = "otap/scratchpads/"
    # scratchpad = "pruebas/otap-2/otap-2_wpc_stack.otap"
    scratchpad = otappath + scratchpad
    print("{} sctatchpad file chosen: {}".format(prefix, scratchpad))
    net_address = gvar.NETWORK_DEFAULT_CHANNEL

    if wni == None:
        print("{} setting the WNI...".format(prefix))
        wni = gvar.create_wni()
    else:
        print("{} wni already given by calling function".format(prefix))

    # set sink to no-otap
    omenu.do_otap_action(mode=omenu.OTAP_MODE_NO_OTAP, curr_net_addr = net_address, wni=wni)

    # upload scratchpad
    omenu.do_otap_action(mode=omenu.OTAP_MODE_UPLOAD_ONLY, curr_net_addr = net_address, scratchpad=scratchpad, wni=wni)

    time.sleep(6)

    # propagate and process
    omenu.do_otap_action(mode=omenu.OTAP_MODE_IMMEDIATELY, curr_net_addr = net_address, wni=wni)

    # wait
    time.sleep(120)

    # restart sink and gateway services.
    os.system("echo admin | sudo -S systemctl restart gateway_services.service")

    #time.sleep(120)
    # activate the sink
    #omenu.do_otap_action(mode=omenu.OTAP_MODE_ACTIVATE_ALL_SINKS, curr_net_addr = net_address)

    # we can write here a line saying: gw updated


