import cv2
import numpy as np
from numpy.typing import NDArray
import os

# CV Pipeline (high-level) (from ChatGPT)
# 1. Blur slightly (reduce noise / specular highlights).
# 2. Convert to a color space (HSV or Lab) where green separates well from the gray background.
# 3. Threshold the green color to build a binary mask.
# 4. Clean mask with morphological open/close.
# 5. Find connected components / contours.
# 6. For each component compute centroid (or fit a circle) and optionally filter by size and circularity.
# 7. Build arr = np.vstack([x_pixels, y_pixels, np.full(n, z)]) → shape (3, n).
# TODO: Camera <-> pi interface
# https://github.com/raspberrypi/picamera2/tree/main
#
# TODO: Build CV pipeline

class Camera:

    def __init__(self, position: NDArray[np.float64]):
        ''' Docstring for camera class
        '''

        assert position.shape == (3,), "Must be a point in eucelidean space"

        self.position = position

        self.next_image = NDArray[np.float64]
        self.__is_next_image = False

        self.points_remaining = 0
        self.points = NDArray[np.float64]
        self.next_point = NDArray[np.float64]
        self.__is_next_point = False

        pass

    def get_next_point(self, closest_to: NDArray[np.float64]) -> None:
        """
        Updates self.next_point with the the closest point to a given point.

        Args:
            closest_to (np.ndarray): The input point used to find its nearest neighbor

        Raises:
            Exception: There is already a next point available
        """

        assert self.__is_next_point == False, "There is already a next point available"

        x = 0
        y = 0

        self.next_point = np.array([x, y, self.position[2]]) + self.position

        self.__is_next_point == True
        return

    def get_image(self) -> None:
        """
        Updates self.next_image with next image from a raspberry pi camera.

        Raises:
            Exception: Raised when camera connection fails
            Exception: Raised when there is already an image available
        """

        assert self.__is_next_image == False, "There is already a next image available"

        self.next_image = self.take_picture()

        self.__is_next_image == True

        return 
    
    def get_points(self) -> None:
        """
        Updates self.points with next image from a raspberry pi camera.
        """
        
        return

    def take_picture(self, filepath:str=None) -> NDArray[np.float64]:
        """
        Takes a picture on the pi camera and returns the resulting np.ndarray

        Args:
            filepath (str, optional): Filepath to which the image will be saved, \
                                      by default will not save the image at all

        Raises:
            Exception: Raised when camera connection fails
            Exception: Raised when a picture cannot be taken for some reason

        Seperating this method from get_image allows photos to be saved externally
        without interfering with the CV pipeline sequence
        """

        if not filepath:
            # Add interface to save the image to a filepath if requested
            pass

        return np.ndarray(np.float64)