#!/usr/bin/python

"Assignment 2 - This is the controller code that students will have to \
    implement sections of. It is Pyretic based, but this is somewhat\
    unimportant at the moment, as we only care about the learning\
    behaviors."

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import packets
from helpers import *


class LearningSwitch(DynamicPolicy):
    def __init__(self):
        """ Initialization of the Learning Switch. The important piece
            is the definition of the switch mapping. This is a nested
            dictionary. """

        # Initialize the parent class
        super(LearningSwitch, self).__init__()

        # Initialize logfile
        init_log("learning-switch.log") # Do NOT edit this line
        
        # TODO: Initialize your forwarding tables. Create this however you wish.
        # Couple of suggestions: Dictionary of dictionaries, Dictionary of 
        # tuples. 

        # NOTE: (Python tip) if you create a variable like this...
        #    foo = 42
        # that will be a local variable, only accessible in this function.
        #
        # But if you create a variable like this...
        #    self.foo = 42
        # that will be a class member that is accessible from other class
        # methods (functions), such as build_policy(), but remember to use
        # "self" *every* time you access it, or you'll access a local variable
        # instead of the class member!

        # Only use one flood instance - this is the default policy when there 
        # isn't a known path.
        self.flood = flood()

        # Get the first packet from each new MAC address on a switch. This
        # is how we are able to learn new routes.
        new_pkts = packets(1, ['srcmac', 'switch'])
        new_pkts.register_callback(self.learn_route)
        self.query = new_pkts

        # Initialize the policy
        self.build_policy() 


    def print_switch_tables(self):
        # TODO - This is different than how logging in static-switch.py works.
        # Here, you have to do a bit more. First, you need to print out each 
        # entry in the forwarding tables, as was done in static-switch.py.
        # Finally (which is already done for you), end_fwd_table() needs to be
        # called, creating a break between each set of forwarding tables.
        # end_fwd_table() need only be called at the very end - not after each
        # entry.

        # After looping through the forwarding table(s), finish up with a break
        # in the log file.
        end_fwd_table() # Do NOT edit this line


    def learn_route(self, pkt):
        """  This function adds new routes into the fowarding table. """

        # TODO - Create a new entry in the fowarding table. Use the functions 
        # in the second half of helpers to simplify all your work.

        # Print out the switch tables:
        self.print_switch_tables()

        # Call build_policy to update the fowarding tables of the switches.
        self.build_policy()


    def build_policy(self):
        """ 
        This is similar to the build_policy() function in StaticSwitch. 
        There is a major difference: If there isn't a rule, you need to flood
        the packets. The example code should help.
        """
        new_policy = None
        not_flood_pkts = None
        
        # TODO: Example code. You will need to edit this based on how you're 
        # storing your policies. You should only have to replace the details in
        # rule entries.
        rule1 = 1, "00:00:00:00:00:01", 3
        rule2 = 1, "00:00:00:00:00:02", 2
        for rule in (rule1, rule2):
            if new_policy == None:
                # First entry, prime the pump
                new_policy = (match(switch=int(rule[0]), dstmac=(rule[1])) >>
                              fwd(rule[2]))
            else:
                new_policy += (match(switch=int(rule[0]), dstmac=(rule[1])) >>
                               fwd(rule[2]))
            if not_flood_pkts == None:
                not_flood_pkts = (match(switch=int(rule[0]), dstmac=(rule[1])))
            else:
                not_flood_pkts |= (match(switch=int(rule[0]), dstmac=(rule[1])))

        # If you follow the pattern above, you won't have to change this below. 
        if not_flood_pkts == None:
            # We don't know of any rules yet, so flood everything.
            self.policy = self.flood + self.query
        else:
            self.policy = if_(not_flood_pkts, new_policy, self.flood) + self.query
        
        # The following line can be uncommented to see your policy being
        # built up, say during a flood period. (Leave it commented out or
        # re-comment it before you submit this file, though.)
        #print self.policy


def main():
    return LearningSwitch()
