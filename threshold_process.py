import numpy as np
import cv2

def threshold_processing(resized_image, mean_value_b):

    if 150 >= mean_value_b >= 100:
        blur_frame_b = cv2.GaussianBlur(resized_image[:,:,0], (5, 5), 1)
        blur_gray = cv2.GaussianBlur(resized_image, (5, 5), 1)
    elif 200 >= mean_value_b >= 150:
        blur_frame_b = cv2.GaussianBlur(resized_image[:,:,0], (5, 5), 1)
        blur_gray = cv2.GaussianBlur(resized_image, (7, 7), 3)
    else:
        blur_frame_b = resized_image[:,:,0]
        blur_gray = cv2.GaussianBlur(resized_image, (5, 5), 1)

    gray = cv2.cvtColor(blur_gray, cv2.COLOR_BGR2GRAY)
    blur_frame_r = cv2.GaussianBlur(resized_image[:,:,2], (5, 5), 1)

    # Tentukan nilai threshold untuk kanal biru berdasarkan mean value
    if mean_value_b <= 95:
        threshold_value = 50
        threshold_value_r = 160
    elif 96 <= mean_value_b <= 115:
        threshold_value = 105
        threshold_value_r = 170
    elif 116 <= mean_value_b <= 145:
        threshold_value = 107
        threshold_value_r = 180
    elif 146 <= mean_value_b <= 160:
        threshold_value = 110
        threshold_value_r = 180
    else:
        threshold_value = 126
        threshold_value_r = 190

    _, crop_threshold_b = cv2.threshold(blur_frame_b, threshold_value, 255, cv2.THRESH_BINARY)
    _, crop_threshold_r = cv2.threshold(blur_frame_r, threshold_value_r, 255,  cv2.THRESH_BINARY )
    _, threshold_gray = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)

    combined_threshold2 = cv2.subtract(crop_threshold_b, crop_threshold_r)

    return combined_threshold2, threshold_gray
