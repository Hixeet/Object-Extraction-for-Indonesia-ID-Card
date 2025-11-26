import numpy as np
import cv2

from preprocess import preprocess_image
from threshold_process import threshold_processing
from coordinate_process import get_final_image

image = cv2.imread("1.jpg")

resized_image, mean_value_b, blue_threshold = preprocess_image(image)

combined_threshold2, threshold_gray = threshold_processing(resized_image, mean_value_b)

final = get_final_image(resized_image, image, combined_threshold2, threshold_gray, blue_threshold)

cv2.imshow('akhir', final)
cv2.waitKey(0)
cv2.destroyAllWindows
