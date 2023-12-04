
# To do 

- [To do](#to-do)
- [TO DO in the code:](#to-do-in-the-code)
- [TO DO in general:](#to-do-in-general)
  - [7. Tests to check robustness of otap:](#7-tests-to-check-robustness-of-otap)
  - [8. Add OTAP and gw software versions](#8-add-otap-and-gw-software-versions)
  - [9. Organize all the documentation again:](#9-organize-all-the-documentation-again)
- [I WAS LAST DOING:](#i-was-last-doing)
- [LAST DISCOVERIES:](#last-discoveries)
  - [1. (08-02-23) If I have a primitive class and extend it.](#1-08-02-23-if-i-have-a-primitive-class-and-extend-it)
  - [2. (08-02-23) Dont duplicate code](#2-08-02-23-dont-duplicate-code)
  - [3. "not connect found" error](#3-not-connect-found-error)
  - [4. Error  *AttributeError: 'WirepasNetworkInterface' object has no attribute '\_connected'*](#4-error--attributeerror-wirepasnetworkinterface-object-has-no-attribute-_connected)
  - [5. Error *Message sending failed: res=GatewayResultCode.GW\_RES\_SINK\_OUT\_OF\_MEMORY*](#5-error-message-sending-failed-resgatewayresultcodegw_res_sink_out_of_memory)
  - [6. SolidRun jumpers (under the motherboard)](#6-solidrun-jumpers-under-the-motherboard)
  - [7. Many Subacks on cloud mqtt](#7-many-subacks-on-cloud-mqtt)
  - [8. Doing otap: Scratchpad stored status has error 4](#8-doing-otap-scratchpad-stored-status-has-error-4)
- [LEARNED THINGS:](#learned-things)
  - [1. How to document the code](#1-how-to-document-the-code)
  - [2. List of wirepas mqtt topics](#2-list-of-wirepas-mqtt-topics)
  - [3. Subscribe to mosquitto topic:](#3-subscribe-to-mosquitto-topic)
  - [4. Find strings in linux directories.](#4-find-strings-in-linux-directories)
  - [5. Count the number of lines](#5-count-the-number-of-lines)
  - [6. Get the gateway id](#6-get-the-gateway-id)
  - [7. Change sink configuration](#7-change-sink-configuration)
  - [8. Installing gateway **S-CONNECT** with ubuntu 22.01,](#8-installing-gateway-s-connect-with-ubuntu-2201)
  - [9. Using Git](#9-using-git)
    - [0 Starting a local github repo](#0-starting-a-local-github-repo)
    - [1 Commiting and pushing to remote repo](#1-commiting-and-pushing-to-remote-repo)
    - [2 Storing git credentials in pc](#2-storing-git-credentials-in-pc)
    - [3 Pull git changes and overwrite local modifications](#3-pull-git-changes-and-overwrite-local-modifications)
    - [4 Adding tags to github](#4-adding-tags-to-github)
    - [5 Creating a github release](#5-creating-a-github-release)
    - [6 Cleaning the .git folder](#6-cleaning-the-git-folder)
    - [7 Link your local repo to a new remote repo](#7-link-your-local-repo-to-a-new-remote-repo)
    - [8 Remote SSH keys for gateway control](#8-remote-ssh-keys-for-gateway-control)
  - [11. List all linux available usb ports](#11-list-all-linux-available-usb-ports)
  - [12. Create conceptual and graphical maps in linux](#12-create-conceptual-and-graphical-maps-in-linux)
  - [13. Ways to write console output to a file](#13-ways-to-write-console-output-to-a-file)
  - [14. Applications that run on linux startup](#14-applications-that-run-on-linux-startup)
  - [15. Running a shell script as a service](#15-running-a-shell-script-as-a-service)
  - [16. Run two systemd services with one timer](#16-run-two-systemd-services-with-one-timer)
  - [17 Run sudo programatically](#17-run-sudo-programatically)
  - [18. Connecting via SSH to a device](#18-connecting-via-ssh-to-a-device)
  - [19. Can't use sudo with my username.](#19-cant-use-sudo-with-my-username)
  - [20. Check disk space](#20-check-disk-space)
  - [21 Change user access in file](#21-change-user-access-in-file)
  - [22 Fill python input from command line](#22-fill-python-input-from-command-line)
  - [23 Disable linux system automatic updates](#23-disable-linux-system-automatic-updates)
  - [24 Run shell command from python](#24-run-shell-command-from-python)
  - [25 How to write a while True loop](#25-how-to-write-a-while-true-loop)
  - [26 Running python script from sheel with X cpus](#26-running-python-script-from-sheel-with-x-cpus)
  - [27 Run a python script from shell and give a user input](#27-run-a-python-script-from-shell-and-give-a-user-input)
  - [28 Check network usage of linux device](#28-check-network-usage-of-linux-device)
  - [29 Check which program has a certain PID](#29-check-which-program-has-a-certain-pid)
  - [30 Check last modified files and their size, in linux](#30-check-last-modified-files-and-their-size-in-linux)
    - [Recent updates](#recent-updates)
    - [Check all current running processes on linux](#check-all-current-running-processes-on-linux)
- [NEW GATEWAY INSTALLATION](#new-gateway-installation)
  - [1. Installing a Linux (ubuntu) OS](#1-installing-a-linux-ubuntu-os)
  - [2. Download github code](#2-download-github-code)
  - [3. Install](#3-install)
    - [1. Disable linux system from automatically updating:](#1-disable-linux-system-from-automatically-updating)
  - [4. *permission* and *file not found* errors](#4-permission-and-file-not-found-errors)
  - [5. Using Yocto](#5-using-yocto)
  - [6. Check the image of a company firmware](#6-check-the-image-of-a-company-firmware)
  - [7. Load a usb device from U-boot 2018.](#7-load-a-usb-device-from-u-boot-2018)
  - [8. Run ubunto from an SSD card instead:](#8-run-ubunto-from-an-ssd-card-instead)
  - [9. Github account to use in the new gateways:](#9-github-account-to-use-in-the-new-gateways)
  - [10. Create a `systemd` linux service to start the sink services](#10-create-a-systemd-linux-service-to-start-the-sink-services)
  - [11. Cap the logs of journalctl and syslog](#11-cap-the-logs-of-journalctl-and-syslog)
    - [Caping the journal logs](#caping-the-journal-logs)
    - [Delete the system logs](#delete-the-system-logs)
    - [Give user permissions to the logs](#give-user-permissions-to-the-logs)
  - [12. Setting a service to update code](#12-setting-a-service-to-update-code)
  - [13. Create a script to not update the logs on code update](#13-create-a-script-to-not-update-the-logs-on-code-update)
    - [During otap](#during-otap)
  - [14. Start the sink](#14-start-the-sink)
- [Entering the Cloud server](#entering-the-cloud-server)
  - [Stopping the cloud server firewall](#stopping-the-cloud-server-firewall)
- [Modifying gateway functionalities:](#modifying-gateway-functionalities)
  - [1. Adding a new message type for the cloud \<\> gateway interactions](#1-adding-a-new-message-type-for-the-cloud--gateway-interactions)
    - [1. Basic scripts to change:](#1-basic-scripts-to-change)
    - [2. Additional parts to change in the gw software:](#2-additional-parts-to-change-in-the-gw-software)



# TO DO in the code:

1. fix error in send dimming to all cloud > gateway (done)
2. Fix/create all create response functions in order to respond (done).
3. Consider error messages from the node (partially)
4. Create github account to use in gateways (done)
5. prepare automatic start of gateway on device reboot (doing..)
6. buy usb-usb cable (done)
7. Develop last functions (update software, send otaps, read electric parameters) (done)
8. develop all database functions.
9. Solve the intermitent error: *AttributeError: 'WirepasNetworkInterface' object has no attribute '_connected'* when sending a message from cloud to gateway. (origin of the problem found) (done)
10. Solve the Sink intermitent error: ** on sink restart or after a sink config update.
11. Start SolidRun from SSD card as the frenchmen advise.
12. Why the second node is not listening to cloud? The error is this function -> self.request_to_node() that uses gvars. Or, it is not. The issue is with the `global_server` chosen. If it is a local server all gwatewa-node messages form the cloud are received well. *The issue is when we use Alice's server*
13. Error *Fatal: Could not read Username for "https://github.com", No such device or address* when automating the git pull. check website > https://github.com/github/hub/issues/1644
14. Change the way a gateway starts listening to a cloud message to a node. Is it necessary to wait for a periodic message from a node? I think wirepas has a function that automatically detects a connected node. We could use this to update the _node list_ . I think this function could be the `get_sinks()` from wirepas `wni` python class.
15. Fix the otap last errors
16. Stop linux automatic updates of the system software
17. Make systemd gateway_update_code service execute every time the gateway reboots. 
18. Make a *secure* command or service, that is always listening and never updates itself, and that if receives a certain message, will upload all the gateway code except itself.
    
# TO DO in general:

1. Choose a time-interval to download the github code (more than 3 min)
2. Choose a time interval to restart the *listen to nodes.py* gateway service (maybe together with the gateway code update?)
3. I could document the code done up to now. In particular, I should document:
   1. How to set up the 2 services and the 1 timer in the new gateway using `systemd`
   2. How to create local *system user* called **salvi-smartec** and *password* which will be **admin** for properly running all the files
   3. How to set up the github username and password using the *credential.helper* so that git can automatically pull global changes and erase any local ones.
4. Set the small and light *SolidRun* gateway for direct communications from *node* to *cloud* without using a local *MQTT broker* and just use the *global MQTT broker* directly.
5. Put the gateway logs outside of the *gateway-services* folder, because after each github code update, they get erased by the github logs, which are emtpy.
6. Check why the logs of `gateway_services_logs_2.log` don't get trimmed. I believe it is because it is set as the output file for the gateway services, service.
7. Book a place at lazertag.

## 7. Tests to check robustness of otap:

    1. unplug power from gateway while it's downloading *github* code.
    2. unplug power from gateway when performing otap in any of its steps:
        - set no otap to all sinks
        - upload new scratchpad to the sinks
        - process and propagate the scratchpad to all nodes and sinks
    3. lose internet connection during:
        - otap process
        - github download code
    4. Connect a different node, well after all the OTAP process has finished. A node with another stack. This is to check whether the sink will indeed override the old program of the node and write the new scratchpad to it even if OTAP process has formally finished a few minutes ago.

## 8. Add OTAP and gw software versions

1. When a cloud request is received, the gateway shoud start updating either software and answer: "updating software"
2. For the cloud to know which version the gw is using, we should create a command called **gw_status** that gives the gateway version with format *mar.min.rev.build* as specified below.
3. Add *node version number* to *node status list* so that the cloud can query the version number as well. This should be done by the hardware technician, alvaro.

- The format should be: *major_release.minor_release.revision_fixes.build_number*

## 9. Organize all the documentation again:
1. Document all the code properly and apply any necessay changes to make things work better
2. Rewrite all the documentation files in a neat and ordered way. We can use this webpage > https://www.pdfforge.org/online/en/markdown-to-pdf or this one https://md2pdf.netlify.app/ or this one https://s25.aconvert.com/convert/p3r68-cdx67/07exw-wsyd7.pdf in order to convert markdown documents into pdf files.
3. Maybe unify all documentation into one single file?

# I WAS LAST DOING:

1. fixing all the prepare_response thingies (80% done)
2. Getting gateway requests to cloud delivered. Created the file *prepare_request.py* but I didn't finish it, it gives an error. as of March 1st 2023
3. Checking how to update nodes via OTAP (wirepas) as of 1st March 2023.
4. checking this > https://developer.wirepas.com/support/solutions/articles/77000498371-how-to-perform-otap-with-wirepas-massive-v5-1#References > What is Network Persistent Data and what are the benefits?
5. Editing the file **README_otap_config.md** and writing down the last descoveries on how to change sink configuration usign python scripts sent by gateway. 
6. Changing the gw id and sink id and node id to the main script. (done)
7. updating the command 10 of the `otap_manu.py` (done)
8. Trying to update a scratchpad and failing (done)
9. Node 31415 doesn't respond to gateway messages, we don't know why. We leave this issue. (solved, it was an issue with the Cloud MQTT server, not the gateway) (solved - another fake cloud subscribed was subscribed with same sub name to the global MQTT and the broker didn't allow a seconds subscriber with the same name)
10. Use the `checksum` of python to compute the CRC in an easier way. (done) 
11. Why when parsing fails on cloud - >gw messages, no error response is given back to the cloud?? fixing this, checking files mqtt_cloud_inter, prepare_response.py, I encountered this wen trying messges cloud > gw type 7. (fixed)
12. Sending node version to cloud from gateway upon request... changed the place where it is done in the gw from read db to node tunnel and now it doesn't work anymore.. :( (done)
13. Now the gateway cant automatically start listenning to cloud > gw messages, it doens't work. I suspect it is because in `start_listen_to_cloud.py` file, we create an additional wni interface, that might create conflicts with the wni interface already created in file `start_listen_to_nodes.py`.

28.04.2023 - Hmm, interesting. Now I created a single WNI to check if that was the issue, and I keep facing the same problem. However, when the gateway services restart and the sink tries to detect the nodes via otap, I do see a failed atempt with [] nodes detected, before the gateway becomes unresponsive to the cloud. Maybe the issue is that we call the "gateway listen to cloud" funciton AFTER the "gateway listen to nodes" script. What if we reverse this order?

Or maybe the issue is that both gatewy functionalities run on the same python and shell script. Maybe I should make 2 python scripts, and run them separetly in two different shell commands, so they don't affect each other. > Did this already, not working properly, somehow the two wnis seems to be influencing each other. 

Let's go back to the original idea, let's have both listen to cloud and listen to nodes in the same script, and let's start by runing listen to cloud, wait 2 seconds so that the gateway has time to get its id, and then let's run the listen to nodes with its wni. I think this actually doesn't work at all for some unknown reason.

14. Solved almost everything, now making sure evertying runs ok again.

# LAST DISCOVERIES:

   ## 1. (08-02-23) If I have a primitive class and extend it. 
   I can define a method on the extended class and call it in the primitive class.
   ## 2. (08-02-23) Dont duplicate code 
   In "create response" and the "reception of the node message" I check two times the message type, and 
                with one time is enough.
   ## 3. "not connect found" error
   For the  wirepass "not connect found" error, maybe it is because I dont close the old connection! when there is a tunneling from gw to node! The subscriber name repeats. Maybe the issue is that gateway listen to nodes, and gateway listen to cloud executes on same terminal? and tehre could be subscriber or publish names that are repeacted? hence the connection error?

   ## 4. Error  *AttributeError: 'WirepasNetworkInterface' object has no attribute '_connected'*
   Cause of the error:  *AttributeError: 'WirepasNetworkInterface' object has no attribute '_connected'* when sending a message from cloud to gateway:
   - The issue is that a second WirepasNetworkInterface() connection is created, while a previous one still exists in the same script or terminal or process. This creates a problem, only one wni is allowed. Problem solved by passing the wni class to the sub itneraction classes that are created programatically, so that only 1 class is used per terminal or execution.
   ## 5. Error *Message sending failed: res=GatewayResultCode.GW_RES_SINK_OUT_OF_MEMORY*
   23rd of March: I found this error this morning when I opened my computer: *Message sending failed: res=GatewayResultCode.GW_RES_SINK_OUT_OF_MEMORY. Caller param is None* on the terminal that was executing the `start_listen_nodes.py`

   ## 6. SolidRun jumpers (under the motherboard)
   They are:
   1. USB OTG
   2. SATA
   3. eMMC
   4. MicroSD

   ## 7. Many Subacks on cloud mqtt

    *Solved on 4 april 2023*

    I observe an subreq every 1 second to the cloud MQTT broker. This is not good. In particular, I see the following error inside the mosquitto MQTT server logs:
```
1680595990: New connection from 79.152.78.3:51997 on port 1883.
1680595990: Client gw-res/n/31415--> subscriber already connected, closing old connection.
1680595990: New client connected from 79.152.78.3:51997 as gw-res/n/31415--> subscriber (p2, c1, k60).
1680595990: No will message specified.
1680595990: Sending CONNACK to gw-res/n/31415--> subscriber (0, 0)
```
Possible reasons:
   1. The MQTT subscribed client (my python mqtt client) has not recieved the *CONNACK* and sends a new one, continuously.

Solution:
1. In the way I programed the subscriptors and publishers, each pub or sub client gave a custom *client_id*. As a matter of fact the client ID was always of this form *gw-res/n/<node_id> --> subscriber* where *<node_id>* could be any node id number. Thus, I forgot three sessions open on my PC, that used this client id for nodes 3, 40002 and 31415, and the MQTT global broker didn't allow anyone else to subscribe using the same client id. Therefore there are two possible solutions to this problem
   1. Leave client_id empty, so the MQTT broker randomly generates a valid value. <- We are using this setting
   2. Ensure that you have a way to uniquely generate a client_id, so that no two equal client_ids are ever generated. This would pose a conflict. 


## 8. Doing otap: Scratchpad stored status has error 4

Full error log:
```
transport-service | wirepas_gateway@sink_manager.py:337:Scratchpad stored status has error: 4
```

# LEARNED THINGS:

## 1. How to document the code
In order to run the documentation strings, read the *README_generate_code_documentation.md*
## 2. List of wirepas mqtt topics
https://github.com/wirepas/backend-apis/tree/master/gateway_to_backend#list-of-all-mqtt-topics
## 3. Subscribe to mosquitto topic:
```
mosquitto_sub -h 127.0.0.1 -p 1883 -u "roma_masana" -P "all_I_want_for_christmas_is_you" -t gw-response/send_data/193853683731279/sink0

global_user="roma_masana"
global_password="all_I_want_for_christmas_is_you"
```
## 4. Find strings in linux directories. 
You can either use:
   
   `find name .`

   or

   `grep -rn "word" *`

## 5. Count the number of lines 
in code in all files within a directory:

    `find . -name '*.php' | xargs wc -l`

## 6. Get the gateway id
In order to get the gateway id check this tutorial: https://github.com/wirepas/wirepas-mqtt-library
In particular, run this command:

`wni.get_gateways()`

And you will get a list with all of them.

## 7. Change sink configuration
We can change all sink configuration using the *examples* folder scripts, within the *wirepas-mqtt-library* as documented in the file **README_otap_config.md**

## 8. Installing gateway **S-CONNECT** with ubuntu 22.01, 
- usuario: **salvi**
- contrasenya: **admin** 

 OS system created in MMC/SD card.

## 9. Using Git

### 0 Starting a local github repo

Type `git init .` to start a local repo on the current directory.

After that you should clone your remote repot to the local folder like so:

```
git clone https://github.com/smartec-lighting/gateway-services-production.git
```

### 1 Commiting and pushing to remote repo

Please use the shell script `/home/$user/smartec/gateway-services/commit_and_push_to_github.sh` in order to properly push the changes to the remote repo.

In particular, note that you can use the global variable `GATEWAY_VERSION` placed in the script `single_transport/backend/global_vars.py` in order to keep track of the version of the gateway software. A change in the value of this variable will force the *shell* script to automatically create a realse of the code and ask for a description of it to the user that is pushing to the remote repo.

### 2 Storing git credentials in pc
check: > https://unix.stackexchange.com/questions/379272/storing-username-and-password-in-git

Basically we need to:

1. Set up a token on your own github account with just *repo* privileges (the least).

2. Run this command to tell git to remember your credentials:

```
git config --global credential.helper store
```

3. run these commands to enter your credentials:

```
git config --global user.name 'your user name'
git config --global user.password 'the_github_token'
git config --global user.token 'the_github_token'
```
The token we created for all the gateway software created by smartec is:
```
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
```

4. Do a *pull* or clone a github private repo, or any other action that requires authentication. Once you authenticate once, the password will be kept

### 3 Pull git changes and overwrite local modifications
In order to download from git the new commits someone did to a repo, and overwrite the local changes (a gateway) might have done, you can execute the following code:
```
git fetch --all
git reset --hard HEAD
git merge origin
```
or alternativeley, run:
```
git fetch --all
git reset --hard origin
```

after that you can do the
```
git pull
```
and you will download automatically the whole repo and overwrite local changes.

### 4 Adding tags to github
This is a way to produce releases in the code in Github. It is done via tagging the local commits and pushing them to the remote repo.  Here is a link that explains how it works -> https://stackoverflow.com/questions/35221147/what-is-the-sequence-for-tagging-commit-in-git 
In short, you should do the following steps:
```
git add .
git commit -m "$message"
git push
git tag -a $version -m "version $version is released!"
git push origin --tags
```
and this will push all the last changes, and then create a tag and push the tags to the remote server in order to upload the last changes, and "label" them to remember this milestone in the future.

Remember this: *Git traffics in commits. A commit is a thing. Everything else is just information about those commits.
A tag refers to a commit. Saying checkout a tag checks out a commit. Saying push a tag pushes a commit.*

### 5 Creating a github release

You can check out how to do this in this page > https://stackoverflow.com/questions/21214562/how-to-release-versions-on-github-through-the-command-line 

In particular, you can use the following command:

```
gh release create <tag> -t <release title, usually the tag itself> -p -n <release notes>
```

where `-p` is a tag to mark it as a pre-release. This should be done after creating an *annotated github tag*. 

### 6 Cleaning the .git folder

Locally, the `.git` folder might take a lot of space. To get rid of unnecessary files, read this guide > https://stackoverflow.com/questions/5613345/how-to-shrink-the-git-folder or run the following commands:

```
rm -rf .git/refs/original/

git reflog expire --expire=now --all

git gc --prune=now

git gc --aggressive --prune=now
```

and this might do the trick.

### 7 Link your local repo to a new remote repo

If you want to change the remote repo in your local repo (either you want to push or pull from a different remote repo) I recommend you read this first > https://stackoverflow.com/questions/5181845/git-push-existing-repo-to-a-new-and-different-remote-repo-server

Basically the commands to follow are these:

1- Delete all connection with the remote repository: Inside the project folder:

    git rm .git (Remove all data from local repository)
    git status (I must say that it is not linked to any, something like an error)

2- Link to a new remote repository

    git init To start a local repository
    git remote add origin urlrepository.git To link with remote repository
    git remote -v To confirm that it is linked to the remote repository

3- Add changes to the local repository and push to the remote repository

    git pull or git pull origin master --allow-unrelated-histories if git history is different in both local and remote repo.
    git add.
    git commit -m" Message "
    git push -u origin master


### 8 Remote SSH keys for gateway control

For the account *SmartGWay*. Using this user's email, and the paraphrase: *javijavi23*

## 11. List all linux available usb ports
 Use `sudo setserial -g /dev/tty* ` to list, in linux, all available ports for usb devices and their address.
## 12. Create conceptual and graphical maps in linux
 Use **Xmind** for making conceptual maps
## 13. Ways to write console output to a file
 How to write command output to a file, and not to the terminal > https://askubuntu.com/questions/420981/how-do-i-save-terminal-output-to-a-file Basicall you have to use the `&>` or `&>>`, synthax like in this example:
    ```
    mosquitto -c conf.file -v &>> logs_mosquitto.out
    ```
    The `>>` appends text to the output file, the `>` symbol deletes all previously stored information.

## 14. Applications that run on linux startup
 Check all applications that will be started on start up in linux > `ls /etc/init.d`

## 15. Running a shell script as a service
read this https://timleland.com/how-to-run-a-linux-program-on-startup/

In order to check the full logs of the service, run 
```
journalctl -u service-name.service | cat
```

In order to run a service execute:
1. to edit the service configuration and running initial script
```
sudo nano /etc/systemd/system/YOUR_SERVICE_NAME.service
``` 
In the file that opens, write something like this (modified up to your taste)
```

[Unit]
Description="Smartec gateway services."

Wants=network.target
After=network-online.target

[Service]
Type=simple
ExecStart=/home/roma/smartec/gateway-services/single_transport/backend/MY_SERVICE_SCRIPT.sh
Restart=on-failure
RestartSec=60
KillMode=control-group
User=roma
StandardOutput=append:/home/user/log1.log
StandardError=append:/home/user/log2.log

[Install]
WantedBy=multi-user.target
```

2. The file `MY_SERVICE_SCRIPT.sh` contains the *shell commands* to run. These commands are actually *the service* you want to run.


3. This service file, in particular the lines of the *standard output and error* will only work for linux systems of version 20.04 onwards. The lines
```
StandardOutput=append:/home/user/log1.log
StandardError=append:/home/user/log2.log
```
Redirect the output of the service to these two log files, respectively. Note that you don't need to create these two files *before* starting the service. The `append` command will create them if not exist already.

4. Change the owner of the log files that this service creates, to the local user `salvi-smartec` by running the following command in the right directory:
```
chown salvi-smartec logs/gateway_services_logs.*
```
Now the files `gateway_services_logs.*` will be owned by the user *salvi-smartec* and our shell scripts of *trimming logs* will be able to run without problem. 

5. In order to reload the services you should execute
```
sudo systemctl daemon-reload
```
6. Now enable the service by running on a terminal:
```
sudo systemctl enable SERVICE-NAME
```
7. After that you can tart the service by running:
```
sudo systemctl start SERVICE_NAME
```
8. Finally, you can check the status of the service anytime to see if it is running by writing:
```
sudo systemctl status SERVICE_NAME
```
9. If you should ever need, you can always stop the service with the following command:
```
sudo systemctl stop SERVICE_NAME
```

10. In my case I observed the error upon checking *service status* that *paho module not found, in python*. I don't know why this happens, but crontab for python scripts may file because other services need to be started before. try reboot with a sleep:
```
@reboot sleep 15; python3 /home/pi/init_server.py && python3 /home/pi/scheduler.py >> /home/pi/mycronlog.txt 2>&1
```

## 16. Run two systemd services with one timer
Check this webpage > https://serverfault.com/questions/776437/how-do-you-configure-multiple-systemd-services-to-use-one-timer

## 17 Run sudo programatically
If we create a *.sh* script that invokes the `sudo` command, it will ask for the password. If this command is 
run withhin a shell script, we cannot type it in. This is why we should run it in this way:
```
echo _password_ | sudo -S _command_
```

## 18. Connecting via SSH to a device 

1. Connect to a machine that is NOT a PC, by:
    1. Find the device IP. For that, connect the device via ethernet cable to a routher. Then scann all IP's in the network and ports 80 and 443 to see which ones are open. To scan the IP's of the network you can use the software *Angry IP scanner* and sort by *port* to see which IP's have port 443 open. > https://angryip.org/download/#linux . Once you find the right IP adress, and port, you can either:
       1.  Browse to the found ip and port. 
       2.  Otherwise, ssh into it by running: `ssh root@ip-address`. Once inside the ssh, all will be clear.

## 19. Can't use sudo with my username.
If you find the following error: ** this webpage explains how to solve it > https://www.tecmint.com/fix-user-is-not-in-the-sudoers-file-the-incident-will-be-reported-ubuntu/ Basicall you have to:
1. Enter the startup option *ubuntu* for advanced options Grub menu by pressing *shift* on boot.
2. Go to *recovery mode* and press *enter* for *maintenance*.
3. Add the *LOCAL_USER* to the *sudo* group by running
```
mount -o rw,remount /
adduser LOCAL_USER sudo
adduser LOCAL_USER admin
exit
```
and start the normal boot sequence.

## 20. Check disk space

In order to check the disk space in a Ubuntu server, you can run the following general command:
```
df -h
```
this will list the main directories and devices and their used space, and their available space.

Once you detect form this command, which is the directory you are interested in studing in more detail, you can run now
the following command:
```
du -h / | grep '^\s*[0-9\.]\+G'
```
In this example, the script will return with any files bigger than 1 GB. If you want to single out 1 MB+ data, you can replace G with M.
In my case I see *30GB* are used in the directory `/var/log` which contain the system logs.

## 21 Change user access in file
In order to change the owner in a linux file, you can run this command:
```
chown user file.ext
```
Now the file `file.ext` will be owned by the user *user*.

## 22 Fill python input from command line
If you have an `input("input a value")` command in your python script, you can automatically send a value to it by running
```
printf "12" | python3 script.py
```
If you have more than one such input in your script, then run
```
printf "12\n23" | python3 script.py
```
and you will send a "12" for the first input, and a "13" for the second one.

## 23 Disable linux system automatic updates

Read > https://linuxconfig.org/disable-automatic-updates-on-ubuntu-20-04-focal-fossa-linux in order to do so.

Basically run:

```
sudoedit /etc/apt/apt.conf.d/20auto-upgrades
```
and change these two lines:

```
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```

For these four:

```
APT::Periodic::Update-Package-Lists "0";
APT::Periodic::Download-Upgradeable-Packages "0";
APT::Periodic::AutocleanInterval "0";
APT::Periodic::Unattended-Upgrade "0";
```

If you have to edit this file remotely, because you dont physically have the gateway and can only connect throught the MQTT bridge, then run this:

```
file=/etc/apt/apt.conf.d/20auto-upgrades; line=$(grep "Unattended" $file -n | cut -d : -f 1); echo admin | sudo -S sed -i $line's/.*/APT::Periodic::Unattended-Upgrade "0";/' $file
```

## 24 Run shell command from python

I advise to use the `subprocess.run()` command as described here > https://docs.python.org/3/library/subprocess.html instead of `os.system()` which gave some trouble.

In particular I used 

```
subprocess.run(["<shell command>"], shell=True, check=True)
```

## 25 How to write a while True loop

Do NOT write a while True loop like so:

```
while True:
  pass
```
This will make the computer call the loop as fast as it can, therefore depleting all its resources.
Instead put a small sleep inside like so:

```
while True:
  # ...code...
  time.sleep(0.1)
```
This will limit the computer to just call the loop each 100ms the most frequent, so the computer will have time and resources to do other things.

## 26 Running python script from sheel with X cpus

Run this

```
taskset --cpu-list 0-3 <app>
```

in order to run an app with only using cpus 0 to 3. Found it here > https://stackoverflow.com/questions/55746872/how-to-limit-number-of-cpus-used-by-a-python-script-w-o-terminal-or-multiproces

Check the cpu usage of a linux machine running the following command:

```
lscpu
```

## 27 Run a python script from shell and give a user input

You can give an automatic user input with the `echo` command like so:

```
echo "5\n78" | python3 script.py
```

This will issue first the number "5" when the `script.py` calls for a user input, and then the shell will give the number 78, when the script calls for the second input.

## 28 Check network usage of linux device

You can check the network usage of the different PIDs or services running in a linux device by running the following command:

```
sudo nethogs -v 3
```
This will show you cummulative usage of bandiwth, by process. In order to just see instantaneous bandwith usage, run:

```
sudo nethogs
```


You have many more different apps to check the network traffic in this webpage > https://www.binarytides.com/linux-commands-monitor-network/

## 29 Check which program has a certain PID

If you want to know which script is related to a specific PID, just run

```
ps -p <PID number> -f
```

## 30 Check last modified files and their size, in linux

Run this command:

```
find /home -type f -printf "%T@ %s %p\n" | sort -n | tail -n 100 | awk '{print $2,$3}' | xargs ls -lh
``` 
or

```
find /home -printf "%T@ %s %p\n" | sort -n | tail -n 1000 | awk '{print $2,$3}' | xargs ls -lh
```
Run this to see the last modified files in the system:


```
find / -type f -printf "%TY-%Tm-%Td %TT %p\n" 2>/dev/null | sort -r | head -n 100 | cut -d ' ' -f 3- | xargs ls -lh
```

List all files that had a change of more than 500K in the last day:

```
find /home -type f -size +15k -mtime -1 -exec ls -lh {} \;
find /home -type f -size +15k -mtime -2 -exec ls -lh {} \; # last 2 days
find /home -type f -size +4k -mtime -3 -exec ls -lh {} \; # last 3 days
```

Alternative:
```
find /home -type f -mtime -1 -exec du -h {} + | awk '$1 > "400K" {print}'
```

Get files modified in the last 5 minutes:

```
find / -mmin -5 -ls
```

within last hour:

```
find / -mmin -60 -ls
```

The last 2 days modified files with a size of more then 15k:

-rw-r--r-- 1 salvi-smartec salvi-smartec 21K jun 12 12:01 /home/salvi-smartec/smartec/gateway-services/single_transport/backend/__pycache__/mqtt_interaction_module.cpython-310.pyc
-rw-r--r-- 1 salvi-smartec salvi-smartec 19K jun 12 12:01 /home/salvi-smartec/smartec/gateway-services/single_transport/backend/__pycache__/global_vars.cpython-310.pyc
-rw-r--r-- 1 salvi-smartec salvi-smartec 17K jun 12 12:01 /home/salvi-smartec/smartec/gateway-services/single_transport/backend/__pycache__/mqtt_interaction_node_basic.cpython-310.pyc
-rw-r--r-- 1 salvi-smartec salvi-smartec 17K jun 12 12:01 /home/salvi-smartec/smartec/gateway-services/single_transport/backend/__pycache__/message_display_specific_functions.cpython-310.pyc
-rw-r--r-- 1 salvi-smartec salvi-smartec 24K jun 12 12:01 /home/salvi-smartec/smartec/gateway-services/single_transport/backend/__pycache__/message_specific_parse_functions.cpython-310.pyc
-rw-r--r-- 1 salvi-smartec salvi-smartec 16K jun 12 12:01 /home/salvi-smartec/smartec/gateway-services/single_transport/backend/__pycache__/mqtt_interaction_cloud.cpython-310.pyc
-rw-r--r-- 1 salvi-smartec salvi-smartec 16K jun 12 12:01 /home/salvi-smartec/smartec/gateway-services/single_transport/backend/__pycache__/message_received_parse_functions.cpython-310.pyc
-rw-r--r-- 1 salvi-smartec salvi-smartec 23K jun 12 12:01 /home/salvi-smartec/smartec/gateway-services/single_transport/backend/__pycache__/message_received_class.cpython-310.pyc
-rwxrwxrwx 1 root root 66K jun 12 15:07 /home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/gateway_services_logs_2.log
-rwxrwxrwx 1 salvi-smartec salvi-smartec 69K jun 12 15:07 /home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/logs_sink_service.out
-rwxrwxrwx 1 salvi-smartec salvi-smartec 25K jun 12 15:07 /home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/logs_mosquitto_server.out
-rwxrwxrwx 1 salvi-smartec salvi-smartec 245K jun 12 15:07 /home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/logs_gateway_backend.out
-rw-r--r-- 1 salvi-smartec salvi-smartec 59K jun 12 12:00 /home/salvi-smartec/smartec/gateway-services/.git/index
-rw-r--r-- 1 salvi-smartec salvi-smartec 32K jun 12 12:33 /home/salvi-smartec/.cache/tracker3/files/http%3A%2F%2Ftracker.api.gnome.org%2Fontology%2Fv3%2Ftracker%23Audio.db-shm
-rw-r--r-- 1 salvi-smartec salvi-smartec 33K jun 12 12:33 /home/salvi-smartec/.cache/tracker3/files/http%3A%2F%2Ftracker.api.gnome.org%2Fontology%2Fv3%2Ftracker%23Pictures.db-wal
-rw-r--r-- 1 salvi-smartec salvi-smartec 32K jun 12 12:33 /home/salvi-smartec/.cache/tracker3/files/http%3A%2F%2Ftracker.api.gnome.org%2Fontology%2Fv3%2Ftracker%23Pictures.db-shm
-rw-r--r-- 1 salvi-smartec salvi-smartec 821K jun 12 12:33 /home/salvi-smartec/.cache/tracker3/files/http%3A%2F%2Ftracker.api.gnome.org%2Fontology%2Fv3%2Ftracker%23FileSystem.db-wal
-rw-r--r-- 1 salvi-smartec salvi-smartec 32K jun 12 12:32 /home/salvi-smartec/.cache/tracker3/files/meta.db-shm
-rw-r--r-- 1 salvi-smartec salvi-smartec 435K jun 12 12:33 /home/salvi-smartec/.cache/tracker3/files/http%3A%2F%2Ftracker.api.gnome.org%2Fontology%2Fv3%2Ftracker%23Software.db-wal
-rw-r--r-- 1 salvi-smartec salvi-smartec 32K jun 12 12:33 /home/salvi-smartec/.cache/tracker3/files/http%3A%2F%2Ftracker.api.gnome.org%2Fontology%2Fv3%2Ftracker%23Video.db-shm
-rw-r--r-- 1 salvi-smartec salvi-smartec 32K jun 12 12:33 /home/salvi-smartec/.cache/tracker3/files/http%3A%2F%2Ftracker.api.gnome.org%2Fontology%2Fv3%2Ftracker%23FileSystem.db-shm
-rw-r--r-- 1 salvi-smartec salvi-smartec 33K jun 12 12:33 /home/salvi-smartec/.cache/tracker3/files/http%3A%2F%2Ftracker.api.gnome.org%2Fontology%2Fv3%2Ftracker%23Video.db-wal
-rw-r--r-- 1 salvi-smartec salvi-smartec 33K jun 12 12:33 /home/salvi-smartec/.cache/tracker3/files/http%3A%2F%2Ftracker.api.gnome.org%2Fontology%2Fv3%2Ftracker%23Audio.db-wal
-rw-r--r-- 1 salvi-smartec salvi-smartec 32K jun 12 12:33 /home/salvi-smartec/.cache/tracker3/files/http%3A%2F%2Ftracker.api.gnome.org%2Fontology%2Fv3%2Ftracker%23Documents.db-shm
-rw-r--r-- 1 salvi-smartec salvi-smartec 32K jun 12 12:33 /home/salvi-smartec/.cache/tracker3/files/http%3A%2F%2Ftracker.api.gnome.org%2Fontology%2Fv3%2Ftracker%23Software.db-shm
-rw-r--r-- 1 salvi-smartec salvi-smartec 411K jun 12 12:33 /home/salvi-smartec/.cache/tracker3/files/http%3A%2F%2Ftracker.api.gnome.org%2Fontology%2Fv3%2Ftracker%23Documents.db-wal
-rw-rw-r-- 1 salvi-smartec salvi-smartec 32K jun 12 12:34 /home/salvi-smartec/.local/share/gvfs-metadata/root-944ca5cd.log
-rw-r--r-- 1 salvi-smartec salvi-smartec 84K jun 12 12:32 /home/salvi-smartec/.local/share/evolution/addressbook/system/contacts.db




In general, to investigate the discrepancy between the reported SIM card consumption and the package manager logs, you may need to explore other avenues. Here are a few suggestions:

    - Check application-specific logs: Some applications, such as web browsers, download managers, or file-sharing tools, maintain their own logs. Reviewing these logs might provide insights into the downloads that occurred.

    - Network traffic monitoring: Consider examining network traffic logs or using network monitoring tools to track data transfers and identify which applications or processes might be responsible for the downloads.

    - File system analysis: Conduct a thorough examination of the file system to identify recently modified or downloaded files. The find command can be helpful here, such as find / -type f -mtime -1 to list files modified in the last day.

### Recent updates

To view the system logs related to package installations and updates, you can use the following command:


```
cat /var/log/dpkg.log | grep "status installed"
```

### Check all current running processes on linux

Well, you can see everything that's running on your system by running (in a terminal window) the command 

```
sudo pstree -a
```

# NEW GATEWAY INSTALLATION

**Estimated time to complete installation**: I started at **9:40am** and finished at **15:55** in order to install all the gateway software
0. Started the machine and configured the basic settings in Windows in order to reboot from a usb (15min)
1. Linux OSystem: (20min)
2. Disable automatic updates of software (3min)
3. Install basic software and python packages for running gateway (10min):
   1. basic linux apps and pip packages (3min)
   2. mosquitto configuration files (5min)
4. Clone the Github repo, enter the valid credentials and download all the code (30min)
   1. create a directory called `smartec` under `/home/salvi-smartec`
   2. clone the Github repository using 
    ```
    git clone https://github.com/smartec-lighting/gateway-services.git
    ```
5. Install linux systemd services, enable them, and run `sudo systemctl daemon-reload` to save the changes.
6. Reboot the computer in order to start the upload code gateway service

Steps to follow:

In general, install:
   - sudo apt install git
   - sudo apt install docker-compose
   - sudo apt install mosquitto
   - sudo apt install mosquitto-clients
   - sudo apt install python3-pip
   - pip3 install numpy
   - pip3 install wirepas-mqtt-library==1.0
   - pip3 install paho-mqtt python-etcd
   - pip3 install getmac crc

## 1. Installing a Linux (ubuntu) OS

I am using Linux Ubuntu 22.10. In particular:

1. During linux Installation I select *minimal installation*
2. I Select **Do not update or download any updates after installation** to make sure all gateways have the same OS version.
3. I chose delete hardisk, and install Ubuntu in order to earase any other OS.
4. Do not choose any advanced option, a LVS volume manager or a ZFS filesystem won't be as fast as the default EXT4 filesystem which is what we want installed.
5. Press *Continue* and *Install* Linux.
6. select the following username and password:
   1. user: *salvi-smartec*
   2. password: *admin
7. Choose **start session automatically** in order to avoid asking for the password.

## 2. Download github code 
from https://github.com/smartec-lighting/gateway-services
## 3. Install
- docker
- docker-compose

### 1. Disable linux system from automatically updating:

Basically run:

```
sudoedit /etc/apt/apt.conf.d/20auto-upgrades
```
and change these two lines:

```
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```

For these four:

```
APT::Periodic::Update-Package-Lists "0";
APT::Periodic::Download-Upgradeable-Packages "0";
APT::Periodic::AutocleanInterval "0";
APT::Periodic::Unattended-Upgrade "1";
```

Also disable the **session logout** after a few minutes. ? Not necessary



## 4. *permission* and *file not found* errors 
When running `docker-compose up` command you will encounter *permission* and *file not found* errors. To fix, them, do the following:
1. I think that while installing docker some permission errors regarding the sockets may be encountered. For that it is maybe necessary to create a Unix group called “docker” as described here: https://docs.docker.com/engine/install/linux-postinstall/. You have to basically 1. create a Unix group called “docker” 2. add the root user to it. IF you sill get the permission error run the following commands: 

    ```
    sudo groupadd docker
    sudo gpasswd -a $USER docker 	<-- adding the user to the docker group 
    newgrp docker  		      <--updating the group 
    sudo su $USER			   <-- give more permissions to the root user    	 
    ```

2. If you get an “No such file or directory”, check the docker service is running, that's to say run the following command: `sudo systemctl start docker`, or better, run docker using:
    ```
    sudo dockerd
    ```
    You can tell docker to start on boot by default by running the command 
    ```
    sudo systemctl enable docker 
    ```

3. After this you should be able to run “docker-compose up” without any permission or file not found errors. 

4. Now we should install the local mqtt broker as described on teams.
    1. Follow teams file "seting up a wirepas gateway"
    2. set up a `/etc/mosquitto/conf.d/default.conf` file with the info:
        ```
        listener 1883 
        allow_anonymous true 
        ```
    3. **note**: if you don't have permissions to edit this file, make your user own it by:
        Check which user you are using:
        ```
        whoami
        ```

        Then make your user own the folder:
        ```
        sudo chown -R "user" path/to/dir
        ```
    4. Finally, start the mosquitto server with:
        ```
        mosquitto -c /etc/mosquitto/conf.d/default.conf -v
        ```

5. Set username and password to your local mqtt moquitto broker as explained here: http://www.steves-internet-guide.com/mqtt-username-password-example/
    1. Basically, set a password file `contra.txt` with this content:
        ```
        username:password
        ```
    2. Run the encryption command
        ```
        mosquitto_passw -U contra.txt
        ```
    3. Modify the `/etc/mosquitto/conf.d/default.conf` configuration mosquitto file to be this one:
        ```
        listener 1883
        password_file /etc/mosquitto/conf.d/passwd_file 
        ```


6. Try tu re-run your `docker-compose up` if it was missign the mosquitto broker.
7. Install all python dependencies:
    1. install pip: 
    ```
    sudo apt install python3-pip
    ```

   ## 5. Using Yocto 
You might try to use Yocto in a device (gateway) given by a company:
8. Install `apt-get` on deby yocto, (which doesn't have `yum` nor `apt-get` inside) follow: https://askubuntu.com/questions/860375/installing-apt-get
9. Connect to a machine that is NOT a PC, by:
    1.  find the device IP. For that, connect the device via ethernet cable to a routher. Then scann all IP's in the network and ports 80 and 443 to see which ones are open. To scan the IP's of the network you can use the software *Angry IP scanner* and sort by *port* to see which IP's have port 443 open. > https://angryip.org/download/#linux 
    2.  Browse to the found ip and port, then enter the *username*:**admin** with *password*: **admin**, you should access the *KURA* portal. 
    3.  Otherwise, ssh into it by running: `ssh root@ip-address`. Once inside the ssh, all will be clear.
    4.  In order to accesss the **Solidrun** device using ssh, enter the password: *aiPh2eim*. The device name should be *BS4444*.

10. Find the "build" folder within a linux distribution. 
    1.  Run the command 
    
    ```
    find / -name build
    ```
    This will tell us where it is.
    2. Once there, I found `build@` but not `build`. This is like a shortcut, to see where it points to, you can run `ls -l`. Then I saw it was pointing to another directory.

11. For running the full funcitoning gateway on a device, we need to install:
    1.  Git
    2.  mosquitto
    3.  python3
    4.  pip3 (for installing new python packages)
    5.  docker (*not needed, if sink services already installed*)
    6.  docker-compose (*not needed, if sink services already installed*)
  
## 6. Check the image of a company firmware 
Installed on a device. Run the command:
```
mender show-artifact
```

## 7. Load a usb device from U-boot 2018. 

1.  We have to locate the filesystem files that boot the OS, in case of Ubuntu they are :
```
EFI/boot/bootx64.efi grubx64.efi mmx64.efi loadaddr 0x12000000
```
2.  In order to see all the environment variables in a device gateway, run the following command:

```
print env
```

3.  Actually what we have to solve in order to start the OS from an external USB device connected via a port to the gateway, is the following situation: "que imagen de linux tendría que flashear en un usb, para que pueda ejecutar los comandos **load** y **bootm** o **bootefi** en el uboot 2018 del gateway, con el usb conectado en un puerto físico? El dispositivo es un gateway USB **OTG - i.MX6de solidrun/solidsense**, y ahora mismo al intentar iniciar desde el usb me da estos dos errores: 1.*warning: invalid device tree, expect boot to fail* 2. *efi_load_pe: invalid optional header magic 20b suggests that the EFI binary file EFI/boot/bootx64.efi*. 
ChatGPT dice:
4.  Buscar un OS compatible con *i.MX6* in order to do this > https://solidrun.atlassian.net/wiki/spaces/developer/pages/321519617/Boot+from+USB+OTG+-+i.MX6 .
5.  Could this version of Yocto work? > https://docs.yoctoproject.org/ref-manual/system-requirements.html#required-git-tar-python-make-and-gcc-versions
   
   ## 8. Run ubunto from an SSD card instead:
1.  create an SD CARD SolidSense with this image  https://solid-run-images.sos-de-fra-1.exo.io/IMX6/Debian/sr-imx6-debian-bullseye-20220712-cli-sdhc.img.xz by using balenaEtcher or windisk32 or “dd”.

2.  Then change the jumper to be able to boot on SD Card (debian) instead eMMC (yocto mender).    

3.  After boot, you can copy the device tree from /boot/ and check the boot mode.

4.  After that:
   - connect your USB Ubuntu on your host (Linux Host), copy the device tree on your USB Ubuntu in /boot.
   - boot and Hit any key to stop autoboot then configure the boot mode in U-Boot by using env set.
   - reboot    

We recommend you to boot on SD CARD on Debian instead USB ubuntu. The SolidSense debian image contains the good u-boot, the good device tree and has already a package manager.

## 9. Github account to use in the new gateways:
- Usuario: SmartGWay
- email: smartec@salvi.es
- Password: Smartec.23

## 10. Create a `systemd` linux service to start the sink services
In order to run the *gateway services* on reboot, create a *gateway_services.service* file on `/etc/systemd/system/` with the following code:
```
[Unit]
Description="Smartec gateway services"
Wants=network.target
After=network-online.target

[Service]
Type=simple
ExecStart=/home/salvi-smartec/smartec/gateway-services/single_transport/backend/start_gateway_services.sh >> /home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/gateway_services_logs_1.log
Restart=on-failure
RestartSec=60
KillMode=control-group
User=salvi-smartec
StandardOutput=append:/home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/gateway_services_logs_1.log
StandardError=append:/home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/gateway_services_logs_2.log

[Install]
WantedBy=multi-user.target  
```


## 11. Cap the logs of journalctl and syslog

### Caping the journal logs
We need to cap the maximum size of the log file `journal` in order to avoid the service from writing too much information and making the device run out of disk space. Run this command to cap it to *500MB*:
```
sudo journalctl --vacuum-size=500M
```

### Delete the system logs

```
sudo -i
```
Then run your command, it my case:
```
> /var/log/syslog.1
```
Always make sure to exit your root shell once you're done with it
```
exit
```
2
### Give user permissions to the logs

It is a common error that I encounter, the fact that some logs can't be edited by the trimming files `trim_log_output.sh`, because the trimming file doesn't have *root* permissions to the logs.

It is important then to create these files with just user permissions so they can be trimmed automatically and don't grow out of disk space.


## 12. Setting a service to update code

We will create a `systemd` service called `gateway_upload_code.service` that runs every **4h** when the timer `gateway_upload_code.timer` trigger and calls it, and updates from github all the gateway code.

the commands to execute are in the script 
```
git_update_gateway_code.sh
```
The service is going to be called 
```
gateway_update_code.service
```
and its service file is going to have the following commands:

```
[Unit]
Description="update gateway software via git"

[Service]
Type=simple
ExecStart=/home/salvi-smartec/smartec/gateway-services/single_transport/backend/git_update_gateway_code.sh
KillMode=control-group
User=salvi-smartec
StandardOutput=append:/home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/gateway_services_logs_1.log
StandardError=append:/home/salvi-smartec/smartec/gateway-services/single_transport/backend/logs/gateway_services_logs_2.log

[Install]
WantedBy=multi-user.target  
```
We need to run this service as *superadmin* or root, since the *.sh* file that we want this service to run, requires superadmin powers. We can either set `User=root` which will give *ownership issues* with the `git fetch --all` command when pulling the Github code, or we can better set *root privileges* for the local user *LOCAL_USER* by running:
```
sudo usermod -G root LOCAL_USER
``` 
To run this service periodically, we must set up a system timer. You can read more on hwo to set a system timer here > https://wiki.archlinux.org/title/systemd/Timers . Basically we have to create a timer (which is a *.timer* file) and store it in this system folder: 
```
sudo nano /etc/systemd/system/TIMER.timer
```
The timer that will execute this service file must have the same name as the service, in this case it must be called
```
gateway_update_code.timer
```
And it must containg the following configuration
```
[Unit]
Description="update gateway software via git"

[Timer]
OnCalendar=*-*-* *:*/1:00

[Install]
WantedBy=timers.target 
```

Now we must enable it 
```
sudo systemctl enable gateway_update_code.timer
```
And start it
```
sudo systemctl start gateway_update_code.timer
```
And update the system `daemon` if we make any change to the timer:
```
sudo systemctl daemon-reload
```

## 13. Create a script to not update the logs on code update

While uploading to Github, it is possible to upload the developper logs, and thus when the production gateway does a software update, it will download the developper logs and erase its production ones. Since we don't want this to happen, we will have to add the command `git reset -- logs/*` rigth after the `add` command. Like thus:
```
git add .
git reset -- logs/*
git commit -m $message
git push 
```
so that everything within the *gateway-services* directory is uploaded, but the log files are *ignored*, since we want the producion gateway to generate and keep its own logs and not download them from github.

We created a `.sh` script in order to perform the *git push* correctly which we called `commit_and_push_to_github.sh`.

### During otap

Remember that the nodes can take up to 1h to be completely updated and operational.


## 14. Start the sink
Sometimes, the sink is properly configured, and the sink servie is started, but it is not configured to start its stack. Therefore it cannot listen to incoming messages from the nodes. To do so, we could use the 
```
python3 otap_menu.py
```
script, and select the option *Set a new sink config* and there, choose *yes* to start the sink.

I will add it manually in the code just in case.



# Entering the Cloud server

Using a ssh connection with the following parameters:
1. user: *aconchello*
2. password: *VdBB7FDVFI*
3. ip: *159.223.30.89*

Alternative cloud server:
1. IP adress: 209.38.235.149
2. user: root
3. private key and public key?
4. paraphrase for accessing private key: 

[11:45] Alicia Conchello Rosales

t~LQshoni&zhrm&v|zew

[11:47] Alicia Conchello Rosales

smartecalice

[11:47] Alicia Conchello Rosales

mAlte^mX*KQ5@^.UPrl|

## Stopping the cloud server firewall

This webpage describes how to do it > https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-the-mosquitto-mqtt-messaging-broker-on-ubuntu-16-04 basically you have to run the following command once inside the cloud server:

```
sudo ufw allow http
```

and the firewall will deactivate.

# Modifying gateway functionalities:

## 1. Adding a new message type for the cloud <> gateway interactions

Guide in order to know the main things that we will have to change when adding a new message:

### 1. Basic scripts to change:

1. Add a *MSG_type* with the right id to the file `global_vars.py`
2. Add an *EXPECTED_MSG_LENGTH_REQUEST* with the right expected number of bytes to the file `global_vars.py` so that the parsing knows how long will be the message
3. Modify the *parsing functions* to add a case that will process this new type of message, in file `message_received_parse_functions.py` 
4. Add a specific parsing function that will extract the desired arguments from the message request/response and store them into the `args` variable, in the file `message_specific_parse_functions.py` 
5. Do the same with the *display function* files, `message_display_functions.py` and `message_display_specific_functions.py` in order to display the arguments and message received in the logs of cloud/gateway.
6. Repeat steps 2-5 for the response of the message.
7. Depending on the spirit of the message, change any of the 
   - *tunnel to node* functions and file: `interaction_tunnel.py`
   - *software update* functions and file `update_gw_software.py`
   - *update database* functions and file `update_gw_database.py`
   - *read database* functions and file `read_gw_database.py`
   - *prepare response* functions and file `prepare_response.py`

8. In the *prepare response* files and functions, you will also have to alter the *create message* functions in order to create the response to the message request. In particular, you will have to change the files: `create_message_functions.py` to add the case of the new message
9. You will also need to add the specific *message creation function* in the file `create_message_specific_functions.py` in order to create the response/request.
10. If the message is between cloud and gateway, you may also need to change the file `create_message_cloud.py` and if it is between the node <> gateway you will need to change the file `create_message_nodes.py`

### 2. Additional parts to change in the gw software:

In principle that's all you would need to change in order to add a new message type. Depending on the intention of the message, you might need to change the otap files, or other files.