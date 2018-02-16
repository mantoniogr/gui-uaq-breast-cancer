#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
UAQ Thermo Breast Cancer

main.py

author: Marco Garduno
mail: mgarduno01@alumnos.uaq.mx
last modified: February 2018
'''

import wx
import cv2
import numpy as np


def thermogram(image, t_max, t_min):
    height, width = image.shape
    t_vgm = np.amax(image)

    t_r = np.zeros((height, width), np.float64)

    for j in range(0, height):
        for i in range(0, width):
            t_r[j, i] = t_min + (image[j, i]/float(t_vgm)) * (t_max - t_min)

    return t_r
