import cv2
import numpy as np


def make_cordinates(image, line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*3/5)
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1, y1, x2, y2])

def canny(image):
    gray = cv2.cvtColor(frame , cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny
def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image

def avarage_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
       x1, y1, x2, y2 = line.reshape(4)
       parameter = np.polyfit((x1, x2), (y1, y2), 1)
       slope = parameter[0]
       intercept = parameter[1]
       if slope <0 :
           left_fit.append((slope, intercept))
       else:
           right_fit.append((slope, intercept))
    left_fit_avarage = np.average(left_fit, axis=0)
    right_fit_avarage = np.average(right_fit, axis=0)
    left_line = make_cordinates(image, left_fit_avarage)
    right_line = make_cordinates(image, right_fit_avarage)
    return np.array([left_line, right_line])



def regoin_of_interest(image):
    height = image.shape[0]
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
    ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

# img = cv2.imread('test_image.jpg')
# lane_img = np.copy(img)
# canny_image = canny(lane_img)
# croped_image = regoin_of_interest(canny_image)
# lines = cv2.HoughLinesP(croped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
# avarage_lines = avarage_slope_intercept(lane_img, lines)
# line_image = display_lines(lane_img, avarage_lines)
# combo_img = cv2.addWeighted(lane_img, 0.8, line_image, 1, gamma=1)
# cv2.imshow('result', canny_image)
# cv2.waitKey(0)

cap = cv2.VideoCapture("test2.mp4")
while(cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny(frame)
    croped_image = regoin_of_interest(canny_image)
    lines = cv2.HoughLinesP(croped_image , 2 , np.pi / 180 , 100 , np.array([]) , minLineLength=40 , maxLineGap=5)
    avarage_lines = avarage_slope_intercept(frame , lines)
    line_image = display_lines(frame , avarage_lines)
    combo_img = cv2.addWeighted(frame , 0.8 , line_image , 1 , gamma=1)
    cv2.imshow('result' , combo_img)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

