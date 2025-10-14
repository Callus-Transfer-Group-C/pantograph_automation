import numpy as np

LINKS = {
    "L1": 5,
    "L2": 5, 
    "L3": 5, 
    "L4": 5, 
    "L5": 2
}

# TODO: Project vec(stack_z_offset -> edge of petri) onto vec(stack_z_offset -> transfer peak) to get safety ensured waypoint
TRANSFER_OUT_ORIGIN = np.array([-0.3, 0.5, 0.02])
TRANSFER_IN_ORIGIN = np.array([0.3, 0.5, 0.02])

STACK_WAYPOINT_Z = 0.25 # meters
STACK_WAYPOINT_Z_OFFSET = STACK_WAYPOINT_Z + 0.02 # meters

# Stack points
# TODO: Confirm semantic clarity
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


