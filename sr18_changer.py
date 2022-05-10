#!/bin/python3
# Micro MIDI controller for the SR16/18

from lcd_menu import LCDMenu
from midi_cc import MidiCC
import mido
import threading
import os
import signal
import sys


DM_MIDI_CHANNEL = 10-1 # The MIDI world calls it channel 10, yet we need to use the value 9 ! :-(

_MIDIport = None # global midi output port


class LCDAction():
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
        """This is the method that the menu code will use to render each item.
        """
        return self.displayString

    def __repr__(self):
        return self.__str__()


def tidyUp():
    _menu.clearScreen()
    _menu.turnOffBacklight()


def init_midi():
    """
    Initialize the MIDI system.

    Sets the global _MIDIport
    """
    global _MIDIport

    try:
        _MIDIport = mido.open_output('MidiSport 1x1 MIDI 1')
        print("Opened MIDI port OK")
    except: 
        print("No MIDI port 'MidiSport 1x1 MIDI 1'? Continuing....")


def changeProgram(program):
    """
    Send a MIDI "Program Change" message with the given value.

    Uses the global _MIDIport
    """
    global _MIDIport
    msg = mido.Message('program_change', channel=DM_MIDI_CHANNEL, program=program)
    print(f"Sending {msg}....")
    _MIDIport.send(msg)


def loadFile(filename):
    """
    Load the indicated JSON file into a list of lists of MIDI objects.
    """
    # print(f"Loading menu data from '{filename}'....")
    return MidiCC.decodeFromJSON(open(filename, "r").read())


def callbackHandler(menu_obj):
    """
    This is the method that will be invoked when the "do it" button is pressed.
    """

    if isinstance(menu_obj, LCDAction):
        if (menu_obj.magicActionThing == LCDAction.ACTION_EXIT):
            print("Exiting....")
            tidyUp()
            sys.exit(LCDAction.ACTION_EXIT)
        elif menu_obj.magicActionThing == LCDAction.ACTION_SHUT_DOWN:
            print("Halting system....")
            tidyUp()
            os.system('sudo shutdown -h now')
        else:
            print("Unknown action: ", menu_obj) # shouldn't happen
        return
    
    # Must be a MIDI thing.

    print(f"callbackHandler: '{menu_obj.kitName}', CC {menu_obj.controlCode}")
    if  isinstance(_MIDIport, mido.PortMidi):
        changeProgram(menu_obj.controlCode)


# Handler for 'die' signal.
def gotSIGWhatever(foo, fum):
    # If we get the signal, create an EXIT action.
    print("Got SIGUSR1 - exiting....")
    callbackHandler(LCDAction("mox nix", LCDAction.ACTION_EXIT))


# Main code
#
if __name__ == "__main__":

    try:
        menuData = loadFile("sr18_small_example.json")

        # ...and this adds one item to the last menu page: shut down the machine.
        menuData.append([LCDAction("Exit app", LCDAction.ACTION_EXIT),
                         LCDAction("Shut down Pi",  LCDAction.ACTION_SHUT_DOWN)])
        # print("Menu data:\n", menuData)

        _menu = LCDMenu(menuData, callbackHandler, buttonsOnRight=True)
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
