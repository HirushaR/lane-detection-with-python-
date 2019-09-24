import cv2
import numpy as np
import matplotlib.pyplot as plt

def canny(image):
    gray = cv2.cvtColor(lane_img , cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray , (5 , 5) , 0)
    canny = cv2.Canny(blur , 50 , 150)
    return canny

img = cv2.imread('test_image.jpg')
lane_img = np.copy(img)
canny = canny(lane_img)
plt.imshow(canny)
plt.show()