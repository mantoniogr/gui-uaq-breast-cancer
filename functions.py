#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
UAQ Thermo Breast Cancer

functions.py

author: Marco Garduno
mail: mgarduno01@alumnos.uaq.mx
last modified: February 2018
'''

import wx
import cv2
import math
import numpy as np

def negative_gray(image):
    height, width =  image.shape
    img = np.copy(image)

    for j in range(0, height):
        for i in  range(0, width):
            img[j, i] = 255 - image[j, i]

    return img

def threshold(image, th1):
    height, width =  image.shape
    img = np.copy(image)

    for j in range(0, height):
        for i in  range(0, width):
            if image[j,i] >= th1:
                img[j,i] = 255;
            else:
                img[j,i] = 0;

    return img

def thermogram(image, t_max, t_min):
    shape = image.shape
    t_vgm = np.amax(image)

    t_r = np.zeros((shape[0], shape[1]), np.float64)

    for j in range(0, shape[0]):
        for i in range(0, shape[1]):
            t_r[j, i] = t_min + (image[j, i]/float(t_vgm)) * (t_max - t_min)

    return t_r

def crop_roi(image_original, image_black):
    shape = image_original.shape

    for j in range(0, shape[0]):
        for i in range(0, shape[1]):
            if image_black[j][i] != 0:
                image_black[j][i] = image_original[j][i]

    return image_black
