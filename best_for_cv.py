from ultralytics import YOLO
import cv2
import numpy as np
from math import sqrt
from maths import funct
model = YOLO('best.pt')

name = input('Введите путь до изображения: ')
image = cv2.imread(name)


results = model.predict(image, save=True, project='results', name='img', show_conf=False, show_labels=False, verbose=False, show_boxes=False, imgsz=(1088, 2048))


class_colors = {
    0: (0, 0, 255),
    1: (0, 255, 0),
    2: (255, 0, 0)
}

result_image = image.copy()
ans = image.copy()

result_image = cv2.multiply(result_image, np.array([0.5]))



for result in results:
    if result.masks is not None:
        for mask, cls in zip(result.masks.xy, result.boxes.cls):
            polygon = np.array(mask, dtype=np.int32)
            cv2.fillPoly(result_image, [polygon], class_colors[int(cls)])

result_image = cv2.medianBlur(result_image, 9)
img = result_image.copy()

blue_channel = img[:, :, 0]
red_channel = img[:, :, 2]
green_channel = img[:, :, 1]

blue_channel =cv2.medianBlur(blue_channel, 9)
green_channel =cv2.medianBlur(green_channel, 9)
red_channel =cv2.medianBlur(red_channel, 9)




_, thresh_red = cv2.threshold(red_channel, 254, 255, cv2.THRESH_BINARY_INV)


_, thresh_green = cv2.threshold(green_channel, 254, 255, cv2.THRESH_BINARY_INV)


_, thresh_blue = cv2.threshold(blue_channel, 254, 255, cv2.THRESH_BINARY_INV)



contours_blue, _ = cv2.findContours(thresh_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_red, _ = cv2.findContours(thresh_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours_green, _ = cv2.findContours(thresh_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


contour_blue = [i for i in contours_blue if 1000 < cv2.contourArea(i) < 1225089.0][0]
contour_green = [i for i in contours_green if 1000 < cv2.contourArea(i) < 1225089.0][0]


all_pixels = []
for k in range(0, len(contour_blue)):
    all_pixels.append(contour_blue[k])

try:
    yn_b, xn_b = filter(lambda x: x[1] + x[0] == min([sum(i[0]) for i in all_pixels]), [i[0] for i in all_pixels])
    if type(yn_b) == np.ndarray:
        yn_b, xn_b = yn_b[1], xn_b[0]
except:
    yn_b, xn_b =list(filter(lambda x: x[1] + x[0] == min([sum(i[0]) for i in all_pixels]), [i[0] for i in all_pixels]))[len(list(
        filter(lambda x: x[1] + x[0] == min([sum(i[0]) for i in all_pixels]), [i[0] for i in all_pixels]))) // 2]

yw_b, xw_b = filter(lambda x: x[0]==min([i[0][0] for i in all_pixels]), [i[0] for i in all_pixels])
if type(yw_b) == np.ndarray:
    yw_b, xw_b = yw_b[1], xw_b[0]
ys_b, xs_b = filter(lambda x: x[1]==max([i[0][1] for i in all_pixels]), [i[0] for i in all_pixels])
if type(ys_b) == np.ndarray:
    ys_b, xs_b = ys_b[1], ys_b[0] #!
di = {}
for k in range(0, len(contour_blue)):
    if contour_blue[k][0][1] < yn_b + 20 and contour_blue[k][0][0] > xs_b - 20:
        q = sqrt((contour_blue[k][0][0] - xn_b)**2 + (contour_blue[k][0][1] - yn_b)**2)
        w = sqrt((contour_blue[k][0][0] - xs_b)**2 + (contour_blue[k][0][1] - ys_b)**2)
        if not di.get(q+w):
            di[sqrt((contour_blue[k][0][0] - xs_b)**2 + (contour_blue[k][0][1] - ys_b)**2) + sqrt((contour_blue[k][0][0] - xn_b)**2 + (contour_blue[k][0][1] - yn_b)**2)] = list(contour_blue[k][0])
ye_b, xe_b = di[max(list(di.keys()))][1], di[max(list(di.keys()))][0]


all_pixels = []
for j in range(0, len(contour_green)):
    all_pixels.append(contour_green[j])


yn_g, xn_g = filter(lambda x: x[1] + x[0] == min([sum(i[0]) for i in all_pixels]), [i[0] for i in all_pixels])

if type(yn_g) == np.ndarray:
    yn_g, xn_g = yn_g[1], xn_g[0]


yw_g, xw_g = filter(lambda x: x[0]==min([i[0][0] for i in all_pixels]), [i[0] for i in all_pixels])
if type(yw_g) == np.ndarray:
    yw_g, xw_g = yw_g[1], xw_g[0]
ys_g, xs_g = filter(lambda x: x[1]==max([i[0][1] for i in all_pixels]), [i[0] for i in all_pixels])
if type(ys_g) == np.ndarray:
    ys_g, xs_g = ys_g[1], ys_g[0] #!
ye_g, xe_g = filter(lambda x: x[0]==max([i[0][0] for i in all_pixels]), [i[0] for i in all_pixels])
ye_g, xe_g = 420, 1260
if type(ye_g) == np.ndarray:
    ye_g, xe_g = ye_g[1], ye_g[0] #!



print(funct([(xs_b, ys_b), (xw_b, yw_b), (xs_g, ys_g), (xw_g, yw_g)], [(xs_b, ys_b), (xn_b, yn_b), (xw_b, yw_b), (xe_b, ye_b)], [(xs_g, ys_g), (xn_g, yn_g), (xw_g, yw_g), (xe_g, ye_g)], [xs_g, ys_g, xw_g, yw_g]))
