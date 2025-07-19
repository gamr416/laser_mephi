import math
import numpy as np


def sigma(a1, b1, a2 ,b2):
    s = abs(a1*b1 + a2*b2)/((math.sqrt(a1**2 + a2**2))*(math.sqrt(b1**2 + b2**2)))

    s = math.degrees(math.acos(s))

    return s

def focus(a):
    s1 = point_remaker(a[0][0],a[0][1],a[1][0],a[1][1])
    s2 = point_remaker(a[2][0],a[2][1],a[3][0],a[3][1])
    k1 = s1[0]
    b1 = s1[1]
    k2 = s2[0]
    b2 = s2[1]
    if k1 == k2:
        return None     
    x = (b2 - b1) / (k1 - k2)
    y = k1 * x + b1
    return (x, y)


def point_remaker(x1,y1,x2,y2):
    if x1 != x2:
        k = (y2 - y1) / (x2 - x1)
    else:
        return None
    b = y1 - k * x1

    return (k, b)


def find_angle(l):
    a = point_remaker(l[0][0],l[0][1],l[1][0],l[1][1])
    b = point_remaker(l[2][0],l[2][1],l[3][0],l[3][1])

    if a and b:

        return sigma(1,a[0],1,b[0])
    

def calculate(center1, center2, U):
    x = -(center1[0] - center2[0])
    y = -(center1[1] - center2[1])
    return [x/U,y/U]
  


def not_svo(a):
    s = math.sqrt((a[2]-a[0])**2 + (a[3]-a[1])**2)
    U = s/70 # 1 = ? мм
    return U


#for_angle = [(x,y),(x,y),(x,y),(x,y)] 4 points for 2 lines for angle
#for_plate = [(x,y),(x,y),(x,y),(x,y)]
#for_obj = [(x,y),(x,y),(x,y),(x,y)]
#for_koof = [x1,y1,x1,y1] 2 point of one edge to calculate S
def funct(for_angle,for_plate,for_obj,for_koof):
    angle = find_angle(for_angle)
    certain = calculate(focus(for_plate), focus(for_obj),not_svo(for_koof))

    return f'{round(angle)} градусов, отклонение: {round(certain[0]), round(certain[1])}'