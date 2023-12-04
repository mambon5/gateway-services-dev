"""
Message class used in all interactions.

"""

from struct import *
import global_vars as gvar # import global variables
import message_received_parse_functions as parsef # import global variables
import database_functions as db_fs # import functions for writing and reading of messages to/from the database
import sqlite3              # to save certain messages to a sql database 
import message_display_functions as displayf
import compute_crc as get_crc

# global variables to import and use within the RxMsg class:

DB_PATH = db_fs.DB_PATH                                         #: database path
DB_NAME = db_fs.DB_NAME                                         #: database name        
datab = DB_PATH + DB_NAME                                       #: table names
TABLE_SUCCESS = db_fs.TABLE_SUCCESS                             #: table of successfully requests
TABLE_FAILS = db_fs.TABLE_FAILS                                 #: table of failed requests
TABLE_REQUESTS_SENT = db_fs.TABLE_REQUESTS_SENT                 #: table of requests sent
TABLE_RECEIVED_RESPONSES = db_fs.TABLE_RECEIVED_RESPONSES        #: table of received responses


class RxMsg:
    """
    Message received class.
    The message is the main way of communicating information between the cloud, the gateway and the nodes. 
    Every message will use this format when processed by the gateway.
   
    :does:
    1. Parsing of the received messages (main functionality of the class)
    2. Display of messages
    3. Storage of messages
    4. Calls specific functions depending on the message type, for parsing, displaying and storage.

    
   
    :param payload: message payload, has a variable length
    :type payload: bytes
    :param topic: MQTT topic where the message was published. It is None for node to gateway messages.
    :type topic: string
    :param source_address: node id that sent the message. It is None for cloud to gateway messages.
    :type source_address: int
    :param gw_id: gateway id to who the message was sent.
    :type gw_id: int
    :param sink_id: sink id that received the message in the gateway
    :type sink_id: int


    :return:

        Returns a **RxMsg** class with the following attributes:

            :payload: (bytes) -- received message data payload 
            :msg_type: (int) -- message TYPE decoded from given data payload (value is None at init time)
            :msg_id: (int) -- unique message temporal identifier
            :gw_id: (int) -- gateway id
            :sink_id: (int) -- sink id
            :node_id: (int) -- node id that sent the message
            :topic: (string) -- mqtt topic to which the message was sent (if applicable, for node messages this is None)
            :args: (list) -- list of additional arguments (besides message id, and msg_type) contained in the message
    """
    def __init__(self, payload=None, topic=None, source_address=None, gw_id=None, sink_id=None, rawdata=None):
        """
        Initialize class instance attributes.

        """
        self.payload = payload       
        self.type = None
        self.msg_fields = []
        self.topic = topic
        self.id = None
        self.node_id = source_address
        self.gw_id = gw_id
        self.sink_id = sink_id
        self.args = []
        self.rawdata = rawdata
        self.sub_supertopic = None

# In order to translate from bytes to hex and viceversa it is good to read https://linuxhint.com/string-to-hexadecimal-in-python/
# here you can use int("0x0A",16) to put this int into base 16.

# when using the struct method "unpack", the format "<" means little endian, the format "B" means an unsigned int of 1 byte, and the format
# "I" means a unsigned int of 4 bytes. Read the Readme.m of the evaluation app of wirepas sdk to understand how each byte is encoded in each message

    







