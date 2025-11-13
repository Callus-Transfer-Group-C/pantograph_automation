# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 David Alexander and Sudikshya Shrestha
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:
#   David Alexander
#   Sudikshya Shrestha

from time import sleep
import RPi.GPIO as GPIO

class Stepper(object):
    MIN_PULSE_DELAY = 0.0005

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
        self.position = 0 # Position in degrees
        
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
        ''' Enables the stepper motor. '''
        GPIO.output(self.ENA, GPIO.HIGH)
        return

    def disable(self) -> None:
        ''' Disable the stepper motor. '''
        GPIO.output(self.ENA, GPIO.LOW)
        return
    
    def direction(self, direction:bool=True) -> None:
        ''' Sets the motor direction.
            
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
                    = seconds per pulse/2
            
            Raises:
                ValueError when delay is less than hardcoded minimum
        '''
        
        if delay < self.MIN_PULSE_DELAY: raise ValueError(
            f'Calculated delay {delay} is less than minimum pulse delay{self.MIN_PULSE_DELAY}')

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

        self.direction(direction)
        
        for _ in range(steps):
            GPIO.output(self.PUL, GPIO.LOW)
            sleep(delay)
            GPIO.output(self.PUL, GPIO.HIGH)
            sleep(delay)
    
    def cleanup(self):
        GPIO.cleanup()




class Servo:
    def __init__(self, 
            servo_pin:int,
            frequency:float=50,
            min_duty:int=2,
            max_duty:int=12,
            range_of_motion:int=180) -> None:
        ''' Initializes the Servo interface. 
            
            Args
                servo_pin (int): GPIO pin number of the servo signal
                frequency (int or float): PWM frequency for the servo signal
                min_duty (int): The duty cycle that sends the servo to its zero position
                max_duty (int): The duty cycle that sends the servo to its maximum position
                range of motion (int, degrees): The range of motion of the servo in degrees
            
            Raises
                AssertionError:
                    min_duty greater than or equal to max_duty
                    range_of_motion less than zero
        '''
        assert max_duty > min_duty , f'min_duty was set to {min_duty} which is greater than max_duty {max_duty}'
        assert range_of_motion > 0 , f'the range of motion was set to {range_of_motion} which is less than or equal to zero'

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servo_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(servo_pin, frequency)  # 50Hz for servo
        self.pwm.start(0)
        self.position = 0
        self.servo_pin = servo_pin
        self.min_duty = min_duty
        self.max_duty = max_duty
        self.range_of_motion = range_of_motion
        return
    
    def set_position(self, angle:float, delay:int=0.2) -> int:
        ''' Sets the current position of the servo
        
            Args
                angle (int or float): target angle for the servo motor

            Raises
                AssertionError:
                    angle outside range of motion'''

        assert angle <= self.range_of_motion and angle >= 0 , f'Angle must be between {0} and {self.range_of_motion}'

        duty = self.min_duty + (angle / (self.range_of_motion / (self.max_duty - self.min_duty)))
        GPIO.output(self.servo_pin, True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(delay)
        GPIO.output(self.servo_pin, False)
        self.pwm.ChangeDutyCycle(0)
        self.position = angle
        return

    def get_position(self) -> float:
        ''' Gets the current position of the servo
         
            Returns:
                position (int): The current position of the servo '''
        return self.position

    def zero(self):
        ''' '''
        self.position = 0
        return

    def cleanup(self):
        ''' Cleanup GPIO pins '''
        self.pwm.stop()
        GPIO.cleanup()
        return
