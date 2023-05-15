import array
import math
import time
import random

# import board

# ------------------------------------------------------------- #
# ------------------------------------------------------------- #


def average_pot(pin, samples_quant):
    samples_sum = 0
    for _ in range(samples_quant):
        samples_sum += int(pin)
        # time.sleep(0.005)
        # time.sleep(1)
    print("Samples_sum: ", samples_sum)
    return int(samples_sum / samples_quant)


while True:

    fruits = []

    fruit = []
    # random.randint(0, 16383)

    for _ in range(12):
        single_fruit = random.randint(0, 16383)
        fruit.append(single_fruit)

    for pin in fruit:
        fruits.append(pin)
        print("Len: ", len(fruits))

        if len(fruits) >= 5:
            print("List >= 5 : ", fruits, "     Average: ", (int(sum(fruits) / len(fruits))), "     CLEAR THE LIST!")
            fruits.clear()
            print("List: ", fruits)
            print(" ")
            print(" ")

        # time.sleep(0.01)


    print(" ")
    print(" ")
    print(" ")


    time.sleep(10)
