import numpy as np
from numpy.typing import NDArray
from scipy.interpolate import make_interp_spline, make_smoothing_spline

class Trajectory:
    def __init__(self, waypoints: NDArray[np.float64], duration):
        self.duration = duration
        self.waypoints = waypoints

    def evaluate(self, time_) -> NDArray[np.float64]:
        # No docstring needed here
        
        raise NotImplementedError("Subclasses must implement the 'evaluate' method")
    
class SplineTrajectory(Trajectory):
    """
    Generates a smooth trajectory using spline interpolation through given waypoints.

    Attributes:
        splines (list): List of spline objects, one for each dimension.
        duration (float): Total duration of the trajectory.

    Methods:
        evaluate(time_): Evaluates the trajectory at the specified time, returning the interpolated position.
    """

    def __init__(self, waypoints, duration):
        """
        Args:
            waypoints (np.ndarray): Array of shape (N, d) representing N waypoints in d-dimensional space.
            duration (float): Total duration of the trajectory.
        """
        super().__init__(waypoints, duration)

        # Non real time trajectory generation
        N, d = waypoints.shape
        u = np.linspace(0, 1, N)
        self.splines = [make_interp_spline(u, waypoints[:, i], bc_type="clamped") for i in range(d)]
    
    def evaluate(self, time_) -> NDArray[np.float64]:
        """
        Evaluates the trajectory at a given time.

        Parameters:
            time_ (float or array-like): The time(s) at which to evaluate the trajectory. 
            Values are clamped between 0 and the trajectory duration.

        Returns
            result (np.ndarray): The evaluated trajectory point(s) as a NumPy array of floats.
        """

        # clamp
        time_ = np.clip(time_, 0, self.duration)
        u = time_ / self.duration
        return np.array([s(u) for s in self.splines])
    
class LinearTrajectory(Trajectory):
    # TODO: Linear trajectory implementation

    def __init__(self, waypoints, duration):
        super().__init__(waypoints, duration)

        raise NotImplementedError("The LinearTrajectory subclass has not yet been implemented")