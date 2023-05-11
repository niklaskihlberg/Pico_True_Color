import board
import usb_midi
import adafruit_midi

import rotaryio

from adafruit_midi.pitch_bend import PitchBend

# midi = adafruit_midi.MIDI(midi_in=usb_midi.ports[0])
midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0], in_channel=0, midi_out=usb_midi.ports[1], out_channel=0
)

# ENCODER 1 ### DEF ###
encoder = rotaryio.IncrementalEncoder(board.GP0, board.GP1)
enc_last_position = 0


while True:

    # ENCODER 1 ### LOOP ####
    if enc_last_position is None or encoder.position != enc_last_position:

        if encoder.position >= 1639:       # 16383
            encoder.position = 0

        if encoder.position <= -1:
            encoder.position = 1638

        enc_last_position = encoder.position
        print("Enc 1,    position: ", encoder.position)
        midi.send(PitchBend(encoder.position * 10))
