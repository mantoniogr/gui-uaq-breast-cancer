#!/usr/bin/env

#
#  morphology_c.pyx
#  imgproc_python
#
#  Created by Marco Garduno on 23/02/18.
#  Copyright 2018 Marco Garduno. All rights reserved.
#

import cv2
import numpy as np
import functions as fc
import cython

def dilation(map, int size):
    cdef int i, j, w, h

    h = map.shape[0]
    w = map.shape[1]

    auxMap = np.copy(map)

    for k in range(0, size):
        # B1
        for j in range(0, h):
            for i in range(0, w-1):
                if auxMap[j, i] < auxMap[j, i+1]:
                    auxMap[j, i] = auxMap[j, i+1]

        # B2
        for j in range(0, h-1):
            for i in range(0, w):
                if auxMap[j, i] < auxMap[j+1, i]:
                    auxMap[j, i] = auxMap[j+1, i]

        # B3
        for j in range(0, h):
            for i in range(w-1, 0, -1):
                if auxMap[j, i] < auxMap[j, i-1]:
                    auxMap[j, i] = auxMap[j, i-1]

        # B4
        for j in range(h-1, 0, -1):
            for i in range(0, w):
                if auxMap[j, i] < auxMap[j-1, i]:
                    auxMap[j, i] = auxMap[j-1, i]

    return auxMap

def erosion(map, int size):
    cdef int i, j, w, h

    h = map.shape[0]
    w = map.shape[1]

    auxMap = np.copy(map)

    auxMap = fc.negative_gray(auxMap)
    auxMap = dilation(auxMap,size)
    auxMap = fc.negative_gray(auxMap)

    return auxMap

def opening(map, int size):
    auxMap = np.copy(map)

    auxMap = erosion(auxMap, size)
    auxMap = dilation(auxMap, size)

    return auxMap

def closing(map, int size):
    auxMap = np.copy(map)

    auxMap = dilation(auxMap, size)
    auxMap = erosion(auxMap, size)

    return auxMap
