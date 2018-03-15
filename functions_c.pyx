#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
UAQ Thermo Breast Cancer

functions.pyx

author: Marco Garduno
email: mgarduno01@alumnos.uaq.mx
last modified: 14 March 2018
'''

import cv2
import math
import numpy as np
import cython

import morphology_c as mc

# Example
@cython.boundscheck(False)
cpdef unsigned char[:,:] threshold_fast(int T, unsigned char [:,:] image):
    # set the variable extension types
    cdef int x, y, w, h
    # grab the image dimensions
    h = image.shape[0]
    w = image.shape[1]

    # loop over the image
    for y in range(0, h):
        for x in range(0, w):
            # threshold the pixel
            image[y, x] = 255 if image[y, x] >= T else 0

    # return the thresholded image
    return image

@cython.boundscheck(False)
cpdef unsigned char[:,:] difference(unsigned char [:,:] image1, unsigned char [:,:] image2):
    # set the variable extension types
    cdef int x, y, w, h
    # grab the image dimensions
    h = image1.shape[0]
    w = image1.shape[1]

    # img = np.zeros((h, w), np.float64)
    img = np.copy(image1)

    # loop over the image
    for y in range(0, h):
        for x in range(0, w):
            # threshold the pixel
            img[y, x] = image1[y, x] - image2[y, x]

    # return the thresholded image
    return img

@cython.boundscheck(False)
cpdef double[:,:] thermogram(unsigned char [:, :] image, int t_max, int t_min):
    cdef int i, j, w, h
    h = image.shape[0]
    w = image.shape[1]

    t_r = np.zeros((h, w), np.float64)
    t_vgm = np.amax(image)

    for j in range(0, h):
        for i in range(0, w):
            t_r[j, i] = t_min + (image[j, i]/float(t_vgm)) * (t_max - t_min)

    return t_r

@cython.boundscheck(False)
cpdef unsigned char[:,:] crop_roi(unsigned char [:,:] image, unsigned char [:,:] image_black):
# def crop_roi(image, image_black):
    cdef int i, j, w, h

    h = image.shape[0]
    w = image.shape[1]

    for j in range(0, h):
        for i in range(0, w):
            image_black[j, i] = image[j, i] if image_black[j, i] != 0 else image_black[j, i]

    return image_black

@cython.boundscheck(False)
cpdef unsigned char[:,:] negative_gray(unsigned char [:,:] image):
# def negative_gray(image):
    cdef int i, j, w, h

    h = image.shape[0]
    w = image.shape[1]

    img = np.copy(image)

    for j in range(0, h):
        for i in  range(0, w):
            img[j, i] = 255 - image[j, i]

    return img

@cython.boundscheck(False)
cpdef unsigned char[:,:] threshold(unsigned char [:,:] image, int th1):
# def threshold(image, th1):
    cdef int i, j, w, h

    h = image.shape[0]
    w = image.shape[1]

    img = np.copy(image)

    for j in range(0, h):
        for i in  range(0, w):
            if image[j, i] >= th1:
                img[j, i] = 255;
            else:
                img[j, i] = 0;

    return img

@cython.boundscheck(False)
cpdef unsigned char[:,:] threshold_2(unsigned char [:,:] image, int T):
# def threshold_2(image, int T):
    cdef int i, j, w, h

    h = image.shape[0]
    w = image.shape[1]

    img = np.copy(image)

    for j in range(0, h):
        for i in  range(0, w):
            if image[j, i] >= T:
                img[j, i] = 0

    return img

@cython.boundscheck(False)
cpdef unsigned char[:,:] chest_removal(unsigned char [:,:] image_original):
# def chest_removal(image_original):
    cdef int i, j, w, h

    h = image_original.shape[0]
    w = image_original.shape[1]

    img = np.copy(image_original)

    for j in range(0, h-1):
        for i in range(0, w-1):
            if img[j, i] == 255 and img[j+1, i] != 255 :
                img[j+1, i] = 255

    list_p = []

    for i in range(0, w-1):
        if img[h-1, i] == 0 and img[h-1, i+1] == 255:
            list_p.append(i)
        if img[h-1, i] == 255 and img[h-1, i+1] == 0:
            list_p.append(i)

    for j in range(0, h):
        for i in range(0, w-1):
            if img[j, i] == 255 and i >= list_p[3]:
                img[j, i+1] = 255
        for i in range(w-1, 0, -1):
            if img[j, i] == 255 and i-1 <= list_p[0]:
                img[j, i-1] = 255

    return img

@cython.boundscheck(False)
cpdef double[:] analysis_two( unsigned char [:, :] image_original, double [:, :] thermogram):
# def analysis(image_original, thermogram):
    cdef int i, j, w, h
    cdef double avg_temp[2]

    h = image_original.shape[0]
    w = image_original.shape[1]

    th, image_umbral = cv2.threshold(np.asarray(image_original), 1, 255, cv2.THRESH_BINARY)
    image_umbral = np.asarray(image_umbral)
    image_labeled = mc.etiquetado(image_umbral)

    th, image_r = cv2.threshold(np.asarray(image_labeled), 1, 1, cv2.THRESH_BINARY)
    th, image_l = cv2.threshold(np.asarray(image_labeled), 2, 2, cv2.THRESH_BINARY)
    cv2.imwrite("1.png", image_r)
    cv2.imwrite("2.png", image_l)

    return avg_temp

@cython.boundscheck(False)
cpdef double[:] analysis_one( unsigned char [:, :] image_original, double [:, :] thermogram):
# def analysis(image_original, thermogram):
    cdef int i, j, w, h
    cdef double avg_temp[2]

    h = image_original.shape[0]
    w = image_original.shape[1]

    th, image_umbral = cv2.threshold(np.asarray(image_original), 1, 255, cv2.THRESH_BINARY)
    image_umbral = np.asarray(image_umbral)
    image_labeled = mc.etiquetado(image_umbral)

    list_r = []
    list_l = []

    for j in range(0, h):
        for i in range(0, w):
            if image_labeled[j, i] == 1:
                list_r.append(thermogram[j][i])
            if image_labeled[j, i] == 2:
                list_l.append(thermogram[j][i])

    t_right = sum(list_r)/len(list_r)
    t_left = sum(list_l)/len(list_l)

    avg_temp[0] = t_right
    avg_temp[1] = t_left

    return avg_temp
