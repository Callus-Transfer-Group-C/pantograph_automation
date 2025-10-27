#
# This file will contain the raspberry pi <-> hardware interfaces for the stepper motors,
# servo motors, and camera(s)
#
# The stepper motor driver will need to be position controlled. This means that we will need
# to have a calibration mechanism built in to the driver that can be accessed through the
# 'Calibrate' task
# 


import sys
import time

# TODO: Stepper motor interface
class Stepper:

    def __init__(self):
        pass

# TODO: Servo driver interface
class Servo:

    def __init__(self):
        pass

    def position(self, position:int):

        print(f"Went to position {position}")

        pass

if __name__ == "__main__":

    motor = Servo()
    motor.position(85)