import board
import usb_midi
import adafruit_midi

from digitalio import DigitalInOut, Direction, Pull
import rotaryio

from adafruit_midi.pitch_bend import PitchBend

midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0], in_channel=0, midi_out=usb_midi.ports[1], out_channel=0
)

# ENCODER 1 BTN ### DEF ###
e1b = DigitalInOut(board.GP2)
e1b.direction = Direction.INPUT
e1b.pull = Pull.UP

e1b_last = e1b.value


# ENCODER 1 ### DEF ###
e1r = rotaryio.IncrementalEncoder(board.GP0, board.GP1)
e1r_last = 0


while True:

    # ENCODER 1 BTN ###
    if e1b.value != e1b_last:
        if not e1b.value:
            print("E1 Button - PRESSED - ", e1b.value)
        else:
            print("E1 Button - RELEASED - ", e1b.value)

    e1b_last = e1b.value

    # ENCODER 1 ### HUE #### 0 # 8192 # 16383 #####
    if e1r_last is None or e1r.position != e1r_last:

        if e1r.position >= 16384:
            e1r.position = 0

        if e1r.position <= -1:
            e1r.position = 16383
        
        midi.send(PitchBend(e1r.position))
        print("Enc 1,    position: ", e1r.position)
        
        # if not e1b.value:
            # midi.send(PitchBend(int(e1r.position * 100)))
            # print("Enc 1,    position: ", int(e1r.position * 100))
        # else:
            # midi.send(PitchBend(int(e1r.position * 10)))
            # print("Enc 1,    position: ", int(e1r.position * 10))
            
        e1r_last = e1r.position
