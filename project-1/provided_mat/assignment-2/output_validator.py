# Assignment 2 output validator for CS 6250 (OMS).
# auth Angela Smiley (based on Assignment 3 output validator by Michael Brown.)

# This output validator is designed to check the student's result log files for errors.
# Errors detected (both):
# Missing or extra columns in log entries.

# Errors detected (static):
# Invalid switch names (not in the sample topology).
# Invalid ports (not in the sample topology).
# Invalid MAC addresses (not in the sample topology).

# Errors detected (learning):
# Missing call to next_entry()

import sys
import re

line_number = 1

def validateStudentOutput(filename, validSwitches=None, validPorts=None, validMacs=None):
    with open(filename) as f:
        for line in f:
            if line != "\n":
                line = line[0:len(line)-1]
                validateLine(line, validSwitches, validPorts, validMacs)
            global line_number
            line_number = line_number + 1


def validateLine(line, validSwitches=None, validPorts=None, validMacs=None):
    vals = line.split(' ')
    if len(vals) != 3:
        print "Invalid Output[L" + str(line_number) + "]: log entry should have three values but " + str(len(vals)) + " are given."
        return
    try:
        switch = int(vals[0])
        if (validSwitches != None) and not (switch in validSwitches):
            print "Invalid Output[L" + str(line_number) + "]: switches in this problem are numbered (" + str(validSwitches) + ") but " + str(switch) + " is given."
    except ValueError:
        print "Invalid Output[L" + str(line_number) + "]: switch no. should be an integer value but is " + vals[0]

    try:
        port = int(vals[1])
        if (validPorts != None) and not (port in validPorts):
            print "Invalid Output[L" + str(line_number) + "]: switches in this problem have ports (" + str(validPorts) + ") but " + str(port) + " is given."
    except ValueError:
        print "Invalid Output[L" + str(line_number) + "]: port no. should be an integer value but is " + vals[1]

    mac = str(vals[2])
    if not isValidMAC(mac):
        print "Invalid Output[L" + str(line_number) + "]: " + mac + " is not a valid MAC address."
    elif (validMacs != None) and not (mac in validMacs):
        print "Invalid Output[L" + str(line_number) + "]: hosts in this problem have mac addresses (" + str(validMacs) + ") but " + mac + " is given."


def isValidMAC(mac):
    hex_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F']
    valid = True
    octets = mac.split(':')
    if len(octets) != 6:
        valid = False
    else:
        for octet in octets:
            if len(octet) != 2:
                valid = False
            else:
                for digit in octet:
                    if digit not in hex_digits:
                        valid = False
    return valid


def countIterations(filename):
    totalSteps=0
    with open(filename) as f:
        for line in f:
            if line == "\n":
                totalSteps += 1
    return totalSteps


if len(sys.argv) != 3 or not (sys.argv[2] in ['static-forwarding', 'learning-switch']):
    print "Syntax:"
    print "    python "+sys.argv[0]+" <log_file> <mode>"
    print "    <mode>: one of {static-forwarding, learning-switch}"
    exit()

print "Output validation initiated on " + sys.argv[1] + " (" + sys.argv[2] + "):"

if sys.argv[2] == 'static-forwarding':
    if countIterations(sys.argv[1]) > 0:
        print("Invalid Output: Blank line in static-forwarding log file " + sys.argv[1])
    validateStudentOutput(sys.argv[1],
                          validSwitches=[1, 2],
                          validPorts=[1, 2, 3],
                          validMacs=['00:00:00:00:00:01','00:00:00:00:00:02','00:00:00:00:00:03','00:00:00:00:00:04'])
else:
    if countIterations(sys.argv[1]) < 1:
        print("Invalid Output: Missing next_entry() in learning-switch log file " + sys.argv[1])
    validateStudentOutput(sys.argv[1])

print "Output validation complete."

