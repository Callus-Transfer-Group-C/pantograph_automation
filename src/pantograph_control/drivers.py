#
# This file will contain the raspberry pi <-> hardware interfaces for the stepper motors,
# servo motors, and camera(s)
#
# The stepper motor driver will need to be position controlled. This means that we will need
# to have a calibration mechanism built in to the driver that can be accessed through the
# 'Calibrate' task
# 
# https://github.com/gavinlyonsrepo/RpiMotorLib

import sys
import time
import RPi.GPIO as gpio

def degree_calc(steps, steptype):
    """ Utility """
    degree_value = {'Full': 1.8,
                    'Half': 0.9,
                    '1/4': .45,
                    '1/8': .225,
                    '1/16': 0.1125,
                    '1/32': 0.05625,
                    '1/64': 0.028125,
                    '1/128': 0.0140625}
    degree_value = (steps*degree_value[steptype])
    return degree_value

# TODO: Stepper motor interface
class Stepper:

    def __init__(self):
        pass

# TODO: Servo driver interface
class Servo:

    def __init__(self):
        pass

# from gavinlyonsrepo
class A4988Nema:
    """ Class to control a Nema bi-polar stepper motor with a A4988
    
        Attributes:
        
        Methods:"""
    def __init__(self, direction_pin, step_pin, mode_pins, motor_type="A4988"):

        assert motor_type in ["A4988", "DRV8825", "LV8729"], f"Error invalid motor_type: {motor_type}"
        
        self.motor_type = motor_type
        self.direction_pin = direction_pin
        self.step_pin = step_pin

        if mode_pins[0] != -1:
            self.mode_pins = mode_pins
        else:
            self.mode_pins = False

        self.stop_motor = False
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)

    def motor_stop(self):
        """ Stop the motor """
        self.stop_motor = True

    def resolution_set(self, steptype):
        """ method to calculate step resolution
        based on motor type and steptype"""

        
        if self.motor_type == "A4988":
            resolution = {'Full': (0, 0, 0),
                          'Half': (1, 0, 0),
                          '1/4': (0, 1, 0),
                          '1/8': (1, 1, 0),
                          '1/16': (1, 1, 1)}
        elif self.motor_type == "DRV8825":
            resolution = {'Full': (0, 0, 0),
                          'Half': (1, 0, 0),
                          '1/4': (0, 1, 0),
                          '1/8': (1, 1, 0),
                          '1/16': (0, 0, 1),
                          '1/32': (1, 0, 1)}
        elif self.motor_type == "LV8729":
            resolution = {'Full': (0, 0, 0),
                          'Half': (1, 0, 0),
                          '1/4': (0, 1, 0),
                          '1/8': (1, 1, 0),
                          '1/16': (0, 0, 1),
                          '1/32': (1, 0, 1),
                          '1/64': (0, 1, 1),
                          '1/128': (1, 1, 1)}
        
        # error check stepmode
        assert steptype in resolution, f"Error invalid steptype: {steptype}"

        if self.mode_pins != False:
            gpio.output(self.mode_pins, resolution[steptype])

    def motor_go(self, clockwise=False, steptype="Full",
                 steps=200, stepdelay=.005, verbose=False, initdelay=.05):
        """ motor_go,  moves stepper motor based on 6 inputs

         (1) clockwise, type=bool default=False
         help="Turn stepper counterclockwise"
         (2) steptype, type=string , default=Full help= type of drive to
         step motor 5 options
            (Full, Half, 1/4, 1/8, 1/16) 1/32 for DRV8825 only 1/64 1/128 for LV8729 only
         (3) steps, type=int, default=200, help=Number of steps sequence's
         to execute. Default is one revolution , 200 in Full mode.
         (4) stepdelay, type=float, default=0.05, help=Time to wait
         (in seconds) between steps.
         (5) verbose, type=bool  type=bool default=False
         help="Write pin actions",
         (6) initdelay, type=float, default=1mS, help= Intial delay after
         GPIO pins initialized but before motor is moved.

        """
        self.stop_motor = False
        # setup GPIO
        gpio.setup(self.direction_pin, gpio.OUT)
        gpio.setup(self.step_pin, gpio.OUT)
        gpio.output(self.direction_pin, clockwise)

        if self.mode_pins != False:
            gpio.setup(self.mode_pins, gpio.OUT)

        try:
            # dict resolution
            self.resolution_set(steptype)
            time.sleep(initdelay)

            for i in range(steps):
                if self.stop_motor:
                    raise StopMotorInterrupt
                else:
                    gpio.output(self.step_pin, True)
                    time.sleep(stepdelay)
                    gpio.output(self.step_pin, False)
                    time.sleep(stepdelay)
                    if verbose:
                        print("Steps count {}".format(i+1), end="\r", flush=True)

        except KeyboardInterrupt:
            print("User Keyboard Interrupt : RpiMotorLib:")
        except StopMotorInterrupt:
            print("Stop Motor Interrupt : RpiMotorLib: ")
        except Exception as motor_error:
            print(sys.exc_info()[0])
            print(motor_error)
            print("RpiMotorLib  : Unexpected error:")
        else:
            # print report status
            if verbose:
                print("\nRpiMotorLib, Motor Run finished, Details:.\n")
                print("Motor type = {}".format(self.motor_type))
                print("Clockwise = {}".format(clockwise))
                print("Step Type = {}".format(steptype))
                print("Number of steps = {}".format(steps))
                print("Step Delay = {}".format(stepdelay))
                print("Intial delay = {}".format(initdelay))
                print("Size of turn in degrees = {}"
                      .format(degree_calc(steps, steptype)))
        finally:
            # cleanup
            gpio.output(self.step_pin, False)
            gpio.output(self.direction_pin, False)
            if self.mode_pins != False:
                for pin in self.mode_pins:
                    gpio.output(pin, False)

class StopMotorInterrupt(Exception):
    """ Stop the motor """
    pass