# Store messages: #############################################

    # save node perdiodic message into sqlite3 database:
    def save_periodic_message_to_db(self, node_id, timestamp):
        """
        Save the periodic messages to the database
        


        :param node_id: node id
        :type node_id: int
        :param timestamp: custom timestamp and date up to the milliseconds
        :type timestamp: string       
        
        :return:
            None
        """    
        # connecting to database if not already connected
        # if 'conn' not in locals():
        global datab

        prefix = "<store>: "
        print("database: " + datab)

        #table name:
        table = "node_status"
 
        conn = sqlite3.connect(datab)   
        print ("\n" + prefix + "Opened database '"+ datab +"' successfully\n ")

        try: 
        # check if table is there 
            conn.execute('''SELECT * FROM '''+table+'''
                LIMIT 1;''')
        # if it succeeds, table exists

        # now if table doesn't exist, create it:
        except:
            print(prefix +"creating SQL table "+table+"...")
            conn.execute('''CREATE TABLE ''' +table+ '''
                (node_id TEXT      NOT NULL,
                time           TEXT     NOT NULL,
                node_counter           TEXT     NOT NULL,
                primary key (node_id, time, node_counter));''')
            print(prefix +"Table "+table+" created successfully")

        node_counter = str(self.msg_fields[0])
        # add data to table now:
        row = [(node_id, timestamp,node_counter)]
        # Print header information of received message.
        print(prefix +"Storing record to database; \n node id: {}\n date-time: {}\n counter value: {} \n...".format(node_id,timestamp, node_counter ))
        
        conn.executemany("INSERT INTO " +table+ " (node_id, time, node_counter) \
            VALUES (?, ?, ?)", row);
        conn.commit()
        print (prefix +"New data added to table "+table+" successfully")

        conn.close()
        print (prefix +"Database connection closed")

    def register_node_to_db(self, node_id, timestamp):
        """ 
        Register or update a node. Each time that a node sends a message, and this function is
        triggered, we will store the following information to the database to register the new node:
        
        - node_id TEXT      NOT NULL,
        - active           INT     NOT NULL,
        - led_status           INT     DEFAULT -1,
        - dimming           INT     DEFAULT -1,
        - first_seen           TEXT     DEFAULT "not yet",
        - last_seen           TEXT     DEFAULT "never",
        - amount_of_neighbours    INT     DEFAULT -1,
        - hops    INT     DEFAULT -1,
        - rssi    INT     DEFAULT -1,
        
        if this node was already registered, then we will only update the following parameters:

        - last seen time
        
        :param node_id: node id
        :type node_id: int
        :param timestamp: custom timestamp and date up to the milliseconds
        :type timestamp: string       
        
        :return:
            None
        """   

        # connecting to database if not already connected
        # if 'conn' not in locals():

        global datab
        prefix = "<store>: register node.. "        
        
        #table name:
        table = "nodes"
 
        conn = sqlite3.connect(datab)   
        print ("\n" + prefix + "Opened database '"+ datab +"' successfully\n ")

        try: 
        # check if table is there 
            conn.execute('''SELECT * FROM '''+table+'''
                LIMIT 1;''')
        # if it succeeds, table exists

        # now if table doesn't exist, create it:
        except:
            print(prefix +"creating SQL table "+table+"...")
            conn.execute('''CREATE TABLE ''' +table+ '''
                (node_id TEXT      NOT NULL,
                active           INT     NOT NULL,
                led_status           INT     DEFAULT -1,
                dimming           INT     DEFAULT -1,
                first_seen           TEXT     DEFAULT "not yet",
                last_seen           TEXT     DEFAULT "never",
                amount_of_neighbours    INT     DEFAULT -1,
                hops    INT     DEFAULT -1,
                rssi    INT     DEFAULT -1,
                primary key (node_id));''')
            print(prefix +"Table "+table+" created successfully")

        # looking for the received node 
        cursor = conn.execute("SELECT * from " + table + " WHERE node_id = '{}'".format(node_id))
        # get all the fileds we store for a node:
        column_names = list(map(lambda x: x[0], cursor.description))

        #counting the times the node is there
        rows_read=0
        for row in cursor:
            rows_read=rows_read+1

        if rows_read == 0: 
            # register node
            active = 1
            
            rows = [(node_id, active,timestamp, timestamp)]
            row = rows[0]
            # Print header information of received message.
            print(prefix +"Storing record to database; \n node id: {}\n active: {}\n first_seen: {} \n last_seen: {} \n...".format(row[0], row[1], row[2], row[2] ))
            
            conn.executemany("INSERT INTO " +table+ " (node_id, active, first_seen, last_seen) \
                VALUES (?, ?, ?, ?)", rows);
            conn.commit()
            print (prefix +"New data added to table "+table+" successfully:")

        elif  rows_read > 1:
            print(prefix + "error: node "+ str(node_id) + " appears more than once in table "+ table)  
        else:
            # node already registered:  
            active = row[1]
            if active == 1:
                print(prefix + "node was active")
            else:                
                print(prefix + "node was dead, and is now active")
            # preparing new updates for the registered node:
            active = 1
            last_seen = timestamp
            
            # updating some parameters of the entry
            new_row = list(row)
            new_row[1] = active
            new_row[5] = last_seen

            # saving the node updates into the database
            query = "UPDATE " + table + " SET "+ db_fs.sql_set_values(new_row, column_names) +" WHERE node_id = '{}'".format(node_id)
            print("query: " + query)
            cursor = conn.execute(query)
            conn.commit()
            print(prefix + " table "+ table + " updated properly!")

            # send message to user:
            row_text = db_fs.get_row_string(new_row, column_names)
            print(prefix + "node {}".format(node_id) + " already registered in table " + table + " of database " + datab + ":")
            print(prefix + row_text)
                          
            
            
        print (prefix +"Database connection closed")
        conn.close()

    def add_msg_to_response_received_table(self, gateway_id, sink_id, node_id, timestamp):
        """ 
        Save response received to the responses_received table.
        
        :Note: 
            this function is bound to disappear, since it is not necessary anymore. 
            Instead, the gateway can open a "listening" thread and await for the 
            message id to be received, just before sending its message to the node.
            This way we avoid having to use the hard disk in order to use the 
            request-response messaging mechanism.

        :param gateway_id: gateway id
        :type gateway_id: int
        :param sink_id: sink id
        :type sink_id: int 
        :param node_id: node id
        :type node_id: int
        :param timestamp: custom timestamp and date up to the milliseconds
        :type timestamp: string       
        
        :return:
            bool -- true if successful
        
            """
        # connecting to database:
        global datab
        prefix = "<store: response-received>.. "        
        
        #table name:
        table = TABLE_RECEIVED_RESPONSES
 
        conn = sqlite3.connect(datab)   
        print ("\n" + prefix + "Opened database '"+ datab +"' successfully\n ")

        try: 
        # check if table is there 
            conn.execute('''SELECT * FROM '''+table+'''
                LIMIT 1;''')
        # if it succeeds, table exists

        # now if table doesn't exist, create it:
        except:
            print(prefix +"creating SQL table "+table+"...")
            conn.execute('''CREATE TABLE ''' +table+ '''
                (msg_id INT      NOT NULL,
                msg_type INT    NOT NULL,
                node_id           TEXT     NOT NULL,
                gateway_id           TEXT     NOT NULL,
                sink_id           TEXT     NOT NULL,
                timestamp           TEXT     NOT NULL
                );''')
            print(prefix +"Table "+table+" created successfully")

        # register response received
        rows = [(self.id, self.type, node_id, gateway_id, sink_id, timestamp)]
        row = rows[0]

        # Print header information of received message.
        print(prefix +"Storing record to table {}; \n message id: {} \n message type: {}\n node id: {}\n gateway id: {} \n sink id: {} \
            \n time: {}\n ...".format(table, row[0], row[1], row[2], row[3], row[4], row[5] ))
        
        conn.executemany("INSERT INTO " +table+ " (msg_id, msg_type, node_id, gateway_id, sink_id, timestamp ) \
            VALUES (?, ?, ?, ?, ?,?)", rows)
        conn.commit()
        print (prefix +"New data added to table "+table+" successfully:")
 
        print (prefix +"Database connection closed")
        conn.close()
        
        return True

    def get_msg_id_and_type(self):
        """
        Parse the *msg type* and *message id* fields from the message payload.

        :does:
            1. calls the :py:meth:`~message_received_class.RxMsg.get_msg_type` and :py:meth:`~message_received_class.RxMsg.get_msg_id`  functions which will extract the first 3 bytes of the message
            2. returns an error if it is unsuccessful in any of its steps.

        :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* return arguments. Empty if parsing was ok, otherwise returns the error type
        """

        result = [False, []]
        prefix = "<computing message id and type> "

        # Check that the payload has at least one byte
        if type(self.payload) is bytes:
            # Parse message type
            res_msg_id = self.get_msg_id()
            res_msg_type = self.get_msg_type()
            if not res_msg_id[0]:
                result[1] = [ res_msg_id[1]]                # if there was a problem parsing the message id, send that error as the problem 
            elif not res_msg_type[0]:
                result[1] = [ res_msg_type[1] ]             # if message id was parsed ok, but the type wasn't, then send that error.
            else:
                result[0] = True

        else:
            self.type = gvar.MSG_TYPE_ERROR
            self.id = gvar.MSG_TYPE_INVALID_UNSUPPORTED_MSG
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]
            print("{} message payload recieved has 0 bytes".format(prefix))
             
        return result

    def get_msg_type(self):
        """
        Parse the *msg type* field from the message payload.

        :does:
            1. Unpacks the third byte of the received message payload.
            2. If everything is correct, it will store the unpacked number as the message type attribute of the RxMsg class
            3. If the lenght of the message is 0, it will report an error, "unexpected message length"
            4. If the message type is not in the supported message list, it will report another error, "invalid message type"

        :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* return arguments. Empty if parsing was ok, otherwise returns the error type

        """
        message_type = None
        result = [False, []]
        prefix = "<computing message type> "
       
        # Get message type field from payload (little-endian bytes order and
        # one unsigned byte to parse.
        message_type = list(unpack('<B', self.payload[2:3])).pop()
        # convert to int type
        # message_type = int.from_bytes(message_type, gvar.MSG_PAYLOAD_ENDIANNESS)
        llista = gvar.MSG_SUPPORTED_LIST_NODE
        llista.extend(gvar.MSG_SUPPORTED_LIST_CLOUD)
        if message_type not in llista:
            # Unknown or unsupported message type received so return an invalid value.
            message_type = gvar.MSG_TYPE_INVALID_UNSUPPORTED_MSG
            result[1] = [gvar.ERROR_TYPE_INVALID_MSG_TYPE]
            print(prefix + "error: message type not in the cloud or node uspported lists")
        else:
            result[0] = True    # operation was successful
       

        self.type = message_type

        return result
 
    def get_msg_id(self):
        """
        Parse the *msg id* field from the message payload.

        :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* return arguments. Empty if parsing was ok, otherwise returns the error type
        """
        message_id = None
        prefix = "<parse msg id>"
        result = [False, []]

        # Get message type field from payload (little-endian bytes order and
        # one unsigned byte to parse.
        try:
            message_id = list(unpack('<H', self.payload[0:2])).pop()
            result[0] = True
        except:
            message_id = gvar.MSG_TYPE_INVALID_UNSUPPORTED_MSG
            result[1] = [gvar.ERROR_TYPE_UNEXPECTED_MESSAGE_LENGTH]
            print("{} error: parsing message id".format(prefix))

        self.id = message_id

        return result

    def get_node_id(self, sub_supertopic):
        """
        Parse the *node id* field from the message payload.

        :param sub_supertopic: subscription MQTT supertopic to which the message was sent. Default to None for node-to-gateway messages
        :type sub_supertopic: string
        
        
        :return:
            None
        """
        if sub_supertopic != None : # if message origin are not hte nodes, then get the gateway id
            subject = self.topic.split("/")[1]
            if subject == "gw" : # to gateway
                self.node_id = "all"
            elif subject == "n" : # to node
                self.node_id = self.topic.split("/")[2] #getting the node id from the topic


    def get_sub_supertopic(self, sub_topic):
        """getting message origin: (in the case of gateway - node messaging this will be None)

        :param sub_topic: subscription MQTT topic to which the message was sent. Default to None for node-to-gateway messages
        :type sub_topic: string

        :does: 
            1. compute the MQTT super topic, according to the topic received.
            2. stores the value into an accessible attribute of the message named the same

        """

        self.sub_supertopic = gvar.get_supertopic(sub_topic)
        

    def get_gw_id(self, sub_supertopic):
        """
        Parse the *gateway id* field from the message payload.
        
        :param sub_supertopic: subscription MQTT supertopic to which the message was sent. Default to None for node-to-gateway messages
        :type sub_supertopic: string
        
        
        :return:
            None        
        """
        if sub_supertopic != None :
            subject = self.topic.split("/")[1]
            if subject == "gw" : # to gateway
                self.gw_id = self.topic.split("/")[2]
            elif subject == "n" and self.gw_id == None : # to node
                self.gw_id = "unknown"



    def parse_basic(self, sub_topic): 
        """
        Basic parsing for received messages. It does the most basic parsing of any message received. It just computes the 
        
        :does: 
            1. Extracts the:

                - *message id* using the :py:meth:`~message_received_class.RxMsg.get_msg_id_and_type` function
                - *message type* using the :py:meth:`~message_received_class.RxMsg.get_msg_id_and_type` function
                - *gateway id* using the :py:meth:`~message_received_class.RxMsg.get_gw_id` function
                - *node id* using the :py:meth:`~message_received_class.RxMsg.get_node_id` function
               from the message payload, and saves it in the :py:meth:`~message_received_class.RxMsg` class.
            2. It returns *True* if the message basic parsing was successful, and *False* plus the error message, otherwise.

        :param sub_supertopic: subscription MQTT supertopic to which the message was sent. Default to None for node-to-gateway messages
        :type sub_supertopic: string
        
        
        :return:
        **result** (*list*) --  
            - [0] - *bool* (True if successful, False if failed)
            - [1] - *list* return arguments. Empty if parsing was ok, otherwise returns the error type
        """
        prefix = "<parse basic>: "
        result = [False, []]

        print(prefix + "message received!")
        # Clear fields list
        self.msg_fields.clear()
        # Clear message type attribute
        self.id = None
        self.type = None

        # extra parsing instructions when the msg comes from cloud mqtt broker to gateway:
        self.get_sub_supertopic(sub_topic)
        self.get_gw_id(self.sub_supertopic)
        self.get_node_id(self.sub_supertopic)
        # self.get_sink_id(self.sub_supertopic)

        # Check payload data has the right data type before trying to parse anything.
        res_parse_id_and_type = self.get_msg_id_and_type()
        
        print(prefix + "msg id: " + str(self.id) + ", msg type: " + str(self.type) + ", payload length: " + str(len(self.payload)) + " bytes, payload: " + str(self.payload))
        print(prefix + "basic parsing complete")

        if res_parse_id_and_type[0]:
            result[0] = True
        else:
            result[1] = res_parse_id_and_type[1]

        return result
        

    # parse message
    def parse(self, sub_topic, mode=None):
        """

        Main parsing function. 

        :does:
        
        1. call the :py:meth:`~message_received_class.RxMsg.parse_basic` function
        2. if the basic parsing was ok, then depending on the 
        
           
            - **message origin** (cloud or nodes)

           a different parsing function from :py:meth:`~message_received_parse_functions` will be called.
        3. After that, a specific parsing function from :py:meth:`~message_specific_parse_functions` will be called
           depending on the 
         
            - **message type**,

           which is designed specifically for that type of message. 
        4. The specific parsing function will save additional rellevant data contained in the message, in the
           **args** attribute (from arguments) of the :py:meth:`~message_received_class.RxMsg` class, as a list of objects.
        5. Finally, it will return *True* if the parsing was all successfull, and *False* if there has been any kind of issue.
        
        :param sub_supertopic: subscription MQTT supertopic to which the message was sent. Default to None for node-to-gateway messages
        :type sub_supertopic: string
        
        :return:

            **result** (*bool*) -- True if parsing was successful, False if it failed)

        """
        prefix = "<parse>: "

        result = [False,[]]
        res_pbasic = self.parse_basic(sub_topic)
 
        # Check payload data has the right data type and that the basic parsing was successful before trying to parse anything.
        if res_pbasic[0] and type(self.payload) is bytes:            

            # Check if message ID parsing was successful and parse message
            # payload accordingly. Bear in mind these are all response messages

            # print(prefix + "message id: " + str(self.id))
            # print(prefix + "message type: " + str(self.type))
            # print(prefix + "raw data length: " + str(len(self.payload)))
            # print(prefix + "raw data payload: " + str(self.payload))            

            if self.sub_supertopic == gvar.CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC:
                # cloud requests to node
                print(prefix + "cloud to node message request")
                result = parsef.parse_cloud_request_to_node(self, prefix)

            elif self.sub_supertopic == gvar.CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
                # cloud requests to gateway
                print(prefix + "cloud to gateway message request")
                result = parsef.parse_cloud_request_to_gateway(self, prefix)
                
            elif self.sub_supertopic == gvar.CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_SUPERTOPIC:
                # cloud response to a gateway request
                print(prefix + "cloud_response_to_gateway_req") 
                result = parsef.parse_cloud_response_to_gateway_req(self, prefix)

            elif self.sub_supertopic == None and mode == "listen": 
                # node --> gateway messages
                result = parsef.parse_node_to_gw_request(self, prefix)

            elif self.sub_supertopic == None and mode == "request":
                # gateway --> node messages
                result = parsef.parse_node_to_gw_response(self, prefix)
                # responses to gw requests to nodes, and node direct messages are not differentiated when received, 
                # only afer parsing. So we put them all here.

            # DELETE THE FOLLOWING THREE CASES AND FUNCTIONS FOR PRODUCTION: (this is just for testing purposes)
            # gateway response to cloud_to_node_req
            elif self.sub_supertopic == gvar.GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC:
                print(prefix + "gateway response to cloud request to node")
                result = parsef.parse_gateway_response_to_cloud_to_node_req(self, prefix)

            # gateway response to cloud request to gateway
            elif self.sub_supertopic == gvar.GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
                print(prefix + "gateway response to cloud request to gateway")
                result = parsef.parse_gateway_response_to_cloud_to_gateway_req(self, prefix)

            # gateway request to cloud
            elif self.sub_supertopic == gvar.GATEWAY_REQUEST_TO_CLOUD_MQTT_SUPERTOPIC:
                print(prefix + "gateway request to cloud")
                result = parsef.parse_gateway_request_to_cloud(self, prefix)

            else:
                print(prefix+"error: invalid message origin!")
                # create an error message
                result[1] = [gvar.ERROR_TYPE_INVALID_MSG_ORIGIN_MQTT_TOPIC]

        else:
            # Invalid payload type: return parsing failed.
            # create an error message
            if not res_pbasic[0]:
                print("{} error in parse basic".format(prefix))
                result[1] = res_pbasic[1]
            else:
                print(prefix+"message payload not in bytes")                
                result[1] = [gvar.ERROR_TYPE_PAYLOAD_NOT_IN_BYTES]
        
        # # the arguments are the second element of "result"
        # self.args = result[1]

        if not result[0]:   # if result is false (or parsing went wrong), set up a msg error type
            self.type = gvar.MSG_TYPE_ERROR
        
        self.args = result[1]       # very important line, do not delete otherwise we loose the received message arguments!

        return result[0]    # in the parsing, it makes only sense to return the bool, not the arguments, since they will be already stored in the msg.args

    def display(self, timestamp, print_raw_data = False):
        """
        Function to display the message fields.

        :does:
        1. Takes the parsed message         
        2. Calls the specific display function from :py:meth:`~message_display_functions` depending on:
            - **message type**
            - **message origin** (cloud or nodes)
            
        :param timestamp: timestamp passed by the caller
        :type timestamp: datetime (custom format)
        :param print_raw_data: Print raw data or not
        :type print_raw_data: bool
        
        :return:
            None

            """
        prefix = "<display>: "
        # format timestamp as YYYY-MM-DD HH:MM:SS        
        if print_raw_data:
            try:
                print(self.data)
            except:
                print(prefix + "no raw data to show")
        # Print header information of received message.
        print(prefix + "Received message at {} at gateway <{}>, sink <{}>, node <{}> :".format(
            timestamp, self.gw_id, self.sink_id, self.node_id))
        # print(prefix + "Displaying the message in general:")
        # self._display_general_message()

        if self.sub_supertopic == gvar.CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC:
            # cloud requests to node
            print(prefix + "cloud to node message request")
            displayf.display_cloud_request_to_node(self, prefix)

        elif self.sub_supertopic == gvar.CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
            # cloud requests to gateway
            print(prefix + "cloud to gateway message request")
            displayf.display_cloud_request_to_gateway(self, prefix)
            
        elif self.sub_supertopic == gvar.CLOUD_RESPONSE_TO_GATEWAY_REQUEST_MQTT_SUPERTOPIC:
            # cloud response to a gateway request
            print(prefix + "cloud_response_to_gateway_req") 
            displayf.display_cloud_response_to_gateway_req(self, prefix)

        elif self.sub_supertopic == None: 
            # gatewat <--> node messages
            print(prefix + "gateway to node messaging") 
            displayf.display_gateway_node_messages(self, prefix)
            # responses to gw requests to nodes, and node direct messages are not differentiated when received, 
            # only afer parsing. So we put them all here.

        # DELETE THE FOLLOWING THREE CASES AND FUNCTIONS FOR PRODUCTION: (this is just for testing purposes)
        # gateway response to cloud_to_node_req
        elif self.sub_supertopic == gvar.GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_NODE_MQTT_SUPERTOPIC:
            print(prefix + "gateway response to cloud request to node")
            displayf.display_gateway_response_to_cloud_request_to_node(self, prefix)

        # gateway response to cloud request to gateway
        elif self.sub_supertopic == gvar.GATEWAY_RESPONSE_TO_CLOUD_REQUEST_TO_GATEWAY_MQTT_SUPERTOPIC:
            print(prefix + "gateway response to cloud request to gateway")
            displayf.display_gateway_response_to_cloud_request_to_gateway(self, prefix)

        # gateway request to cloud
        elif self.sub_supertopic == gvar.GATEWAY_REQUEST_TO_CLOUD_MQTT_SUPERTOPIC:
            print(prefix + "gateway request to cloud")
            displayf.display_gateway_request_to_cloud(self, prefix)

        else:
            print(prefix+"error: invalid message origin!")


       

    def store(self, gateway_id, sink_id, node_id, timestamp):
        """
        Saves to the database the received message payload arguments. The Gateway is responsible for 
        creating and mantaining the databases

        If the global variable *store_messages* is set to True, this function will be called in different moments
        and store the following information:
        
        1. Register nodes to the database
        2. add_msg_to_response_received_table (depracated, this function is not necessary anymore and will be deleted)


        :param timestamp: timestamp passed by caller
        :type timestamp: datetime (custom format)
        :param gateway_id: gateway id
        :type gateway_id: int
        :param sink_id: sink id
        :type sink_id: int
        :param node_id: node id
        :type node_id: int


        :return:
            None
        """
        

        # save message to responses_recieved or node_requests
        if self.type in gvar.MSG_RESPONSE_RECEIVED_FROM_NODES_LIST :
            self.add_msg_to_response_received_table(gateway_id, sink_id, node_id, timestamp)

        else: 
            print("cannot store received message, the msg type doesn't match any of: "+ " ".join([ str(value) for value in gvar.MSG_RESPONSE_RECEIVED_FROM_NODES_LIST]))

        # register node, if not yet registered:
        # in any recieved message, first store/check if already stored the node in the nodes table:
        self.register_node_to_db(node_id, timestamp)

        # print('')  # separate each new message display by one empty line 
