"""Main node to gateway interaction class.


"""

from mqtt_interaction_node_basic import mqtt_interaction_node_basic
import update_gw_database as updb
import read_gw_database as readdb
import prepare_response as sdresp
import interaction_tunnel as intunnel
import otap_specific_functions as ospef
import global_vars as gvar
from wirepas_mqtt_library import WirepasOtapHelper

class mqtt_interaction_node_main(mqtt_interaction_node_basic):
    """
    This is the main interaction class with the nodes. 
    
    :structure:
        1. It will be running as long as the gateway is powered and until the script is stopped externally by someone or an error.
        2. It listens to all the node messages, and then creates all the cloud-classes that listen
           to the cloud messages directed towards the nodes. 
        3. It is the director of the wirepas orchestra.
        4. It has the following methods:
            - :py:meth:`~mqtt_interaction_node_main.mqtt_interaction_node_main.on_message_main_node_listen`
            - :py:meth:`~mqtt_interaction_node_main.mqtt_interaction_node_main.update_node_list`
          
    :param wni: the wirepas network interface class connected to the selected local mqtt broker     
    :type wni: WirepasNetworkInterface
    :param mode: mode of the interaction. Can be either "listen" to receive messages from the subtopic, or "request" if we want to the entity to publish requests to the pubtopic
    :type mode: string
    :param node_list: list of nodes that the gateway can see and talk to
    :type node_list: string

    :return:
        Returns a :py:meth:`~mqtt_interaction_node_basic.mqtt_interaction_node_basic` class with the following attributes:
            :node_id_list: (int) -- list of all nodes connected to the gateway at some point
    """

    def __init__(self, mode="listen", wni=None, node_list = []):
        prefix = "<init mqtt main node interac> "
        self.node_id_list = node_list         # here we will keep track of all the nodes we read

        mqtt_interaction_node_basic.__init__(self, mode=mode, wni=wni) 

        if self.node_id_list == []: # in case no node list was supplied, get one:
            # getting node list of available nodes:
            print("{} no valid node list supplied, computing one...".format(prefix))
            otapHelper = WirepasOtapHelper(self.wni,
                                    int(gvar.NETWORK_DEFAULT_CHANNEL))
            self.node_id_list = ospef.get_node_list(otapHelper)
        
        print("{} node list detected by sink: {}".format(prefix, self.node_id_list))
       
        # for each node in the list, start listening to cloud messages for that specific node id.
        for node_id in self.node_id_list:
            cloudtunel = intunnel.tunnel_to_cloud(node_id, self.wni)     

    # this is the alternative function to the "on_listen" function defined in the main mqtt_interaction class for cloud ineractions
    def on_message_main_node_listen(self, msg, parsed):
        """
        Every time a node sends a message to the gateway, this functions is executed.

        :does:
            1. Tunnel to cloud (i.e. starts listenning to incoming cloud messages, if the node that sends the message is unregisterd by the gateway)
            2. Update the database (if applicable)
            3. Read gateway database (if applicable)
            4. Prepare the response based on the results of the previous actions
            5. Send the message to the nodes, if the message is a node request, by calling the function 
               :py:meth:`~mqtt_interaction_module.mqtt_interaction.publish`
           
        :Note:  - It is the equivalent to the :py:meth:`~mqtt_interaction_cloud.mqtt_interaction_cloud.on_message_c` function of the
                mqtt_interaction_cloud class.

        :references:
            1. It is useful to check the wirepas mqtt library documentation -> https://wirepas.github.io/wirepas-mqtt-library/ 

        :param msg: message class
        :type msg: RxMsg
        :param parsed: True if parsing was successful, False if failed
        :type parsed: bool
            

        """

        prefix = "<on_message_event (nodes) main listen>: "
            
        # prepare tunnel to cloud
        cloudtunel = intunnel.prepare_cloud_tunnel(msg, self)           
                    
        # update database::
        update_db = updb.update_gw_database(msg, self.mode, self.interlocutor, self)
        
        # read database::
        read_db = readdb.read_gw_database(msg, self.mode, self.interlocutor)
    
        # prepare response:
        result = sdresp.prepare_response(msg, parsed, update_db, read_db, self.mode, self.interlocutor, self.pubtopic, cloudtunel)
        
        # error in prep response
        if not result[0]:
            print(prefix + "response preparation failed. Quitting execution...")
            return
        
        payload = result[1]
        # send response message if recieved message is a node request
        if self.is_a_msg_request(msg.type):
            print(prefix + "sending msg to gw: {}, sink: {} and node: {}".format(self.gw_id, self.sink, msg.node_id))
            if self.publish(payload, self.gw_id, self.sink, msg.node_id) :
                print(prefix + "response sent successfully")
            else:
                print(prefix + "error: in publishing, response not sent. Message payload: " + str(payload))


    def update_node_list(self, node_id):
        """
        Updates the node id list, if necessary. This function is executed everytime a node message is received.

        :does:
            1. Checks whether the node id that sent the message, is not already in the node list.
            2. If it is not there, then add it.

        :param node_id: Node id that has been detected on a new message. 
        :type node_id: int

        :return:
            Nothing
        """
        prefix = "<update node list> "

        if node_id not in self.node_id_list:
            self.node_id_list.append(node_id)
            print(prefix + "node {} added to the gateway node list".format(node_id))
        else:
            print(prefix + "node {} already in the list".format(node_id))

