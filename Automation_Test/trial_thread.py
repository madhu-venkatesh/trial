#!/usr/bin/python

import thread
import time

# Define a function for the thread
def print_time(threadName):
    print "Device %s" %str(threadName)
    func2(threadName, 1)

def func2(threadName, delay):
    print "Hello from func 2, %s" %str(threadName)
    time.sleep(delay)
    print "After sleep %s" %str(threadName)
    if "dev002" in threadName:
	print "Exiting thread for %s" % str(threadName)
	thread.exit()
    print "This is the extra stuff %s" % str(threadName)

with open("dev_list.txt", "r") as f:
    for line in f:
        try:
            thread.start_new_thread(print_time, (line, ))
        except:
            print "Error: Unable to start thread"
while 1:
    pass
