import board
import storage

from digitalio import DigitalInOut, Direction, Pull

import usb_midi  # usb_hid

# On some boards, we need to give up HID to accomodate MIDI.
# usb_hid.enable()

# DigitalInOut(board.GP2).direction = Direction.INPUT
# DigitalInOut(board.GP2).pull = Pull.UP

e1b = DigitalInOut(board.GP2)
e1b.direction = Direction.INPUT
e1b.pull = Pull.UP
# last_e1b = True

if e1b.value:
    print("No button pressed while power on: disable_usb_drive()")
    storage.disable_usb_drive()

usb_midi.enable()

# else:
#     print("Button pressed while power on: enable_usb_drive()")
#     storage.enable_usb_drive()