import numpy as np
from scipy.interpolate import make_interp_spline, make_smoothing_spline

class Trajectory:
    def __init__(self, waypoints, duration):
        """
        waypoints: np.array of shape (N, d)
            N = number of points
            d = dimension of each point (e.g., 2D, 3D, ...)

        duration: total trajectory time in seconds
        """
        # parameter u from 0 to 1
        self.duration = duration
        self.waypoints = waypoints

    def evaluate(self, t):
        return
    
class SplineTrajectory(Trajectory):

    def __init__(self, waypoints, duration):
        super().__init__(waypoints, duration)

        # Non real time trajectory generation
        N, d = waypoints.shape
        u = np.linspace(0, 1, N)
        self.splines = [make_interp_spline(u, waypoints[:, i], bc_type="clamped") for i in range(d)]
    
    def evaluate(self, t):
        # clamp
        t = np.clip(t, 0, self.duration)
        u = t / self.duration
        return np.array([s(u) for s in self.splines])