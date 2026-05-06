import numpy as np
import cv2

def apply_erosion(thresholded_image, kernel_size):
    # Define the kernel for erosion
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    # Apply erosion on the thresholded image
    eroded_image = cv2.erode(thresholded_image, kernel, iterations=1)

    return eroded_image