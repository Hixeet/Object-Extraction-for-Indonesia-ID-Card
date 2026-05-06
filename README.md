## Demo

![Image](![Uploading Black and White Simple Portfolio Presentation.png…]()
)
Full Video: aa

---

## Features

* Color-based object detection using blue and red channels
* Image segmentation with Gaussian Blur, thresholding, and morphological operations
* Main object extraction based on the largest contour
* Automatic cropping of the detected object region
* Automatic rotation to correct image orientation
* Parameter adjustment based on lighting conditions (simple adaptive thresholding)
* Corner detection from multiple directions
* Perspective transformation to straighten the object (document-like scanning)
* Result validation to determine whether transformation is necessary

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Hixeet/Object-Extraction-for-Indonesia-ID-Card.git
cd Object-Extraction-for-Indonesia-ID-Card
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Example dependencies:

```text
opencv-python
numpy
```

---

## How It Works

1. **Image Input**
   The system reads an input image using OpenCV.

2. **Channel Separation**
   The image is split into **Blue, Green, and Red channels** for color-based analysis.

3. **Preprocessing**

   * Gaussian Blur to reduce noise
   * Thresholding on blue (Otsu) and red (manual) channels
   * Mask combination to isolate object regions

4. **Noise Reduction**
   Morphological erosion is applied to remove small noise.

5. **Object Detection**

   * Contours are detected from the thresholded image
   * The **largest contour** is selected as the main object

6. **Cropping & Alignment**

   * Bounding box is computed
   * Object is cropped from the original image
   * Automatic rotation is applied if needed

7. **Adaptive Processing**
   Processing parameters are adjusted based on the average intensity of the blue channel.

8. **Corner Detection**

   * Nearest white pixels are detected from four directions
   * Points are refined based on pixel intensity and position
   * Used to estimate object corners

9. **Perspective Transformation**

   * Uses `cv2.getPerspectiveTransform`
   * Warps the object into a normalized rectangular view (900x600)

10. **Final Output**

   * If the object is already aligned original image is used
   * Otherwise transformed image is displayed

---

## Notes

* This method relies heavily on object color (especially blue and red)
* Performance may decrease under extreme lighting conditions
* Some parts use manual pixel loops and can be optimized with NumPy
* Suitable for document-like or planar object preprocessing
