import board
import usb_midi
import adafruit_midi
import time
import rotaryio

from digitalio import DigitalInOut, Direction, Pull
from adafruit_midi.pitch_bend import PitchBend
from analogio import AnalogIn

# from statistics import mean

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

# POTENTIOMETER 1 ### DEF ###
a1p = AnalogIn(board.GP26)
last_a1p = 0


def delay():
    return time.sleep(0.025) # 25ms skall vara 40Hz (vilket ändå är DMX update rate taket...)

def get_14bit_midi_from_voltage(value):

    # value = pin.value

    # Ceiling 1
    if value > 56000:
        value = 56000

    # Floor 1
    elif value < 2800:
        value = 2800

    else:
        value = value

    # Floor 2
    value = int(value - 2800)

    # Floor 3...
    if value <= 0:
        value = 0

    # Divide to ≈ 14-bit midi range... (Ungefär...) (53201 / 3.25 = 16384)
    value = value / 2.7

    # Make value an integer
    value = int(value)

    # Ceiling 2
    if value > 16383:
        value = 16383

    return value


while True:

    # # ENCODER 1 ### HUE #### 0 # 8192 # 16383 #####
    # if e1r.position != last_e1r:
    #
    #     if e1b.value: # "NORMAL MODE" # ≈ 70 Varv / 360 (1 grad i taget...)
    #         if e1r.position > last_e1r:
    #             e1r.position = e1r.position + 9
    #             e1r.position = (e1r.position + 16384) % 16384
    #             midi.send(PitchBend(e1r.position), channel=0)
    #         else:
    #             e1r.position = e1r.position - 9
    #             e1r.position = (e1r.position + 16384) % 16384
    #             midi.send(PitchBend(e1r.position), channel=0)
    #
    #     else:  # ENCODER PRESSED # inc 45 loops 20 ≈ 5 Varv / 360 (20 grader i taget...)
    #         fade_increment = 180
    #         fade_loops = 5
    #         if e1r.position > last_e1r:
    #             def fade_up():
    #                 e1r.position = e1r.position + fade_increment
    #                 e1r.position = (e1r.position + 16384) % 16384
    #                 midi.send(PitchBend(e1r.position), channel=0)
    #                 delay()
    #             for _ in range(fade_loops):
    #                 fade_up()
    #
    #         else:
    #             def fade_down():
    #                 e1r.position = e1r.position - fade_increment
    #                 e1r.position = (e1r.position + 16384) % 16384
    #                 midi.send(PitchBend(e1r.position), channel=0)
    #                 delay()
    #
    #             for _ in range(fade_loops):
    #                 fade_down()
    #
    #     e1b_last = e1b.value
    #     last_e1r = e1r.position
    #
    #     print("Encoder Color: ", e1r.position, "Button:", e1b.value)
    #     print(" ")


    # PEDAL:
    raw_analog_samples = []
    analog_input_resolution = 750

    # Append voltage samples into the list:
    for _ in range(analog_input_resolution):
        raw_analog_samples.append(a1p.value)

    # If the list isn't empty...
    if not len(raw_analog_samples) <= 0:

        # Average out the value:
        a1p_averaged_value = int(sum(raw_analog_samples) / len(raw_analog_samples))

        # Average out the value TEST:
        # a1p_averaged_value = int(mean(raw_analog_samples))

        # Turn the voltage into 14-bit midi:
        a1p_averaged_value_midi = get_14bit_midi_from_voltage(a1p_averaged_value)

        # And it exceeds the threshold...
        if len(raw_analog_samples) >= analog_input_resolution:

            # AND passes the "debouncing-test":
            if a1p_averaged_value_midi != last_a1p:

                # Send the midi!
                midi.send(PitchBend(a1p_averaged_value_midi), channel=1)
                print("Pedal Midi: ", a1p_averaged_value_midi)
                print(" ")
                last_a1p = a1p_averaged_value_midi

            # Clear the list...
            raw_analog_samples.clear()


    # time.sleep(0.001)
    time.sleep(0.025) # 40Hz
    # time.sleep(0.1)
    # time.sleep(0.25)
    # time.sleep(0.5)
    # time.sleep(1)



