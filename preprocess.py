import numpy as np
import cv2

def preprocess_image(image):

    blurred_frame_b = cv2.GaussianBlur(image[:,:,0], (5, 5), 1)
    blurred_frame_r = cv2.GaussianBlur(image[:,:,2], (5, 5), 1)

    _, blue_threshold = cv2.threshold(blurred_frame_b, 255, 255,  cv2.THRESH_BINARY + cv2.THRESH_OTSU )
    _, red_threshold = cv2.threshold(blurred_frame_r, 200, 255, cv2.THRESH_BINARY)
    combined_threshold = cv2.subtract(blue_threshold, red_threshold)

    kernel = np.ones((2, 2), np.uint8)
    eroded_image = cv2.erode(combined_threshold, kernel, iterations=1)

    contours, _ = cv2.findContours(eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(largest_contour)
    crop_image = image[y:y+h, x:x+w]

    height, width, channels = crop_image.shape

    if width < height:
        rotated_image = cv2.rotate(crop_image, cv2.ROTATE_90_CLOCKWISE)
        rotated_height, rotated_width, _ = rotated_image.shape
        print("Gambar sudah dirotasi:", rotated_height, rotated_width)
    else:
        rotated_image = crop_image
        print("Tidak perlu merotasi gambar")
        
    resized_image = cv2.resize(rotated_image, (900, 600))

    mean_value_b = np.mean(resized_image[resized_image[:,:,0] > 0])
    print("Nilai rata-rata intensitas dari channel B pada KTP:", mean_value_b)

    return resized_image, mean_value_b, blue_threshold
