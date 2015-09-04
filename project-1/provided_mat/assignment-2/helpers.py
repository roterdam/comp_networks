#!/usr/bin/python

"Helpers for Assignment 2."

import re

logfilename = None

def init_log(filename):
    global logfilename
    logfilename = filename
    logfile = open(logfilename, "w")
    logfile.close()
    
def write_forwarding_entry(switchnum, switchport, macaddr):
    global logfilename
    logfile = open(logfilename, "a")
    # Prints out a forwarding entry to the log file

    # Lots of type checking beforehand.
    if isinstance(switchnum, int) != True:
        raise TypeError("switchnum is not an int")
    if isinstance(switchport, int) != True:
        raise TypeError("switchport is not an int")
    if isinstance(macaddr, str) != True:
        raise TypeError("macaddr is not a string")
    # from https://stackoverflow.com/questions/7629643/how-do-i-validate-the-format-of-a-mac-address
    if None == re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", macaddr.lower()):
        raise TypeError("macaddr is not in proper form: 00:00:00:00:00:00")

    logfile.write(str(switchnum) + " " + str(switchport) + " " + macaddr.lower() + "\n")
    print str(switchnum) + " " + str(switchport) + " " + macaddr.lower()

    logfile.close()

def end_fwd_table():
    global logfilename
    logfile = open(logfilename, "a")
    logfile.write("\n")
    print ""
    logfile.close()



# These helper functions are simply macros to simplify your introduction
# to Pyretic.
def get_src_mac(pkt):
    """ Returns the source MAC address of the packet. """
    return pkt['srcmac']

def get_dst_mac(pkt):
    """ Returns the destination MAC address of the packet. """
    return pkt['dstmac']

def get_switch(pkt):
    """ Returns the switch of the packet. """
    return pkt['switch']

def get_inport(pkt):
    """ Returns the port the packet came in on. """
    return pkt['inport']

def get_outport(pkt):
    """ Returns the port the packet came in on. """
    return pkt['outport']
