#!/bin/python3
# Being a thing what encapsulates the name of a drum kit, and the corresponding MIDI Control Code.
#
import json

class MidiCC:
    """
    Being a thing what encapsulates the name of a drum kit, and the corresponding MIDI Control Code.
    Also has a utility method to parse this data from a JSON file. 
    (Said file contains other crap, too; see below for its structure.)
    """

    # dictionary keys
    SET_NAME     = "setname"
    CC_LIST_NAME = "ccdata"

    def __init__(self, kitname, controlcode):
        self.kitName = kitname
        self.controlCode = controlcode

    def __str__(self):
        """This is the method that the menu code will use to render each item.
        """
        return self.kitName

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def decodeFromJSON(s):
        """
        Load the JSON data from the given string.
        The first item in each list is a string - the name of the set of objects.
        The second item in each list is a list of kit names and control codes.
        Returns a list of dictionary items: SET_NAME, and CC_LIST_NAME which is a list of CC objects.
        """
        result = []
        for pagedata in json.loads(s): # "pagedata" is a string followed by a list of CC objects.
            resultdict = {}
            resultdict[MidiCC.SET_NAME] = pagedata[0]
            cclist = pagedata[1]
            ccresult = []
            for k in cclist:
                ccresult.append(MidiCC(k[0], k[1]))
            resultdict[MidiCC.CC_LIST_NAME] = ccresult
            result.append(resultdict)
        return result


# Test code.
# The input file should look something like this:
#  a list of
#    a string (the page title), followed by
#    a list of tuples of: a string (the kit name) and an integer (the MIDI control code).
#
# such as:
# [
#   [
#     "Rock kits",
#     [["Rock01", 57], ["Rock02", 58], ["Rock03", 59], ["Rock04", 60], ["Rock05", 61], ["Rock06", 62]]
#   ],
#   [
#     "Techno kits",
#     [["Techno01", 78], ["Techno02", 79], ["Techno03", 80], ["Techno04", 81], ["Techno05", 82]]
#   ]
# ]
#
if __name__ =="__main__":
    filename = "sr18_small_example.json"
    print(f"Testing parsing JSON file '{filename}'....")
    f = open(filename, "r")
    fcontents = f.read()
    # print(f" read: {fcontents}\n")
    # print(f" json: {json.loads(fcontents)}\n")
    newlist = MidiCC.decodeFromJSON(fcontents)

    print("Parsed:", newlist)
