#!/bin/python3
# Micro MIDI controller for the SR16/18

from lcd_menu import LCDMenu
from midi_cc import MidiCC
import mido
import threading

DM18_MIDI_CHANNEL = 10-1 # The MIDI world calls it channel 10, yet we need to use the value 9 ! :-(

_MIDIport = None


def init_midi():
    """
    Initialize the MIDI system.

    Sets the global _MIDIport
    """
    global _MIDIport

    _MIDIport = mido.open_output('MidiSport 1x1 MIDI 1')
    print("Opened MIDI port OK")


def changeProgram(program):
    """
    Send a MIDI "Program Change" message with the given value.

    Uses the global _MIDIport
    """
    global _MIDIport
    msg = mido.Message('program_change', channel=DM18_MIDI_CHANNEL, program=program)
    print(f"Sending {msg}....")
    _MIDIport.send(msg)


def loadFile(filename):
    """
    Load the indicated JSON file into a list of lists of MIDI objects.
    """
    # print(f"Loading menu data from '{filename}'....")
    f = open(filename, "r")
    fcontents = f.read()
    return MidiCC.decodeFromJSON(fcontents)


def callbackHandler(midicc_obj):
    """
    This is the method that will be invoked when the "do it" button is pressed.
    """
    print(f"callbackHandler: '{midicc_obj.kitName}', CC {midicc_obj.controlCode}")
    changeProgram(midicc_obj.controlCode)


# Main code
#
if __name__ == "__main__":

    try:
        menuData = loadFile("sr18_small_example.json")
        menu = LCDMenu(menuData, callbackHandler, buttonsOnRight=True)
        init_midi()

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
        menu.clearScreen()
        menu.turnOffBacklight()
