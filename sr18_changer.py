#!/bin/python3
# Micro MIDI meta-controller for the SR16/18
# Uses my LCDMenu code for the display.
# See https://github.com/RobCranfill/piAlesisSR for more info.
# (c)2022 robcranfill@robcranfill.net

from lcd_menu import LCDMenu, LCDMenuPage, LCDMenuData
from midi_cc import MidiCC

import mido
import os
import signal
import sys
import threading


DM_MIDI_CHANNEL = 10-1 # The MIDI world calls it channel 10, yet we need to use the value 9 ! :-(
MIDI_INTERFACE_NAME = "MidiSport 1x1 MIDI 1"

_MIDIport = None # global midi output port


class MyAction():
    """
    A somewhat ad-hoc class for implementing action-y menu items.
    This could have been done more simply, using a String object, I suppose.
    """
    # Values for magicActionThing:
    ACTION_SHUT_DOWN = 0
    ACTION_EXIT = 1

    def __init__(self, displayString, magicActionThing):
        self.displayString = displayString
        self.magicActionThing = magicActionThing

    def __str__(self):
        """This is the method that the menu code will use to render this action.
        """
        return self.displayString

    def __repr__(self):
        return self.__str__()


def tidyUp():
    """
    Will be called on exit, normal or otherwise.
    """
    _menu.clearScreen()
    _menu.turnOffBacklight()


def init_midi():
    """
    Initialize the MIDI system.

    Sets the global _MIDIport
    """
    global _MIDIport

    try:
        _MIDIport = mido.open_output(MIDI_INTERFACE_NAME)
        print("Opened MIDI port OK")
    except: 
        print(f"No MIDI port '{MIDI_INTERFACE_NAME}'? Continuing....")


def changeProgram(program):
    """
    Send a MIDI "Program Change" message with the given value.

    Uses the global _MIDIport
    """
    global _MIDIport
    msg = mido.Message("program_change", channel=DM_MIDI_CHANNEL, program=program)
    print(f"Sending {msg}....")
    _MIDIport.send(msg)


def loadFile(filename):
    """
    Load the indicated JSON file into a list menu pages; this can be added to by the caller.
    """
    # print(f"Loading menu data from '{filename}'....")
    oldstyle = MidiCC.decodeFromJSON(open(filename, "r").read())

    pages = []
    for page in oldstyle:
        name = page[MidiCC.SET_NAME]
        list = page[MidiCC.CC_LIST_NAME]
        pages.append(LCDMenuPage(name, list))
    return pages


def callbackHandler(menu_obj):
    """
    This is the method that will be invoked when the "do it" button is pressed.
    """

    if isinstance(menu_obj, MyAction):
        if (menu_obj.magicActionThing == MyAction.ACTION_EXIT):
            print("Exiting....")
            tidyUp()
            sys.exit(MyAction.ACTION_EXIT)
        elif menu_obj.magicActionThing == MyAction.ACTION_SHUT_DOWN:
            print("Halting system....")
            tidyUp()
            os.system("sudo shutdown -h now")
        else:
            print("Unknown action: ", menu_obj) # shouldn't happen
        return
    
    # Must be a MIDI object; send it.
    print(f"Send MIDI control code: '{menu_obj.kitName}', CC {menu_obj.controlCode}")
    if  _MIDIport:
        changeProgram(menu_obj.controlCode)


# Handler for 'die' signal.
def gotSIGWhatever(foo, fum):
    # If we get the signal, create an EXIT action.
    print("Got SIGUSR1 - exiting....")
    callbackHandler(MyAction("mox nix", MyAction.ACTION_EXIT))


# Main code
#
if __name__ == "__main__":

    try:

        # Load the MIDI-oriented pages.
        pageList = loadFile("sr18_small_example.json")

        # A final utility page to control the app.
        lastPage = LCDMenuPage("Utils", 
            [MyAction("Exit menu app", MyAction.ACTION_EXIT),
             MyAction("Shut down Pi",  MyAction.ACTION_SHUT_DOWN)])
        pageList.append(lastPage)

        menudata = LCDMenuData(pageList)

        _menu = LCDMenu(menudata, callbackHandler, buttonsOnRight=True)
        init_midi()

        # When running headless, we can send this signal to stop the app.
        # We are supposed to be able to send a SIGINT to get the same thing as ctrl-C,
        # but it doesn't seem to work. SIGUSR1 works.
        signal.signal(signal.SIGUSR1, gotSIGWhatever)
        
        # We create and wait on this event, but it never comes. How sad.
        # (This program is interrupt driven.)
        #
        threading.Event().wait()

    # ctrl-C? OK, done.
    except KeyboardInterrupt:
        pass

    # something else?
    except OSError as exception:
        print(f"Exception: {exception}")

    finally:
        tidyUp()
