#
# This file will contain the raspberry pi <-> hardware interfaces for the stepper motors,
# servo motors, and camera(s)
#
# The stepper motor driver will need to be position controlled. This means that we will need
# to have a calibration mechanism built in to the driver that can be accessed through the
# 'Calibrate' task

import sys
import time

from time import sleep
import RPi.GPIO as GPIO
import math

class Stepper(object):

    def __init__(self, enable, dir, pulse, steps_per_rev=1600):
        '''  '''
        self.steps_per_rev = steps_per_rev
        self.position = 0 # Position in radians


    def step(self, steps):

        for 


class Servo:
    def __init__(self, servo_pin):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(servo_pin, 50)  # 50Hz for servo
        self.pwm.start(0)
        self._position = 0
        self.servo_pin = servo_pin

    @property
    def position(self):
        """Return current servo position (angle)."""
        return self._position

    @position.setter
    def position(self, angle):
        """Set servo position (angle between 0 and 120)."""

        duty = 2 + (angle / 18)
        GPIO.output(self.servo_pin, True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(0.5)
        GPIO.output(self.servo_pin, False)
        self.pwm.ChangeDutyCycle(0)
        self._position = angle


    def cleanup(self):
        """Stop PWM and clean up GPIO."""
        self.pwm.stop()
        GPIO.cleanup()
