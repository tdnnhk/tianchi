# -*- coding: utf-8 -*-


import os
import pandas as pd
import numpy as np
import cv2
import math
from PIL import Image, ImageDraw


def draw_boxes(path, name, rectangle=False):
    file_pic = '\\image_1000\\%s.jpg' % name  # 图片的地址
    file_text = '\\txt_1000\\%s.txt' % name  # 描述文件的地址
    if not os.path.exists(path + file_pic):
        print('无法找到图片')
        return
    if not os.path.exists(path + file_text):
        print('无法找到描述文件')
        return

    img = Image.open(path + file_pic)

    draw = ImageDraw.Draw(img)
    text_point = pd.read_csv(path + file_text, header=None)
    arr_img = np.array(img)
    #print(arr_img[100], "aaa")
    for idx, row in text_point.iterrows():
        point = row.loc[range(8)].tolist()  # 依次读取八个点的数据
        x = [point[i] for i in [0, 2, 4, 6]]
        y = [point[i] for i in [1, 3, 5, 7]]
        point = [(a, b) for a, b in zip(x, y)]
        draw.polygon(point, outline=(0, 128, 255))  # 画多边形

    print(point)
    print(point[1][1])

    # 求出点1，点2连线的方程g1
    a1 = np.array([[point[0][0], 1], [point[1][0], 1]])
    b1 = np.array([point[0][1], point[1][1]])
    g1 = np.linalg.solve(a1, b1)
    print(g1[0])

    # 求出与g1线垂直的线,并选择外围的方程g4
    if (g1[0] != 0.0):
        a2 = - (1 / g1[0])
        b21 = point[0][1] - a2 * point[0][0]
        b22 = point[3][1] - a2 * point[3][0]
        if (b22 > b21):
            g4 = [a2, b22]
        else:
            g4 = [a2, b21]
    else:
        if (point[3][1] > point[0][1]):
            g4 = [0, point[3][1]]
        else:
            g4 = [0, point[0][1]]

    print(g4)

    # 求出与g1线垂直的并选择外围的方程g2
    b31 = point[1][1] - g4[0] * point[1][0]
    b32 = point[2][1] - g4[0] * point[2][0]
    if (b31 > b32):
        g2 = [g4[0], b31]
    else:
        g2 = [g4[0], b32]
    print(g2)

    # 求出与g2\g4线垂直的并选择外围的方程g3
    b41 = point[2][1] - g4[0] * point[1][0]
    b42 = point[3][1] - g4[0] * point[2][0]
    if (b41 > b42):
        g3 = [g1[0], b41]
    else:
        g3 = [g1[0], b42]
    print(g3)


    # 添加行序列

    tem_row = []
    new_img = []
    #print(arr_img[212][212], "1111")
    # for x in range(212, 256):
    #     y = math.floor(g4[0] * x + g4[1])
    #     tem_row.append(arr_img[y][x])
    # new_img = tem_row

    for h in range(10,787):
        tem_row1 = []
        for x in range(10, 263):
            #y = math.floor(g4[0] * x + g4[1])
            tem_row1.append(arr_img[h][x])
        new_img.append(tem_row1)

    new_img1=np.array(new_img)
    img11 = Image.fromarray(new_img1)
    img11.show()
    print(new_img1.shape)

    return img


if __name__ == '__main__':
    path = 'D:\\learn\\projects\\Tianchi\\dataset\\train_1000'  # 文件夹地址
    name = 'TB1.PhFLXXXXXaDXFXXunYpLFXX'
    img = draw_boxes(path, name, True)
    img.resize((400, 400)).save(path + '\\demo.jpg')  # 保存图片
    # img.show()
    realpath = path + '\\image_1000\\%s.jpg' % name;
    cvtest = cv2.imread(realpath)
    print(cvtest.shape)
    # cv2.line(cvtest, (300, 0), (100, 399), (0, 0, 233))
    # cvtest.show()
    box = np.array([[(185, 726), (190, 760), (411, 699), (402, 670)]])
    # boxaf = np.array([[(0, 0), (35, 0), (35, 65), (0, 65)]])
    # box = np.array([[(185.1, 726.0), (190.5, 760.2), (411.3, 699.0), (402.3, 670.0)]])
    cv2.fillPoly(cvtest, box, (0, 255, 0), shift=0)
    #cv2.imshow('lena.jpg', cvtest)
    cv2.waitKey(0)

