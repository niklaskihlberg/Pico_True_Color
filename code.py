import board
import usb_midi
import adafruit_midi
import time
import rotaryio

from digitalio import DigitalInOut, Direction, Pull
from adafruit_midi.pitch_bend import PitchBend

midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0], in_channel=0, midi_out=usb_midi.ports[1], out_channel=0
)

# ENCODER 1 BTN ### DEF ###
e1b = DigitalInOut(board.GP2)
e1b.direction = Direction.INPUT
e1b.pull = Pull.UP
last_e1b = True

# ENCODER 1 ### DEF ###
e1r = rotaryio.IncrementalEncoder(board.GP0, board.GP1)
last_e1r = 0

while True:

    # ENCODER 1 ### HUE #### 0 # 8192 # 16383 #####
    if e1r.position != last_e1r:

        if e1b.value: # "NORMAL MODE"
            if e1r.position > last_e1r: e1r.position = e1r.position + 9
            else: e1r.position = e1r.position - 9

        else:  # ENCODER PRESSED
            if e1r.position > last_e1r: e1r.position = e1r.position + 249
            else: e1r.position = e1r.position - 249

        e1r.position = (e1r.position + 16384) % 16384
        midi.send(PitchBend(e1r.position), channel=0)
        e1b_last = e1b.value
        last_e1r = e1r.position

        print("Color: ", e1r.position)
        print("Button: ", e1b.value)
        print(" ")

    time.sleep(0.001)
    # time.sleep(0.025)
    # time.sleep(0.5)
