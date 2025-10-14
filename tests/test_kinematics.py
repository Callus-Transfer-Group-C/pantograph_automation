import pytest
import numpy as np
from pantograph_control.kinematics import compute_joint_angles, OutOfBoundsException

@pytest.mark.filterwarnings("ignore:invalid value encountered in arccos")
def test_out_of_bounds():

    a1 = a4 = 5
    a2 = a3 = 5
    a5 = 2

    P1 = np.array([0, 0])
    P5 = np.array([-a5, 0])

    # TODO: Test over a range of values know to be outside of the specified configuration
    x = 2
    y = 10

    P3 = np.array([x, y])

    with pytest.raises(OutOfBoundsException):
        compute_joint_angles(a1, a2, a3, a4, a5, P1, P3, P5)

