import numpy as np
import cv2
from preprocessing import preprocess_image
from erosion import apply_erosion
from coordinate_utils import find_nearest_coordinates
from perspective import apply_perspective

image = cv2.imread('testing_image_1.png') #For other image format like "jpg, jpeg, etc" or image not found in directory, using path from image

b, g, r, blue_threshold, red_threshold, combined_threshold = preprocess_image(image)

# Read the thresholded image
thresholded_image = combined_threshold

# Define the kernel size for erosion
kernel_size = 2

# Apply erosion
eroded_image = apply_erosion(thresholded_image, kernel_size)

# Find contours in the thresholded image
contours, _ = cv2.findContours(eroded_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Find the largest contour (blue region)
largest_contour = max(contours, key=cv2.contourArea)

# Create a mask of the largest contour
mask = np.zeros_like(b)
cv2.drawContours(mask, [largest_contour], 0, 255, -1)

# Apply the mask to the original image
result = cv2.bitwise_and(image, image, mask=mask)

# Find the bounding box of the blue region
x, y, w, h = cv2.boundingRect(largest_contour)

# Crop the image based on the bounding box
cropped_image = result[y:y+h, x:x+w]
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

b2, g2, r2 = cv2.split(resized_image)

mean_value_b = np.mean(resized_image[b2 > 0])
print("Mean Value B:", mean_value_b)

if 150 >= mean_value_b >= 100:
    blur_frame_b = cv2.GaussianBlur(b2, (5, 5), 1)
    blur_gray = cv2.GaussianBlur(resized_image, (5, 5), 1)
elif 200 >= mean_value_b >= 150:
    blur_frame_b = cv2.GaussianBlur(b2, (5, 5), 1)
    blur_gray = cv2.GaussianBlur(resized_image, (7, 7), 3)
else:
    blur_frame_b = b2
    blur_gray = cv2.GaussianBlur(resized_image, (5, 5), 1)

gray = cv2.cvtColor(blur_gray, cv2.COLOR_BGR2GRAY)

blur_frame_r = cv2.GaussianBlur(r2, (5, 5), 1)
blur_frame_g = cv2.GaussianBlur(g2, (5, 5), 1)

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
else:
    threshold_value = 126
    threshold_value_r = 190

_, crop_threshold_b = cv2.threshold(blur_frame_b, threshold_value, 255, cv2.THRESH_BINARY)
_, crop_threshold_r = cv2.threshold(blur_frame_r, threshold_value_r, 255,  cv2.THRESH_BINARY )
_, crop_threshold_g = cv2.threshold(blur_frame_g, 109, 255,  cv2.THRESH_BINARY )

# Apply thresholding
_, threshold_gray = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)

# Combine blue and red thresholds
combined_threshold2 = cv2.subtract(crop_threshold_b, crop_threshold_r)

# Remove same pixels
same_pixels = cv2.bitwise_and(crop_threshold_b, crop_threshold_r)
combined_threshold3 = cv2.subtract(combined_threshold2, same_pixels)

kernal = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
dilate = cv2.dilate(combined_threshold2, kernal, iterations=1)

hasil = np.array(dilate) 
hasil_coordinates = find_nearest_coordinates(hasil)

(min_x_0, min_y_0), (min_x_hw, min_y_hw), (min_x_0w, min_y_0w), (min_x_h0, min_y_h0) = hasil_coordinates

print("Koordinat Terdekat:")
print("Dari (0, 0):", (min_x_0, min_y_0))
print("Dari (height, width):", (min_x_hw, min_y_hw))
print("Dari (0, width):", (min_x_0w, min_y_0w))
print("Dari (height, 0):", (min_x_h0, min_y_h0))

image_array = dilate
height, width = image_array.shape

min_x_same_intensity = width
min_y_same_intensity = height
for x in range(width):
    for y in range(height):
        if image_array[y, x] == image_array[min_y_0, min_x_0]:
            sum_coordinates = x + y
            if sum_coordinates < min_x_same_intensity + min_y_same_intensity:
                min_x_same_intensity = x
                min_y_same_intensity = y

print(f"Koordinat terkecil dengan intensitas yang sama: ({min_x_same_intensity}, {min_y_same_intensity})")

min_x_same_intensity_w0 = min_x_0w 
min_y_same_intensity_w0 = min_y_0w
for x in range(min_x_0w-10, width):
    for y in range(min_y_0w+10, -1, -1):
        if image_array[y, x] == image_array[min_y_0w, min_x_0w]:
            sum_coordinates = (width - x) + y
            if sum_coordinates < (width - min_x_same_intensity_w0) + min_y_same_intensity_w0:
                min_x_same_intensity_w0 = x
                min_y_same_intensity_w0 = y

print(f"Koordinat terkecil dengan intensitas yang sama pada bagian kanan atas: ({min_x_same_intensity_w0}, {min_y_same_intensity_w0})")

