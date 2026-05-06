def find_nearest_coordinates(image_array):
    # Periksa ukuran gambar
    height, width = image_array.shape 

    # Inisialisasi variabel
    min_x_0 = width
    min_y_0 = height
    min_x_hw = width
    min_y_hw = height
    min_x_h0 = width
    min_y_h0 = 0
    min_x_0w = width
    min_y_0w = 0

    # (0,0)
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

    # (height,width)
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

    # (0,width)
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

    # (height,0)
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