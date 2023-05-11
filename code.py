import board

import usb_midi
import adafruit_midi
import time

# from adafruit_midi.control_change import ControlChange
from adafruit_midi.pitch_bend import PitchBend

import rotaryio

midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0])

# ENCODER 1 ### DEF ###
encoder = rotaryio.IncrementalEncoder(board.GP0, board.GP1)
enc_last_position = 0
Last_midi_check_time = -1


while True:

    now = time.monotonic()

    msg = midi.receive()

    # ENCODER 1 ### LOOP ####
    if enc_last_position is None or encoder.position != enc_last_position:

        if encoder.position >= 16384:
            encoder.position = 0

        if encoder.position <= -1:
            encoder.position = 16383

        enc_last_position = encoder.position

        print("Enc 1,    position: ", encoder.position)
        # midi.send(ControlChange(1, encoder.position)
        midi.send(encoder.position, channel=0)
