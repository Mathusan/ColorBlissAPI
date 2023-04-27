import numpy as np
import cv2
from PIL import Image

#Colour-space conversions
class Modify:


    @staticmethod
    def RGB_TO_LMS():
        #Matrix for the conversion of RGB colour-space to LMS colour-space
        return np.array([[17.8824, 43.5161, 4.11935],
                         [3.45565, 27.1554, 3.86714],
                         [0.0299566, 0.184309, 1.46709]]).T

    @staticmethod
    def LMS_TO_RGB() -> np.ndarray:
        #Matrix for the conversion of LMS colour-space to RGB colour-space
        return np.array([[0.0809, -0.1305, 0.1167],
                         [-0.0102, 0.0540, -0.1136],
                         [-0.0004, -0.0041, 0.6935]]).T

    @staticmethod
    def colour_correction_matrix(degree_of_protanopia, degree_of_deutranopia) -> np.ndarray:
        #Matrix for correcting colour blindness from LMS colour-space
        return np.array([[1 - degree_of_deutranopia/2, degree_of_deutranopia/2, 0],
                         [degree_of_protanopia/2, 1 - degree_of_protanopia/2, 0],
                         [degree_of_protanopia/4, degree_of_deutranopia/4, 1 - (degree_of_protanopia + degree_of_deutranopia)/4]]).T
        
        #degree_of_protanopia --> Protanomaly degree for colour correction. If 0, colour correction is only done for Deutranomally type.
        #degree_of_deutranopia --> Deutranomaly degree for colour correction. If 0, colour correction is only done for Protanomaly type.


#Functions to load the image
class LoadImage:

    @staticmethod
    def process_RGB(path):
        rgb_image = np.array(Image.open(path)) / 255
        return rgb_image

    @staticmethod
    def process_LMS(path):
        rgb_image = np.array(Image.open(path)) / 255
        lms_image = np.dot(rgb_image[:,:,:3], Modify.RGB_TO_LMS())
        return lms_image