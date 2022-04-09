# piAlesisSR
A way to select different drum kits ("kit" in the sense of "collections of sounds"), when using a MIDI drum kit ("kit" in the sense of a physical set of surfaces to be beat upon; an Alesis DM6, in my case) to send notes to an external drum machine (an Alesis SR18 for me).

This uses my [PiLCDmenu](https://github.com/RobCranfill/PiLCDmenu) code to present a super-simple GUI to select a drum kit via MIDI.

This is Yet Another Solution to my ongoing quest (see my other projects, such as [MIDIBox](https://github.com/RobCranfill/midiBox), [PowerOff](https://github.com/RobCranfill/poweroff), and [MIDITrans](https://github.com/RobCranfill/miditrans)) to be able to easily and on the fly select "nice" drum kits.

To reiterate the problem statement:
 * The DM6 built-in sounds are a) very limited; b) lame; and c) on my machine, broken.
 * The DM6 uses USB-MIDI, but SR18 has only DIN MIDI connectors.

This led me to the solution of a Raspberry Pi running the ALSA 'aconnect' util, which sends MIDI notes from the DM6 to the SR16/18. Independently, this code sends control codes to select different kits.

----
Notes:
 Don't forget to do something like
  ``export PYTHONPATH=../PiLCDmenu/``
