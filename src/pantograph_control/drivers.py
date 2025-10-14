#
# This file will contain the raspberry pi <-> hardware interfaces for the stepper motors,
# servo motors, and camera(s)
#
#
# (Of course) these drivers will be heavily dependant on the rpi version, as pi5 has different
# gpio control than earlier versions.
#
# Long story short, whatever we write will not be backwards compatible. And that's okay!!
# One of our biggest challenges will be getting a position control from a fundamentally
# velocity-controlled motor WITH newer hardware (pi5)

import sys
import time


# https://github.com/gpiozero/gpiozero/issues/144
# TODO: need stepper and servo driver motor classes compatible with pi5

from gpiozero import OutputDevice

class Stepper:

    def __init__(self):
        pass


class Servo:

    def __init__(self):
        pass