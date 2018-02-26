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

def threshold_2(image, th1):
    height, width =  image.shape
    img = np.copy(image)

    for j in range(0, height):
        for i in  range(0, width):
            if image[j,i] >= th1:
                img[j,i] = 0

    return img

def chest_removal(image_original):
    shape = image_original.shape
    img = np.copy(image_original)

    for j in xrange(0, shape[0]-1):
        for i in xrange(0, shape[1]-1):
            if img[j][i] == 255 and img[j+1][i] != 255 :
                img[j+1][i] = 255

    list_p = []

    for i in xrange(0, shape[1]-1):
        if img[shape[0]-1][i] == 0 and img[shape[0]-1][i+1] == 255:
            list_p.append(i)
        if img[shape[0]-1][i] == 255 and img[shape[0]-1][i+1] == 0:
            list_p.append(i)

    for j in xrange(0, shape[0]):
        for i in xrange(0, shape[1]-1):
            if img[j][i] == 255 and i >= list_p[3]:
                img[j][i+1] = 255
        for i in xrange(shape[1]-1, 0, -1):
            if img[j][i] == 255 and i-1 <= list_p[0]:
                img[j][i-1] = 255

    return img

def analysis(image_original, thermogram):
    shape = image_original.shape
    th, image_umbral = cv2.threshold(image_original, 1, 255, cv2.THRESH_BINARY)

    x_max = 0
    x_min = 10000000

    for j in xrange(0, shape[0]):
        for i in xrange(0, shape[1]):
            if image_umbral[j][i] == 255:
                if i > x_max:
                    x_max = i
                if i < x_min:
                    x_min = i

    # for i in xrange(0, int(shape[1]/2)):
    #     for j in xrange(0, shape[0]):
    #         if image_umbral[j][i] == 255:
    #             x_min = i
    #             break
    #
    # for i in xrange(int(shape[1]/2), shape[1], -1):
    #     for j in xrange(0, shape[0]):
    #         if image_umbral[j][i] == 255:
    #             x_max = i
    #             break

    mid_x = int((x_max+x_min)/2)
    max_value = np.amax(image_original)

    list_t = []
    list_p_r = []

    for k in xrange(0, max_value):
        for j in xrange(0, shape[0]):
            for i in xrange(0, mid_x):
                if image_original[j][i] == k:
                    list_t.append(thermogram[j][i])
        list_p_r.append(sum(list_t)/len(list_t))

    t_right = sum(list_p_r)/len(list_p_r)

    list_t = []
    list_p_l = []

    for k in xrange(0, max_value):
        for j in xrange(0, shape[0]):
            for i in xrange(mid_x, shape[1]):
                if image_original[j][i] == k:
                    list_t.append(thermogram[j][i])
        list_p_l.append(sum(list_t)/len(list_t))

    t_left = sum(list_p_l)/len(list_p_l)

    return t_right, t_left
