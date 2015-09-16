#!/usr/bin/python

import thread
import time
import os
import sys
import pexpect
import re

workspace = ""
#git_tag_name = ""
#job_name = ""
dev_tc_list = {}

def remove_host(dev):
    command = "ssh-keygen -f /root/.ssh/known_hosts -R "+dev
    os.system(command)

def dev_cleanup(dev_details):
    print "Cleaning up!"
    command = "ssh "+dev_details[2]+"@"+dev_details[1]
    child = pexpect.spawn(command)
    child.logfile = open("mylog1", "w")
    child.expect('Are you sure you want to continue connecting (yes/no)?')
    child.sendline('yes')
    child.expect ('password:')
    child.sendline (dev_details[3])
    child.expect('#')
    child.sendline('cd /mnt/ops/logs')
    child.expect('#')
    child.sendline('rm -rf *')
    child.expect('#')
    child.sendline('ls')
    child.expect('#')
    var = child.before
    var1 = var.split("\n")
    if len(var1)==2:
	print "Cleanup Done!"

def dev_log_backup(dev_details):
    print "In log backup"
    command = "scp -r "+dev_details[2]+"@"+dev_details[1]+":/mnt/ops/logs /var/lib/jenkins/jobs/Dart_Build/logs"
    child = pexpect.spawn(command)
    child.logfile = open("/var/lib/jenkins/jobs/Dart_Build/mylog1", "w")
    child.expect ('password:')
    child.sendline (dev_details[3])
    time.sleep(120)
    #print "At the end of log backup"
    #child.expect('#')
    #child.sendline('cd /mnt/ops/logs')
    #child.expect('#')
    
def dev_accessibility(dev_details):
    command = "ping -c 1 " + dev_details[1]
    if os.system(command) == 0:
        print "%s is up!" % dev_details[1]
        return 1
    else:
        print "%s is down!" % dev_details[1]
        return -1

def check_upgrade(f, dev_details):
    command = "ssh "+dev_details[2]+"@"+dev_details[1]
    child = pexpect.spawn(command)
    child.logfile = open("/var/lib/jenkins/jobs/Dart_Build/mylog", "w")
    child.expect('Are you sure you want to continue connecting (yes/no)?')
    child.sendline('yes')
    child.expect ('password:')
    child.sendline (dev_details[3])
    child.expect('#')
    child.sendline('cat /etc/release')
    child.expect('#')
    var = child.before
    var1 = var.split("\n")
    print var1[1]
    if var1[1].strip("\r") in f:
        print "Upgrade successful!"

def dev_upgrade(dev_details):
    global workspace
    print workspace
    command = workspace + "/z3/images/"
    print command
    os.chdir(command)
    files = os.listdir(command)
    for f in files:
        if "firmware" in f:
            print f
            break
    command = "wput ./" + f + " ftp://"+dev_details[2]+":"+dev_details[3]+"@"+dev_details[1]+"/../mnt/support/package/"+f
    os.system(command)
    time.sleep(180)
    while True:
        res = dev_accessibility(dev_details)
        if res == 1:
            break
    remove_host(dev_details[1])
    #Check if upgrade was successful
    check_upgrade(f, dev_details)

#Key-Device Name, Value: 0-Device ID 1-Device IP 2-Login 3-Pwd 4 onwards TC IDs
def device_thread(key):
    print key
    dev_details = dev_tc_list[key]
    print dev_details
    tc_list = dev_details[4:]
    res = dev_accessibility(dev_details)
    if res == -1:
        print "Device not accessible"
        thread.exit()
    dev_upgrade(dev_details)
    dev_log_backup(dev_details)
    #i = 0
    for tc in tc_list:
        remove_host(dev_details[1])
        dev_cleanup(dev_details)
	edit_config(dev_details)
        #exec_tc(tc)
	#i += 1

def get_dev_num_tc():
    global dev_tc_list
    i = 0
    with open('dev_tc_list.csv', 'r') as f:
	for line in f:
	    line = line.strip("\n")
	    line = line.split(",")
	    if line[0] == "Device Name":
		    continue 
	    num_tc = dev_tc_list.get(line[0])
	    if str(num_tc) == "None":
		    dev_details = []
		    dev_details.append(line[1])
		    dev_details.append(line[2])
		    dev_details.append(line[3])
		    dev_details.append(line[4])
		    dev_details.append(line[5])
		    dev_tc_list.update({line[0]:dev_details})
	    else:
		    dev_details = num_tc
		    dev_details.append(line[5])
		    dev_tc_list[line[0]] = dev_details

def spawn_thread():
    dev_keys = dev_tc_list.keys()
    for key in dev_keys:
	    try:
	        thread.start_new_thread(device_thread, (key,))
	    except:
	        print "ERROR: Unable to start thread for device %s" % str(key)
    while 1:
	    pass

workspace = sys.argv[1]
#workspace = workspace.strip("/")
#git_tag_name = sys.argv[2]
#job_name = sys.argv[3]
get_dev_num_tc()
spawn_thread()















