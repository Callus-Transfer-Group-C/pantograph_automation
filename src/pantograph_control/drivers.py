#
# This file will contain the raspberry pi <-> hardware interfaces for the stepper motors,
# servo motors, and camera(s)
#
# The stepper motor driver will need to be position controlled. This means that we will need
# to have a calibration mechanism built in to the driver that can be accessed through the
# 'Calibrate' task


from time import sleep
import RPi.GPIO as GPIO
import math

class Stepper(object):

    def __init__(self, enable:int, dir:int, pulse:int, steps_per_rev:int=1600, speed:int=60) -> None:
        '''Initialize the motor driver instance.

        Args:
            enable : int
                GPIO pin number or control object used to enable/disable the motor driver.
            dir : int
                GPIO pin number or control object used to set the motor direction.
            pulse : int
                GPIO pin number or control object used to send step/pulse signals. 1 pulse = 1 step.
            steps_per_rev : int, optional
                Number of microsteps per full revolution. Defaults to 1600.
            speed : int | float, optional
                Motor speed in revolutions per minute (RPM). Defaults to 60.
        '''
        self.steps_per_rev = steps_per_rev
        self.position = 0 # Position in radians

        self.ENA = enable
        self.DIR = dir
        self.PUL = pulse

        self.speed = speed # in rpm

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PUL, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.output(self.DIR, GPIO.HIGH)
        GPIO.output(self.PUL, GPIO.HIGH)

        self.enable()
        return

        
    def enable(self) -> None:
        GPIO.output(self.ENA, GPIO.HIGH)
        return
    
    def direction(self, direction:bool=True) -> None:
        ''' Sets the motor direction
            
            direction : bool
                The direction to rotate. True is forward, False is reverse
        '''

        val = GPIO.HIGH if direction else GPIO.LOW

        GPIO.output(self.DIR, val)
        return
    
    def pulse(self, delay):
        ''' Pulses the pulse pin once with a specified delay.
        
            Args:
                delay : float or int
                    seconds per GPIO output
                    = seconds per pulse/2'''
        print(delay)
        GPIO.output(self.PUL, GPIO.LOW)
        sleep(delay)
        GPIO.output(self.PUL, GPIO.HIGH)
        sleep(delay)

        return

    def step(self, steps:int, direction:bool=True) -> None:
        ''' Steps the stepper motor a certain number of steps in a direction.
        
            Args:
                steps : int
                    The number of steps to rotate
                direction : bool
                    The direction to rotate. True is forward, False is reverse
            
            Calculates delay based on speed and steps per rotation
        '''

        delay = 0.5 * 60 / (self.steps_per_rev * self.speed) # seconds per pulse
        print(delay)
        
        for step in range(steps):
            GPIO.output(self.PUL, GPIO.LOW)
            sleep(delay)
            GPIO.output(self.PUL, GPIO.HIGH)
            sleep(delay)
    
    def cleanup(self):
        GPIO.cleanup()




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
