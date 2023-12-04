"""
This file is responsible for updating the mesh network node software, via OTAP operations. 
- A good description of how OTAP works can be found here: https://developer.wirepas.com/support/solutions/articles/77000496639-wirepas-massive-otap-application-note
- tutorial on how to otap nodes -> https://developer.wirepas.com/support/solutions/articles/77000498371-how-to-perform-otap-with-wirepas-massive-v5-1 
- How a node bootloader and flash memory work -> https://developer.wirepas.com/support/solutions/articles/77000496582-wirepas-massive-flash-structure-and-bootloader-application-note

Steps for updating the node software:
    1. **Propagate** to spread a new update image (called a Scratchpad) to all devices in a given network
    2. **Trigger**: to send an update command to a network
    3. **Process** and apply the Update: When all devices process the update image and move to the new version

Node software that can be updating with the OTAP algorithm:
    1. Wirepas stack 
    2. Application sitting in the same radio chipset.
    3. Other user memory areas

:Notes: for node
    1. In order for the OTAP to operate **some flash memory must be reserved** in each device to store the update image called Scratchpad.
    2. normal network operations are **disrupted** during the update process.

:Area ID: Can either be:
    1. Wirepas stack firmware AreaID (*Stack AreaID*): The Area ID is always the same for all devices having the same chipset
    2. Application Area ID (*AppAreaID*): Each application area shall have a unique 32-bit AreaID that is stored in the device’s memory. 
        It shall be different for all different application firmware areas. **AreaID’s cannot be changed afterward the firmware build process**
    3. User-defined Area ID, that can also be defined to store specific data related to the user application or system and which can be updated via the Wirepas OTAP mechanism. 
        It has the same properties as the *application area ID*

:Boatloader: Whenever a new OTAP scratchpad is found in memory, the bootloader authenticates it and iterates through the OTAP files (see Scratchpad). 
If any of the data files have a matching AreaID, the bootloader erases the referenced memory areas and then writes file contents there.

:examples: You can check the *examples* directory in the *wirepas_mqtt_library* in order to see some working examples of how to implement the otap updates.
"""

from wirepas_mqtt_library import WirepasNetworkInterface, WirepasOtapHelper
from mqtt_credentials import *
import wirepas_mesh_messaging as wmm

def use_otap(scratchpad, AreaID, seq_number):
    """
    :param scratchpad: An OTAP Scratchpad is binary data that gets copied from one node to another. A scratchpad is a collection of binaries transmitted via the OTAP. Each binary in a scratchpad has (among others) an Identifier to define the targeted component to be updated. This identifier is called AreaID and is a specific software component (a specific area in Flash memory to be accurate). 
    :type scratchpad: binary file
    :param AreaID: identifier for the firmware to update. 
    :type AreaID: int
    :param seq_number: version of the scratchpad. Stored in 1 byte, its value is 1-254. The latest OTAP scratchpad gets copied between nodes until all nodes have the same scratchpad sequence number.
    :type seq_number: int

    :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *bytes* Message payload to respond with

            


        """
    pass

wni = WirepasNetworkInterface(local_broker,
                              local_port,
                              local_user,
                              local_password,
                              insecure=local_insecure)

def print_all_sinks():
    """
    print all the sinks connected to the gateway

    :return:
        Nothing

    :does:
        Iterates through all links and prints gateway and sink ids
    """
    line = ""
    for gw, sink, config in wni.get_sinks():
        line += "[%s:%s] " % (gw, sink)

    print(line)

def get_gateway():
    """
    print the current gateway id

    :return:
        Nothing

    :does:
        prints the gateway ids connected to this backend
    """
    res = wni.get_gateways()
    print(res)


def send_all_sinks_to_all_nodes(msg="hola mon"):
    """
    For each sink connected to the backend, (it says network though), make them broadcast to all the nodes they can reach

    :param msg: A string to broadcast to all nodes
    :param type: string

    :return:
        Nothing

    :does:
        for each sink, broadcast message to all nodes
    """
    for gw, sink, config in wni.get_sinks():
        try:
            res = wni.send_message(gw, sink, 0xFFFFFFFF, 1, 1, msg.encode())
            if res != wmm.GatewayResultCode.GW_RES_OK:
                print("Cannot send data to %s:%s res=%s" % (gw, sink, res))
            else:
                print("message: " + msg + "\nsent successfully to sink: " + str(sink) +
                      "\nand gateway: " + str(gw) + "\nwith config: " + str(config))
        except TimeoutError:
            print("Cannot send data to %s:%s", gw, sink)
    


