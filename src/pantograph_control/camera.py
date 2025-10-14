import gpiozero
import numpy as np

# TODO:
class Camera:

    def __init__(self, position: np._ArrayT):

        self.position = position
        pass

    def get_next_point(self) -> np._ArrayT:
        
        # Return some point in overall 
        return np.array([0, 0])