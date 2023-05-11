import usb_midi  # usb_hid

# On some boards, we need to give up HID to accomodate MIDI.
# usb_hid.enable()
usb_midi.enable()
