import numpy as np

LINKS = {
    "L1": 5,
    "L2": 5, 
    "L3": 5, 
    "L4": 5, 
    "L5": 2
}

# TODO: Implement all trajectory points
# Project vec(stack_z_offset -> edge of petri) onto vec(stack_z_offset -> transfer peak) to get safety ensured waypoint
TRANSFER_OUT_ORIGIN = np.array([-0.3, 0.5, 0.02])
TRANSFER_IN_ORIGIN = np.array([0.3, 0.5, 0.02])

STACK_WAYPOINT_Z = 0.25 # meters
STACK_WAYPOINT_Z_OFFSET = STACK_WAYPOINT_Z + 0.02 # meters

# Stack points
STACK_OUT_FULL_ORIGIN = np.array([0, 0, 0])
STACK_IN_WASTE_ORIGIN = np.array([0, 0, 0])

STACK_OUT_EMPTY_ORIGIN = np.array([0, 0, 0])
STACK_IN_FULL_ORIGIN = np.array([0, 0, 0])


# Trajectory peaks to ensure no collision
TRAJ_TRANSFER_OUT_PEAK = np.array([-0.3, 0.5, 0.02])
TRAJ_TRANSFER_IN_PEAK = np.array([0.3, 0.5, 0.02])
TRAJ_OUT_FULL_PEAK = np.array([-0.1, 0.1, STACK_WAYPOINT_Z_OFFSET])
TRAJ_IN_WASTE_PEAK = np.array([-0.3, 0.15, STACK_WAYPOINT_Z_OFFSET])
TRAJ_OUT_EMPTY_PEAK = np.array([0.3, 0.15, STACK_WAYPOINT_Z_OFFSET])
TRAJ_IN_FULL_PEAK = np.array([0.1, 0.1, STACK_WAYPOINT_Z_OFFSET])

# pantograph class configuration variables
ENA_PIN_1 = 17 # stepper 1
PUL_PIN_1 = 27
DIR_PIN_1 = 12
ENA_PIN_2 = 13 # stepper 2
PUL_PIN_2 = 16
DIR_PIN_2 = 19
ENA_PIN_3 = 5 # stepper 3
PUL_PIN_3 = 6
DIR_PIN_3 = 7
STEPS_PER_REV = 1600 # common stepper config
SPEED = 60
SERVO_PIN = 11 # servo
FREQUENCY = 50
MIN_DUTY = 2
MAX_DUTY = 12
RANGE_OF_MOTION = 180




