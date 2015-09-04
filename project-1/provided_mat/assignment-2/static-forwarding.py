#!/usr/bin/python

" Assignment 2 - static-forwarding.py - \
    First part of the assignment. This is to create a static-forwarding table."

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from helpers import *


class StaticSwitch(Policy):
    def __init__(self):
        """ 
        Initialization of static switch. Set up your forwarding tables  here.
        You need to key off of Switch and MAC address to determine forwarding
        port.
        Suggested routes: 
          - Array with switch as index, dictionary for MAC to switch port
          - dictionary of dictionaries
        """

        # Initialize the parent class
        super(StaticSwitch, self).__init__()

        # TODO: Set up forwarding tables. Create this however you wish. As
        # a suggestion, using a list of tuples will work.

        # NOTE: (Python tip) If you create a variable like this...
        #    foo = 42
        # that will be a local variable, only accessible in this function.
        #
        # But if you create a variable like this...
        #    self.foo = 42
        # that will be a class member that is accessible from other class
        # methods (functions), such as build_policy(), but remember to use
        # "self" *every* time you access it, or you'll access a local variable
        # instead of the class member!

        # Initialize logfile
        init_log("static-forwarding.log") # Do NOT edit this line

        # TODO (below): Write out the forwarding tables. This is different than 
        # what you will need to do in learning-switch.py: you need only do this
        # once. You need to write out the forwarding table entries one-by-one,
        # then close out the file. The file is initialized and closed already
        # for you, you simply need to loop through the forwarding table you 
        # created above.
        #
        # Loop through table entries using write_forwarding_table() from
        # helpers.py


    def build_policy(self):
        """ 
        This creates the pyretic policy. You'll need to base this on how you 
        created your forwarding tables. You need to compose the policies 
        in parallel. 
        """
        
        subpolicies = []

        # TODO: Rework below based on how you created your forwarding tables.
        subpolicies.append(match(switch=1, dstmac="00:00:00:00:00:01") >> fwd(3))
        subpolicies.append(match(switch=1, dstmac="00:00:00:00:00:02") >> fwd(2))

        # NOTE: the following lines will flood for MAC broadcasts (to
        # ff:ff:ff:ff:ff:ff). You need to include something like this in order
        # for ARPs to propogate, so we recommend you do not edit the
        # "ff:ff:ff:ff:ff:ff" rules. xfwd() is like fwd(), but will not forward
        # out a port a packet came in on.
        subpolicies.append(match(switch=1, dstmac="ff:ff:ff:ff:ff:ff") >> parallel([xfwd(1), xfwd(2), xfwd(3)])) # Do NOT edit this line
        subpolicies.append(match(switch=2, dstmac="ff:ff:ff:ff:ff:ff") >> parallel([xfwd(1), xfwd(2), xfwd(3)])) # Do NOT edit this line

        # This returns a parallel composition of all the subpolicies you put
        # together above.
        return parallel(subpolicies)


def main():
    return StaticSwitch().build_policy()
