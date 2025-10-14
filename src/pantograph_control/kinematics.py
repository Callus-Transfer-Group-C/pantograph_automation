import numpy as np
from numpy.typing import NDArray
from typing import Tuple

def compute_joint_angles(
    a1: float, a2: float, a3: float, a4: float, a5: float,
    P1: NDArray[np.float64], P3: NDArray[np.float64], P5: NDArray[np.float64]
) -> Tuple[float, float]:
    # TODO: Update url with link
    # TODO: Add ValueError test
    """
    Compute joint angles given a pantograph end point. Follows the coordinate system and ik equations
    detailed in this paper: <URL>

    Args:
        a1, a2, a3, a4, a5 (float or int): The link lengths of the pantograph
        P1, P5 (float or int): The xy space location of the base joints
        P3 (np.array): The xy cartesian location of the end effector P3

    Returns:
        theta1, theta5: The base joint angles in radians

    Raises:
        OutOfBoundsException: If P3 is out of reach of the end effector.
        ValueError: If the distance between P1 and P5 != a5
    """

    try:
        alpha1, beta1, alpha5, beta5 = _compute_pentangles(a1, a2, a3, a4, a5, P1, P3, P5)
    except Exception:
        raise OutOfBoundsException(P3)
    
    if not (alpha1 > 0 and alpha5 > 0 and beta1 > 0 and beta5 > 0): 
        raise OutOfBoundsException(P3,
            f"Invalid angles. \n alpha1: {alpha1} \n alpha5: {alpha5} \n beta1: {beta1} \n beta5: {beta5} \n for point P3")
    
    if not (_dist(P1, P5) == a5):
        raise ValueError(f"P1: {P1} and P5: {P5} are further apart than the length of a5: {a5}")

    theta1 = _compute_theta1(alpha1, beta1)

    theta5 = _compute_theta5(alpha5, beta5)

    return theta1, theta5

def compute_end_point(
    a1: float, a2: float, a3: float, a4: float, a5: float,
    P1: NDArray[np.float64], P5: NDArray[np.float64],
    theta1: float, theta5: float
) -> NDArray[np.float64]:
    """
    Compute joint angles given a pantograph end point. Follows the coordinate system and ik equations\n
    detailed in this paper: <URL>

    Args:
        a1, a2, a3, a4, a5 (float or int): The link lengths of the pantograph
        P1, P5 (float or int): The xy space location of the base joints
        theta1, theta5: The base joint angles in radians

    Returns:
        P3 (np.array): The xy cartesian location of the end effector P3

    Raises:
        OutOfBoundsException: If P3 is out of reach of the end effector.
        ValueError: If the distance between P1 and P5 != a5
    """
    # TODO: Update url

    if not (_dist(P1, P5) == a5):
        raise ValueError(f"P1: {P1} and P5: {P5} are further apart than the length of a5: {a5}")

    # TODO: Forward kinematics for the pantograph. Also needs appropriate tests in test_ik.py

    P3 = np.array([0.0, 0.0])

    return P3

def _compute_pentangles(a1, a2, a3, a4, a5, P1, P3, P5):

    alpha1 = np.arccos((np.pow(a1, 2) - np.pow(a2, 2) + np.pow(_dist(P1, P3), 2)) /
                       (2*a1*_dist(P1, P3)))
    
    beta1 = np.atan2(P3[1], -P3[0])

    alpha5 = np.arccos((np.pow(a4, 2) - np.pow(a3, 2) + np.pow(_dist(P5, P3), 2)) /
                       (2*a4*_dist(P5, P3)))

    beta5 = np.atan2(P3[1], P3[0] + a5)

    return alpha1, beta1, alpha5, beta5

def _dist(P1, P2):
    return np.linalg.norm(P1 - P2)

def _compute_theta1(alpha1, beta1):

    return np.pi - alpha1 - beta1

def _compute_theta5(alpha5, beta5):

    return alpha5 + beta5

class OutOfBoundsException(Exception):
    """Raised when a point lies outside the valid bounds."""
    
    def __init__(self, point=None, message="Point is out of bounds"):
        if point is not None:
            message = f"{message}: {point}"
        super().__init__(message)
        self.point = point
