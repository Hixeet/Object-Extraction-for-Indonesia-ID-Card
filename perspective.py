import cv2
import numpy as np

def apply_perspective(resized_image, pts, pts1, pts2, pts3):
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    matrix2 = cv2.getPerspectiveTransform(pts,pts2)
    matrix3 = cv2.getPerspectiveTransform(pts3,pts2)

    final = cv2.warpPerspective(resized_image, matrix, (900, 600))
    final2 = cv2.warpPerspective(resized_image, matrix2, (900, 600))
    final3 = cv2.warpPerspective(resized_image, matrix3, (900, 600))

    return final, final2, final3