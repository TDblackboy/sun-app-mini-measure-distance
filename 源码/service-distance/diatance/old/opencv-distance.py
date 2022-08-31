# -*- coding: utf-8 -*-
# @Time : 2022/1/6 9:17
# @Author : 曹沫
"""
利用opencv测距
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

path = '../images/2.jpg'
# cap = cv2.VideoCapture(0)
# cap.set(10, 160)
# cap.set(3, 1920)
# cap.set(4, 1080)
scale = 3
wP = 210 * scale
hP = 297 * scale


def getContours(img, cThr=None, minArea=1000, filter=0, draw=False):
    """
    图片的外形轮廓
    :param draw:
    :param filter:
    :param minArea:
    :param cThr:
    :param img:
    :return:
    """
    if cThr is None:
        cThr = [100, 100]
    # 处理成灰度图
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 高斯模糊，高斯滤波
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    # 边缘检测,参数：两个阈值
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])

    kernel = np.ones((5, 5))
    # 膨胀函数
    imgDial = cv2.dilate(imgCanny, kernel, iterations=3)
    # 腐蚀：将前景物体变小
    imgThre = cv2.erode(imgDial, kernel, iterations=2)

    cv2.imshow('Canny', imgThre)

    contours, hierarchy = cv2.findContours(imgThre, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    finalContours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalContours.append([len(approx), area, approx, bbox, i])
            else:
                finalContours.append([len(approx), area, approx, bbox, i])

    finalContours = sorted(finalContours, key=lambda x: x[1], reverse=True)

    if draw:
        for con in finalContours:
            cv2.drawContours(img, con[4], -1, (0, 0, 255), 3)
            # [hull.astype(int)]
    return img, finalContours


def warpImg(img, points, w, h):
    # fig = plt.figure(figsize=(6, 6))
    # plt.scatter(147, 166)
    # plt.scatter(146, 593)
    # plt.scatter(404, 601)
    # plt.scatter(418, 176)
    # plt.show()
    print(points.shape)
    points.reshape((4, 2))


while True:
    # 使用摄像头加载图片
    # if webcam:
    #     success, img = cap.read()
    # else:
    #     # 读彩图
    #     img = cv2.imread(path)
    #     # 读灰度图
    #     # img = cv2.imread(path,2)

    img = cv2.imread(path)
    # 缩放
    img = cv2.resize(img, (0, 0), None, 0.2, 0.2)

    # 图片轮廓 minArea=50000, filter=4
    img, contours = getContours(img, draw=True, minArea=5000, filter=4)
    # print(finalContours)

    # 选取四个点
    if len(contours) != 0:
        biggest = contours[0][2]
        # print(biggest)
        warpImg(img, biggest, 100, 100)

    # cv2.namedWindow("origin", 0)
    # cv2.resizeWindow("origin", 640, 480)
    cv2.imshow('origin', img)
    cv2.waitKey(1)
