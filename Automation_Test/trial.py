#!/usr/bin/python

import os
import sys
import re
import pexpect

conf_tc_list = {}

def some_func():
    #conf_keys = conf_tc_list.keys()
    for k, v in dict.items(conf_tc_list):
	print k
	print v
        command = "scp root@10.0.6.123:"+k+" ./"
	child = pexpect.spawn(command)
	child.logfile = open("/home/amagi/Desktop/Automation_Test/mylog", "a")
	while i = child.expect (['password:', 'Are you sure you want to continue connecting (yes/no)?']):
	    print i
	    if i==0:
                child.sendline ('secure09')
	    elif i==1:
	        child.sendline ('yes')
	a = k.split("/")
	conf_file = "./"+a[len(a)-1]
	print conf_file
	keys = v.keys()
	new_file = conf_file+"1"
	for every_key in keys:
	    print every_key
	    f1 = open(new_file, 'w')
	    with open(conf_file, 'r') as f:
	        for line in f:
		    if not line.startswith("#"):
		        if line.startswith(every_key):
			    content = line.split("=")
			    content[1] = v.get(every_key)
			    line = content[0]+"="+content[1]
		    f1.write(line)
	    f1.close()
	    command = "mv "+new_file+" "+conf_file
	    os.system(command)
	command = "scp ./"+conf_file+" root@10.0.6.123:"+k
	child = pexpect.spawn(command)
	child.logfile = open("/home/amagi/Desktop/Automation_Test/mylog", "w")
	child.expect ('password:')
        child.sendline ('secure09')
	command = "rm "+conf_file
	os.system(command)	    

def read_conf_file():
    global conf_tc_list
    with open('/home/amagi/Desktop/Automation_Test/TC_Config/TC001.csv', 'r') as f:
	for line in f:
	    line = line.strip("\n")
	    line = line.split(",")
	    if line[0] == "Complete path of file":
		    continue 
	    conf_file = conf_tc_list.get(line[0])
	    if str(conf_file) == "None":
		key_val_dict = {}
		key_val_dict.update({line[1]:line[2].strip("\r")})
		conf_tc_list.update({line[0]:key_val_dict})
	    else:
		key_val_dict = conf_file
		key_val_dict.update({line[1]:line[2].strip("\r")})
		conf_tc_list[line[0]] = key_val_dict

read_conf_file()
print conf_tc_list
some_func()
