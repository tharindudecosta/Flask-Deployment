import cv2
import numpy as np

def ace_color_constancy(image, threshold=0.1):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    l, a, b = cv2.split(lab)
    mean_l = np.mean(l)
    l = l - mean_l
    l = np.clip(l, -threshold * 255, threshold * 255)
    l = l + mean_l
    l = l.astype(a.dtype)
    l = cv2.normalize(l, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    adjusted_lab = cv2.merge([l, a, b])
    return cv2.cvtColor(adjusted_lab, cv2.COLOR_Lab2BGR)
