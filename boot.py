import board
import usb_midi  # usb_hid

from digitalio import DigitalInOut, Direction, Pull

# On some boards, we need to give up HID to accomodate MIDI.
# usb_hid.enable()
usb_midi.enable()

# DigitalInOut(board.GP2).direction = Direction.INPUT
# DigitalInOut(board.GP2).pull = Pull.UP
#
# if not DigitalInOut(board.GP2).value:
#     MOUNT THE STORAGE
#
# else:
#     HIDE IT...