def upload_scratchpad(gw, sink, scratchpad, seq):
    """
    Calls the wni.upload_scratch() and loads the scratchpad to the desired sink.

    :param gw_id: Id of gateway the sink is attached
    :type gw_id: str
    :param sink_id: Id of sink
    :type sink_id: str
    :param seq: Sequence to use for this scratchpad
    :type seq: int
    :param scratchpad: Scratchpad to upload, None to clear the current stored one
    :type scratchpad: str
    :param cb: If set, callback to be asynchronously called when gateway answers

        **Expected signature**:

        .. code-block:: python

                on_scratchpad_uploaded_cb(gw_error_code, param)

        - gw_error_code: :obj:`~wirepas_mesh_messaging.gateway_result_code.GatewayResultCode`
        - param: param given when doing this call

        .. warning:: If unset, call is synchronous and caller can be blocked for up to 60 seconds

    :type cb: function
    :param param: Optional parameter that will be passed to callback
    :type param: object
    :return: None if cb is set or error code from gateway is synchronous call
    :rtype: :obj:`~wirepas_mesh_messaging.gateway_result_code.GatewayResultCode`

        """
    
    result = wni.upload_scratchpad(gw, sink, seq, scratchpad)

def process_scratchpad(gw_id, sink_id):
    """
    Process scratchpad on a given sink.

    :param gw_id: Id of gateway the sink is attached
    :type gw_id: str
    :param sink_id: Id of sink
    :type sink_id: str
    :param cb: If set, callback to be asynchronously called when gateway answers

        **Expected signature**:

        .. code-block:: python

            on_scratchpad_processed_cb(gw_error_code, param)

        - gw_error_code: :obj:`~wirepas_mesh_messaging.gateway_result_code.GatewayResultCode`
        - param: param given when doing this call

        .. warning:: If unset, call is synchronous and caller can be blocked for up to 60 seconds

    :type cb: function
    :param param: Optional parameter that will be passed to callback
    :type param: object
    :return: None if cb is set or error code from gateway is synchronous call
    :rtype: :obj:`~wirepas_mesh_messaging.gateway_result_code.GatewayResultCode`

    :raises TimeoutError: Raised if cb is None and response is not received within 60 sec
    :does: Calls the wni function :py:meth:`~wni.upload_scratchpad()` 

    """



    wni.process_scratchpad(gw_id, sink_id)

def propag_and_process(wni , network):
    """
    :param wni: Wirepas network interface
    :type wni: :obj:`~wirepas_mqtt_library.wirepas_network_interface.WirepasNetworkInterface`
    :param network: Network address concerned by the otap
    """
    
    otapHelper = WirepasOtapHelper(wni, network)
    
    otapHelper.set_propagate_and_process_scratchpad_to_all_sinks(seq=None, crc=None, delay=None)

def set_target_scratchpad(gw_id, sink_id):
    """
    set_target_scratchpad(self, gw_id, sink_id, action, cb=None, param=None)
    Set target scratchpad on a given sink

    :param gw_id: Id of gateway the sink is attached
    :type gw_id: str
    :param sink_id: Id of sink
    :type sink_id: str
    :param action: Action to set
    :type action: :class:`wirepas_mesh_messaging.otap_helper.ScratchpadAction`
    :param cb: If set, callback to be asynchronously called when gateway answers

        **Expected signature**:

        .. code-block:: python

            on_target_set_cb(gw_error_code, param)

        - gw_error_code: :obj:`~wirepas_mesh_messaging.gateway_result_code.GatewayResultCode`
        - param: param given when doing this call

        .. warning:: If unset, call is synchronous and caller can be blocked for up to 2 seconds

    :type cb: function
    :param param: Optional parameter that will be passed to callback
    :type param: object
    :return: None if cb is set or error code from gateway is synchronous call
    :rtype: :obj:`~wirepas_mesh_messaging.gateway_result_code.GatewayResultCode`

    :raises TimeoutError: Raised if cb is None and response is not received within 2 sec
    """
    PROPAGATE_AND_PROCESS = 3

    result = wni.set_target_scratchpad(gw_id, sink_id, action=PROPAGATE_AND_PROCESS)
    return result