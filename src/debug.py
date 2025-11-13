from pantograph_control.pantograph import *
import numpy as np
from time import sleep

joint1_config = JointConfig(
    17, 22, 27, 1600, 10
)

joint2_config = JointConfig(
    10, 11, 9, 1600, 10
)

joint3_config = JointConfig(
    5, 13, 6, 1600, 90
)

gripper_config = GripperConfig(12)

joint1 = Joint(joint1_config)
joint2 = Joint(joint2_config)
joint3 = Joint(joint3_config)
gripper = Gripper(gripper_config, 50, 0)

pantograph = Pantograph(PantographConfig(joint1, joint2, joint3, gripper,
                                         15, 17, 17, 15, 11,
                                         P1=np.array([0, 0]), P5=np.array([-11, 0])))

pantograph.calibrate_temp()
pantograph.joint1.stepper.speed = 20
pantograph.joint2.stepper.speed = 20
pantograph.z_stage.stepper.speed = 120

while True:

    x = input('(demo) >> ')

    match x:

        case 'p':

            points = [
                (15, 16),
                (-26, 16),
                (15, 16),
                (-26, 16),
                (15, 16)
            ]

            for point in points:

                print(f'Moving to {point}')
                pantograph.moveto(np.array([point[0], point[1]]))
        
        case 'z':
            pantograph.move_z(4000, True)
            sleep(0.5)
            pantograph.move_z(4000, False)

        case 'g':
            pantograph.gripper.open()
            sleep(0.5)
            pantograph.gripper.close()
