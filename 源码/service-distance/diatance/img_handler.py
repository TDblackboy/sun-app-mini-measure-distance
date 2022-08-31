# -*- coding: utf-8 -*-
# @Time : 2022/1/6 13:17
# @Author : 曹沫
"""
输入-传参：图片的保存路径
处理：
    加载图片
    图片特征处理
    轮廓选择？
    距离计算？
输出：处理后的图片？路径？

API
1.cv2.cvtColor(图像颜色转换)
2.cv2.findContours(找出图像的轮廓)
3.cv2.drawContours(画出图像轮廓)
4.cv2.contourArea(轮廓面积)
5.cv2.arcLength(轮廓周长)
6.cv2.aprroxPloyDP(获得轮廓近似)
7.cv2.boudingrect(外接圆)
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

import config


def show(title, img):
    cv2.imshow(title, img)
    cv2.waitKey(0)


def showAll(*imgs):
    i = 1
    for img in imgs:
        cv2.imshow(str(i), img)
        i += 1
    cv2.waitKey(0)


def imgPreHandler(img, cThr=None):
    """
    图片预处理
    :param cThr:
    :param img:
    :return:
    """
    if cThr is None:
        cThr = [100, 100]

    # ------------------图像特征处理----------------------
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
    # --------------------------------------------------
    # showAll(imgGray, imgBlur, imgCanny, imgDial, imgThre)
    return imgThre


def getContours(origin, imgProcessed, minArea=1000, shape=0, draw=False):
    """
    图片的外形轮廓,计算
    :param shape:
    :param imgProcessed:
    :param origin:
    :param draw:
    :param minArea:
    :return:
    """
    # --------------边缘---------------------------------
    # （1）搜索轮廓：尽可能检测所有的轮廓
    # cv2.findContours处理的图像为二值图（黑白图）=》原图-灰度图-二值图
    # cv2.RETR_EXTERNAL表示只检测外轮廓：轮廓的检索模式
    # 轮廓的近似办法：cv2.CHAIN_APPROX_SIMPLE压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标
    # contours:一个列表，每一项都是一个轮廓， 不会存储轮廓所有的点，只存储能描述轮廓的点
    # hierarchy:一个ndarray, 元素数量和轮廓数量一样
    contours, hierarchy = cv2.findContours(imgProcessed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # <class 'tuple'>
    # print(type(contours))
    # print(contours)
    # <class 'numpy.ndarray'>
    # print(type(hierarchy))
    # print(hierarchy)

    # （2）挑选轮廓
    finalContours = []
    for i in contours:
        # 根据轮廓的面积筛选：计算轮廓的面积
        area = cv2.contourArea(i)
        # print('ares:', area)
        if area > minArea:
            # 计算轮廓的周长
            peri = cv2.arcLength(i, True)
            # print('peri', peri)
            # 轮廓的近似:返回的是一些列点组成的多边形
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            # print('approx', approx)
            # 矩形边框:(x，y，w，h)x，y是矩阵左上点的坐标，w，h是矩阵的宽和高--“绿边的”
            # bbox = cv2.boundingRect(approx)
            x, y, w, h = cv2.boundingRect(approx)
            # 画出“绿色的边缘线”
            cv2.rectangle(origin, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # shape? 四个点，代表四条边即四边形
            if shape > 0:
                # print(len(approx))
                if len(approx) == shape:
                    # 保存一个轮廓的相关信息
                    # finalContours.append([len(approx), area, approx, bbox, i])
                    finalContours.append([len(approx), area, approx, (x, y, w, h), i])
            else:
                finalContours.append([len(approx), area, approx, (x, y, w, h), i])

    finalContours = sorted(finalContours, key=lambda x: x[1], reverse=True)

    # ---画出原图的边缘-----------------
    # 问题：画的线不够好-没有直直的把轮廓圈起来，只是把轮廓点显示出来了！
    # 画出“红色的点/线”
    if draw:
        for con in finalContours:
            cv2.drawContours(origin, con[4], -1, (0, 0, 255), 3)
    # show("ori",origin)
    return origin, finalContours


def reorder(points):
    """
    “4个边界点”重排序
        shape：（4，1，2），矩形4个点，每个（x，y）
    :param points:
    :return:
    """
    # print(points)
    new = np.zeros_like(points)
    # print(new)
    points = points.reshape((4, 2))

    add = points.sum(1)
    # print(add)
    new[0] = points[np.argmin(add)]
    new[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    new[1] = points[np.argmin(diff)]
    new[2] = points[np.argmax(diff)]
    # print(new)
    return new


def warpImg(img, points, w, h, pad=20):
    points = reorder(points)
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    # 透视变换
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgWrap = cv2.warpPerspective(img, matrix, (w, h))
    imgWrap = imgWrap[pad:imgWrap.shape[0] - pad, pad:imgWrap.shape[1] - pad]
    # 效果是将原图中的轮廓扣出来了
    return imgWrap


def plt1():
    """
    绘制散点图
    :return:
    """
    plt.scatter(182, 328)
    plt.scatter(298, 249)
    plt.scatter(303, 508)
    plt.scatter(427, 417)
    plt.show()


def findDis(pts1, pts2):
    """
    计算边长:勾股定理
    :param pts1:
    :param pts2:
    :return:
    """
    return ((pts2[0] - pts1[0]) ** 2 + (pts2[1] - pts1[1]) ** 2) ** 0.5


# 问题：计算边长，图片中距离的长度与实际物体长度的比例？怎么确定！！！
class Distance:
    def __init__(self):
        # 这个参数很重要
        # self.scale = 5 #近距离 10cm左右
        self.scale = 1.5  # 远距离 40cm左右
        self.wP = 210 * self.scale
        self.hP = 297 * self.scale

    def compute(self, fullPath):
        # 1读彩图
        # img数据格式为<class 'numpy.ndarray'>
        # print(type(img))
        img1 = cv2.imread(fullPath)
        # 2缩放
        img1 = cv2.resize(img1, (0, 0), None, 0.2, 0.2)

        # 3预处理
        img2 = imgPreHandler(img1)

        # 4图片中所有轮廓
        # minArea、shape参数调整
        # img1, contours = getContours(img1, img2, draw=True, minArea=5000, shape=4)
        img1, contours = getContours(img1, img2, minArea=5000, shape=4, draw=True)

        # 是否有选中的轮廓数据
        if len(contours) != 0:
            # ---------------------------------------------------------
            # (***)将外层最大的轮廓抠出来
            # "轮廓"矩阵（红边的）的四个点
            # biggest = contours[0][2]
            # imgWarp = warpImg(img1, biggest, self.wP, self.hP)
            # # 取出其中小的轮廓
            # imgWarp2 = imgPreHandler(imgWarp, cThr=[50, 50])
            # imgContours2, conts2 = getContours(imgWarp, imgWarp2, minArea=2000, shape=4)

            # ----------------------------------------------------------
            # 遍历识别出的每一个轮廓
            for one in contours:
                # "轮廓"矩阵（红边的）的四个点
                points = one[2]
                # 边长用颜色勾勒
                cv2.polylines(img1, [points], True, (255, 0, 0), 3)
                # 计算边长
                nPoints = reorder(points)
                # 大约值
                dw = round(findDis(nPoints[0][0] // self.scale, nPoints[1][0] // self.scale) / 10, 1)
                dh = round(findDis(nPoints[0][0] // self.scale, nPoints[2][0] // self.scale) / 10, 1)
                # print(dw)
                # print(dh)
                # 显示边长：画出“粉色的边长+箭头”
                # arrowedLine参数：图片、起点、终点、颜色、线宽、线的类型、箭头平移系数、箭头大小缩放系数
                cv2.arrowedLine(img1, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[1][0][0], nPoints[1][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                cv2.arrowedLine(img1, (nPoints[0][0][0], nPoints[0][0][1]), (nPoints[2][0][0], nPoints[2][0][1]),
                                (255, 0, 255), 3, 8, 0, 0.05)
                x, y, w, h = one[3]
                # putText参数：图片，添加的文字，左上角坐标，字体，字体大小，颜色，字体粗细
                cv2.putText(img1, '{}cm'.format(dw), (x + 30, y - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (255, 0, 255),
                            2)
                cv2.putText(img1, '{}cm'.format(dh), (x - 70, y + h // 2), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2,
                            (255, 0, 255),
                            2)

        # 显示处理后的图片
        # showAll(img1)
        savePath = config.get_rootPath() + config.get_prefix() + fullPath.replace(config.get_rootPath(), '')
        cv2.imwrite(savePath, img1)
        return savePath


if __name__ == '__main__':
    fullPath = './images/3.jpg'
    distance = Distance()
    distance.compute(fullPath)
    # print(fullPath.replace(config.get_rootPath(), ''))
