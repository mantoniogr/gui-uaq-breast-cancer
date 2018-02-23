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
import cython

def thermogram(image, int t_max, int t_min):
    cdef int i, j, w, h

    h = image.shape[0]
    w = image.shape[1]

    t_r = np.zeros((h, w), np.float64)
    t_vgm = np.amax(image)

    for j in range(0, h):
        for i in range(0, w):
            t_r[j, i] = t_min + (image[j, i]/float(t_vgm)) * (t_max - t_min)

    return t_r

def crop_roi(image, image_black):
    cdef int i, j, w, h

    h = image.shape[0]
    w = image.shape[1]

    for j in range(0, h):
        for i in range(0, w):
            image_black[j, i] = image[j][i] if image_black[j, i] != 0 else image_black[j, i]

    return image_black

def negative_gray(image):
    cdef int i, j, w, h

    h = image.shape[0]
    w = image.shape[1]

    img = np.copy(image)

    for j in range(0, h):
        for i in  range(0, w):
            img[j, i] = 255 - image[j, i]

    return img

def threshold_2(image, int T):
    cdef int i, j, w, h

    h = image.shape[0]
    w = image.shape[1]

    img = np.copy(image)

    for j in range(0, h):
        for i in  range(0, w):
            img[j, i] = 0 if image[j, i] >= T else image[j, i]

    return image

def chest_removal(image_original):
    cdef int i, j, w, h

    h = image_original.shape[0]
    w = image_original.shape[1]

    img = np.copy(image_original)

    for j in xrange(0, h-1):
        for i in xrange(0, w-1):
            if img[j][i] == 255 and img[j+1][i] != 255 :
                img[j+1][i] = 255

    list_p = []

    for i in xrange(0, w-1):
        if img[h-1][i] == 0 and img[h-1][i+1] == 255:
            list_p.append(i)
        if img[h-1][i] == 255 and img[h-1][i+1] == 0:
            list_p.append(i)

    for j in xrange(0, h):
        for i in xrange(0, w-1):
            if img[j][i] == 255 and i >= list_p[3]:
                img[j][i+1] = 255
        for i in xrange(w-1, 0, -1):
            if img[j][i] == 255 and i-1 <= list_p[0]:
                img[j][i-1] = 255

    return img
