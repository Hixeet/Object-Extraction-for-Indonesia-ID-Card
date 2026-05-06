import numpy as np
import cv2

def preprocess_image(image):
    # Split the image into blue, green, and red channels
    b, g, r = cv2.split(image)

    # Filter Gaussian
    blurred_frame_b = cv2.GaussianBlur(b, (5, 5), 1)
    blurred_frame_r = cv2.GaussianBlur(r, (5, 5), 1)

    # Thresholding the blue channel
    _, blue_threshold = cv2.threshold(blurred_frame_b, 255, 255,  cv2.THRESH_BINARY + cv2.THRESH_OTSU )

    # Thresholding the red channel
    _, red_threshold = cv2.threshold(blurred_frame_r, 200, 255, cv2.THRESH_BINARY)

    # Combine blue and red thresholds using bitwise OR
    combined_threshold = cv2.bitwise_or(blue_threshold, red_threshold)

    # Make the same pixels between red and blue thresholds become 0 (black)
    same_pixels = cv2.bitwise_and(blue_threshold, red_threshold)
    combined_threshold = cv2.subtract(combined_threshold, same_pixels)

    return b, g, r, blue_threshold, red_threshold, combined_threshold