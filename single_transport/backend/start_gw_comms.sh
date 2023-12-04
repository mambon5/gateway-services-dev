#!/bin/bash

python3 check_internet.py 2         # check internet connection momentarily, and restart gateway services if no 
                                    # connection
python3 check_internet.py 1  &      # check internet connection in a forever loop, and restart services if internet 
                                    # connection is lost at some point. Call this asyncronously
python3 send_ip.py                  # send alive signal to cloud, with gw id and ip
python3 remote_control_gw.py &      # start remote connection with the cloud
python3 start_gw_comms.py           # the taskset command with the cpu list, allows us to say how many CPUs 
                                    # to use for running a specific app