min_x_same_intensity_h0 = min_x_h0 
min_y_same_intensity_h0 = min_y_h0
for x in range(min_x_h0+10, -1, -1):
    for y in range(min_y_h0-10, height):
        if image_array[y, x] == image_array[min_y_h0, min_x_h0]:
            sum_coordinates = x + (height - y)
            if sum_coordinates < min_x_same_intensity_h0 + (height - min_y_same_intensity_h0):
                min_x_same_intensity_h0 = x
                min_y_same_intensity_h0 = y

print(f"Koordinat terkecil dengan intensitas yang sama pada bagian kiri bawah: ({min_x_same_intensity_h0}, {min_y_same_intensity_h0})")

min_x_same_intensity_hw = min_x_hw 
min_y_same_intensity_hw = min_y_hw
for x in range(min_x_hw-10, width):
    for y in range(min_y_hw-10, height):
        if image_array[y, x] == image_array[min_y_hw, min_x_hw]:
            sum_coordinates = (width - x) + (height - y)
            if sum_coordinates < (width - min_x_same_intensity_hw) + (height - min_y_same_intensity_hw):
                min_x_same_intensity_hw = x
                min_y_same_intensity_hw = y

print(f"Koordinat terkecil dengan intensitas yang sama pada bagian kanan bawah: ({min_x_same_intensity_hw}, {min_y_same_intensity_hw})")

point1 = (min_x_0, min_y_0)
point2 = (min_x_0w, min_y_0w)
point3 = (min_x_h0, min_y_h0)
point4 = (min_x_hw, min_y_hw)

pointa = (min_x_same_intensity, min_y_same_intensity)
pointb = (min_x_same_intensity_w0, min_y_same_intensity_w0)
pointc = (min_x_same_intensity_h0, min_y_same_intensity_h0)
pointd = (min_x_same_intensity_hw, min_y_same_intensity_hw)

nonzero_coords = np.column_stack(np.where(image_array == 255))

points = ['c1', 'c2', 'c3', 'c4']
min_coordinate_sums = [float("inf")] * 4
min_coordinates = [None] * 4

for point_idx, point_name in enumerate(points[:4]):
    for y in range(height):
        for x in range(width):
            if threshold_gray[y, x] == 255:
                if point_name == 'c1':
                    coordinate_sum = x + y
                elif point_name == 'c2':
                    coordinate_sum = (width - x) + y
                elif point_name == 'c3':
                    coordinate_sum = x + (height - y)
                elif point_name == 'c4':
                    coordinate_sum = (width - x) + (height - y)
                else:
                    coordinate_sum = float("inf")
                
                if coordinate_sum < min_coordinate_sums[point_idx]:
                    min_coordinate_sums[point_idx] = coordinate_sum
                    min_coordinates[point_idx] = (x, y)

pointc1 = min_coordinates[0]
pointc2 = min_coordinates[1]
pointc3 = min_coordinates[2]
pointc4 = min_coordinates[3]

top_left = np.float32(pointa)
top_right = np.float32(pointb)
bottom_left = np.float32(pointc)
bottom_right = np.float32(pointd)

for point_name, coordinate in zip(points, min_coordinates):
    if coordinate is not None:
        print(f"Point {point_name} dengan nilai 255 dan jumlah koordinat terkecil:", coordinate)
        x, y = coordinate
        if point_name == 'c1' and x < 85 and y < 85:
            top_left = np.float32(pointc1)
        elif point_name == 'c2' and x > 815 and y < 85:
            top_right = np.float32(pointc2)
        elif point_name == 'c3' and x < 50 and y > 515:
            bottom_left = np.float32(pointc3)
        elif point_name == 'c4' and x > 815 and y > 515:
            bottom_right = np.float32(pointc4)

pts = np.float32([[pointa], [pointb], [pointc], [pointd]])
pts1 = np.float32([[point1], [point2], [point3], [point4]])
pts2 = np.float32([[0, 0], [900, 0], [0, 600], [900, 600]])
pts3 = np.float32([top_left, top_right, bottom_left, bottom_right])

matrix = cv2.getPerspectiveTransform(pts1,pts2)
matrix2 = cv2.getPerspectiveTransform(pts,pts2)
matrix3 = cv2.getPerspectiveTransform(pts3,pts2)

final = cv2.warpPerspective(resized_image, matrix, (900, 600))
final2 = cv2.warpPerspective(resized_image, matrix2, (900, 600))
final3 = cv2.warpPerspective(resized_image, matrix3, (900, 600))

test = np.array(blue_threshold)  
test_coordinates = find_nearest_coordinates(test)

(min_x_0, min_y_0), (min_x_hw, min_y_hw), (min_x_0w, min_y_0w), (min_x_h0, min_y_h0) = test_coordinates

height2, width2, channel = image.shape
tolerance = 1

if (
    min_x_0 <= tolerance and (min_y_0) <= tolerance and
    (width2 - min_x_hw )<= tolerance and (height2 - min_y_hw) <= tolerance and
    (width2 - min_x_hw )<= tolerance and (min_y_0) <= tolerance and
    min_x_0 <= tolerance and (height2 - min_y_hw) <= tolerance
):
    akhir = image  
else:
    akhir = final3

cv2.imshow('akhir',akhir)
cv2.waitKey(0)
