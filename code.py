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

def delay():
    return time.sleep(0.025) # 25ms skall vara 40Hz (vilket ändå är DMX update rate taket...)

while True:

    # ENCODER 1 ### HUE #### 0 # 8192 # 16383 #####
    if e1r.position != last_e1r:

        if e1b.value: # "NORMAL MODE" # ≈ 70 Varv / 360 (1 grad i taget...)
            if e1r.position > last_e1r:
                e1r.position = e1r.position + 9
                e1r.position = (e1r.position + 16384) % 16384
                midi.send(PitchBend(e1r.position), channel=0)
            else:
                e1r.position = e1r.position - 9
                e1r.position = (e1r.position + 16384) % 16384
                midi.send(PitchBend(e1r.position), channel=0)

        else:  # ENCODER PRESSED # inc 45 loops 20 ≈ 5 Varv / 360 (20 grader i taget...)
            fade_increment = 45
            fade_loops = 20
            if e1r.position > last_e1r:
                def fade_up():
                    e1r.position = e1r.position + fade_increment
                    e1r.position = (e1r.position + 16384) % 16384
                    midi.send(PitchBend(e1r.position), channel=0)
                    delay()
                for _ in range(fade_loops):
                    fade_up()

            else:
                def fade_down():
                    e1r.position = e1r.position - fade_increment
                    e1r.position = (e1r.position + 16384) % 16384
                    midi.send(PitchBend(e1r.position), channel=0)
                    delay()

                for _ in range(fade_loops):
                    fade_down()

        e1b_last = e1b.value
        last_e1r = e1r.position

        print("Color: ", e1r.position)
        print("Button: ", e1b.value)
        print(" ")

    # time.sleep(0.001)
    # time.sleep(0.025)
    # time.sleep(0.5)
