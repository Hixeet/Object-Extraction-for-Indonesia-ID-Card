import numpy as np
import cv2

def find_nearest_coordinates(image_array):
    height, width = image_array.shape 

    min_x_0 = width
    min_y_0 = height
    min_x_hw = width
    min_y_hw = height
    min_x_h0 = width
    min_y_h0 = 0
    min_x_0w = width
    min_y_0w = 0

    x = 0
    y = 0
    while x < width and y < height:
        intensity = image_array[y, x]

        if intensity >= 255:
            if x < min_x_0:
                min_x_0 = x
                min_y_0 = y
            break
        x += 1
        y += 1

    x = width - 1
    y = height - 1
    while x >= 0 and y >= 0:
        intensity = image_array[y, x]

        if intensity >= 255:
            if x < min_x_hw:
                min_x_hw = x
                min_y_hw = y
            break
        x -= 1
        y -= 1

    x = width - 1
    y = 0
    while x >= 0 and y < height:
        intensity = image_array[y, x]

        if intensity >= 255:
            if x < min_x_0w:
                min_x_0w = x
                min_y_0w = y
            break
        x -= 1
        y += 1

    x = 0
    y = height - 1
    while x < width and y >= 0:
        intensity = image_array[y, x]

        if intensity >= 255:
            if x < min_x_h0:
                min_x_h0 = x
                min_y_h0 = y
            break
        x += 1
        y -= 1

    return (min_x_0, min_y_0), (min_x_hw, min_y_hw), (min_x_0w, min_y_0w), (min_x_h0, min_y_h0)


def get_final_image(resized_image, image, combined_threshold2, threshold_gray, blue_threshold):

    hasil_coordinates = find_nearest_coordinates(combined_threshold2)

    (min_x_0, min_y_0), (min_x_hw, min_y_hw), (min_x_0w, min_y_0w), (min_x_h0, min_y_h0) = hasil_coordinates

    image_array = combined_threshold2
    height, width = image_array.shape

    min_x_same_intensity = min_x_0
    min_y_same_intensity = min_y_0
    for x in range(min_x_0+10, 0, -1):
        for y in range(min_y_0+10, 0, -1):
            if image_array[y, x] == image_array[min_y_0, min_x_0]:
                sum_coordinates = x + y
                if sum_coordinates < min_x_same_intensity + min_y_same_intensity:
                    min_x_same_intensity = x
                    min_y_same_intensity = y

    min_x_same_intensity_w0 = min_x_0w 
    min_y_same_intensity_w0 = min_y_0w
    for x in range(min_x_0w-10, width):
        for y in range(min_y_0w+10, 0, -1):
            if image_array[y, x] == image_array[min_y_0w, min_x_0w]:
                sum_coordinates = (width - x) + y
                if sum_coordinates < (width - min_x_same_intensity_w0) + min_y_same_intensity_w0:
                    min_x_same_intensity_w0 = x
                    min_y_same_intensity_w0 = y

    min_x_same_intensity_h0 = min_x_h0 
    min_y_same_intensity_h0 = min_y_h0
    for x in range(min_x_h0+10, 0, -1):
        for y in range(min_y_h0-10, height):
            if image_array[y, x] == image_array[min_y_h0, min_x_h0]:
                sum_coordinates = x + (height - y)
                if sum_coordinates < min_x_same_intensity_h0 + (height - min_y_same_intensity_h0):
                    min_x_same_intensity_h0 = x
                    min_y_same_intensity_h0 = y

    min_x_same_intensity_hw = min_x_hw 
    min_y_same_intensity_hw = min_y_hw
    for x in range(min_x_hw-10, width, +1):
        for y in range(min_y_hw-10, height, +1):
            if image_array[y, x] == image_array[min_y_hw, min_x_hw]:
                sum_coordinates = (width - x) + (height - y)
                if sum_coordinates < (width - min_x_same_intensity_hw) + (height - min_y_same_intensity_hw):
                    min_x_same_intensity_hw = x
                    min_y_same_intensity_hw = y


    pointa = (min_x_same_intensity, min_y_same_intensity)
    pointb = (min_x_same_intensity_w0, min_y_same_intensity_w0)
    pointc = (min_x_same_intensity_h0, min_y_same_intensity_h0)
    pointd = (min_x_same_intensity_hw, min_y_same_intensity_hw)

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
            x, y = coordinate
            if point_name == 'c1' and x < 85 and y < 85:
                top_left = np.float32(pointc1)
            elif point_name == 'c2' and x > 815 and y < 85:
                top_right = np.float32(pointc2)
            elif point_name == 'c3' and x < 50 and y > 515:
                bottom_left = np.float32(pointc3)
            elif point_name == 'c4' and x > 815 and y > 515:
                bottom_right = np.float32(pointc4)

    pts = np.float32([[0, 0], [900, 0], [0, 600], [900, 600]])
    pts2 = np.float32([top_left, top_right, bottom_left, bottom_right])
    matrix = cv2.getPerspectiveTransform(pts2, pts)
    final = cv2.warpPerspective(resized_image, matrix, (900, 600))

    test_coordinates = find_nearest_coordinates(blue_threshold)
    (min_x_0, min_y_0), (min_x_hw, min_y_hw), (min_x_0w, min_y_0w), (min_x_h0, min_y_h0) = test_coordinates

    height2, width2, channel = image.shape

    if (
        min_x_0 <= 1 and (min_y_0) <= 1 and
        (width2 - min_x_hw )<= 1 and (height2 - min_y_hw) <= 1 and
        (width2 - min_x_hw )<= 1 and (min_y_0) <= 1 and
        min_x_0 <= 1 and (height2 - min_y_hw) <= 1
    ):
        akhir = image  
    else:
        akhir = final

    return akhir
