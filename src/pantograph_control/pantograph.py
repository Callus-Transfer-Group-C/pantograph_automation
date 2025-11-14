from dataclasses import dataclass
from . import drivers, kinematics
import math, threading
import numpy as np
from numpy.typing import NDArray
from typing import Tuple


@dataclass
class JointConfig:
    ''' Configuration data for Joint '''
    
    # Stepper configuration
    ENA_PIN:int
    PUL_PIN:int
    DIR_PIN:int
    STEPS_PER_REV:int=1600
    SPEED:float=60

    # TODO: Encoder configuration

@dataclass
class GripperConfig:
    ''' Configuration data for the Gripper '''
    SERVO_PIN:int # servo
    FREQUENCY:float = 50
    MIN_DUTY:int = 2
    MAX_DUTY:int = 12
    RANGE_OF_MOTION:float = 180


class Joint:
    
    def __init__(self, config:JointConfig):

        self.position = None        

        self.stepper = drivers.Stepper(
            config.ENA_PIN,
            config.DIR_PIN,
            config.PUL_PIN,
            config.STEPS_PER_REV,
            config.SPEED
        )

        # Option to add encoder later
        pass

    def zero(self):
        ''' Sets the current joint position index to zero '''
        self.position = 0
        return
    
    def set_position(self, position:float):
        ''' Sets the joint position
        
            Args
                position (int): The position in radians to which the joint should rotate
                
            Raises
                RuntimeError: When the joint is not calibrated (i.e. position is None)
        '''
        if self.position is None:
            raise RuntimeError('Calibrate the joint!\n(Hint: use Joint.zero() once the motor is at its zero position)')

        # Calculate neccessary angle change
        angle = position - self.get_position()

        # Calculate which direction to rotate
        direction = True if angle >= 0 else False

        # Calculate number of steps to rotate
        steps = int(self.__rad_to_steps(abs(angle)))

        # Rotate the stepper
        self.stepper.step(steps, direction)
        self.position = position # Change this later for feedback control

        return
    
    def get_position(self):
        ''' Gets the joint position
        
            Returns
                position: Current joint position in radians
        '''
        # Option to add reading from encoder in the future
        return self.position
    
    def __rad_to_steps(self, angle:float) -> int:
        ''' Converts the angle (in radians) to number of steps '''

        assert angle >= 0 , ' Error in __rad_to_steps: angle must be positive'

        return (angle * self.stepper.steps_per_rev) // (2 * math.pi)
     
    

class Gripper:

    def __init__(self, config:GripperConfig, angle_at_open:float, angle_at_closed:float):
        ''' Initialize the gripper
            
            Args
                config: The gripper hardware configuration data
                angle_at_open: The angle at which the gripper is all the way open
                angle_at_closed: The angle at which the gripper is all the way closed
        '''

        self.percent = None
        self.max_angle = angle_at_open
        self.min_angle = angle_at_closed
        
        self.main_servo = drivers.Servo(
            config.SERVO_PIN,
            config.FREQUENCY,
            config.MIN_DUTY,
            config.MAX_DUTY
        )

        # Option for secondary servo if neccessary

        pass
    
    def zero(self):
        ''' Sets the current gripper percent closed to zero (fully closed)'''
        self.percent = 0
        return
    
    def grip(self, percent:float=100):
        ''' Move the gripper to a percent open (default to all the way open)
        
            Args
                percent (float): a value from 0 to 100, 0 being closed and 100 being open
            
            Raises
                AssertionError: When percent is not between 0 and 100, inclusive
        '''
        assert percent >= 0 and percent <= 100 , f'Percentage {percent} must be between 0 and 100, inclusive!'

        self.main_servo.set_position(
            self.__percent_to_angle(percent),
            delay=(0.5 * percent / 100) # TODO: Calibrate max servo delay (right now at 0.5s)
        )
        return
    
    def open(self):
        ''' Open the gripper '''
        self.grip(100)
        return
    
    def close(self):
        ''' Close the gripper '''
        self.grip(0)
        return
    
    def __percent_to_angle(self, percent):
        ''' Convert a percentage to a gripper angle 
        
            Returns
                angle (percent): The angle to which the percentage corresponds to
        '''

        angle = percent/100 * (self.max_angle - self.min_angle)

        return angle

@dataclass
class PantographConfig:
    ''' Configuration data for Pantograph '''
    joint1:Joint
    joint2:Joint
    z_stage:Joint
    gripper:Gripper
    
    link_a1:float
    link_a2:float
    link_a3:float
    link_a4:float
    link_a5:float

    P1: NDArray[np.float64]
    P5: NDArray[np.float64]

class Pantograph:

    def __init__(self, config: PantographConfig) -> None:
        
        self.gripper = config.gripper
        self.joint1 = config.joint1
        self.joint2 = config.joint2
        self.z_stage = config.z_stage

        self.a1 = config.link_a1
        self.a2 = config.link_a2
        self.a3 = config.link_a3
        self.a4 = config.link_a4
        self.a5 = config.link_a5

        self.P1 = config.P1
        self.P5 = config.P5        
        pass

    def moveto(self, point: NDArray[np.float64]):
        
        theta1, theta2 = kinematics.compute_joint_angles(
            self.a1, self.a2, self.a3, self.a4, self.a5,
            self.P1, point, self.P5
        )

        
        thread1 = threading.Thread(target=self.joint1.set_position, args=(theta1, ))
        thread2 = threading.Thread(target=self.joint2.set_position, args=(theta2, ))

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        return
    
    def move_z(self, steps, direction):

        self.z_stage.stepper.step(steps, direction)

    def calibrate_temp(self):

       
        self.joint1.stepper.disable()
        self.joint2.stepper.disable()
        input(f"Press enter to zero joint1 >> ")
        self.joint1.zero()
        self.joint1.stepper.enable()
        self.joint2.stepper.enable()

        self.joint1.stepper.disable()
        self.joint2.stepper.disable()
        input(f"Press enter to set joint2 to pi/2 >> ")
        self.joint2.position = np.pi/2
        self.joint1.stepper.enable()
        self.joint2.stepper.enable()

        input(f"Press enter to zero z_stage >> ")
        self.z_stage.zero()

        self.joint2.set_position(np.pi/2)
        self.joint1.set_position(np.pi/4)
        self.joint2.set_position(3*np.pi/4)

    def cleanup(self):

        self.joint1.stepper.cleanup()
        self.joint2.stepper.cleanup()
        self.z_stage.stepper.cleanup()


    



