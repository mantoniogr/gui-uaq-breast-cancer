#!/usr/bin/env

#
#  morphology.py
#  imgproc_python
#
#  Created by Marco Garduno on 19/02/18.
#  Copyright 2018 Marco Garduno. All rights reserved.
#

import cv2
import numpy as np
import functions as f

def dilation(map, size):
    height, width =  map.shape
    auxMap = np.copy(map)

    for k in range(0, size):
        # B1
        for j in range(0, height):
            for i in range(0, width-1):
                if auxMap[j, i] < auxMap[j, i+1]:
                    auxMap[j, i] = auxMap[j, i+1]

        # B2
        for j in range(0, height-1):
            for i in range(0, width):
                if auxMap[j, i] < auxMap[j+1, i]:
                    auxMap[j, i] = auxMap[j+1, i]

        # B3
        for j in range(0, height):
            for i in range(width-1, 0, -1):
                if auxMap[j, i] < auxMap[j, i-1]:
                    auxMap[j, i] = auxMap[j, i-1]

        # B4
        for j in range(height-1, 0, -1):
            for i in range(0, width):
                if auxMap[j, i] < auxMap[j-1, i]:
                    auxMap[j, i] = auxMap[j-1, i]

    return auxMap

def erosion(map, size):
    height, width =  map.shape
    auxMap = np.copy(map)

    auxMap = f.negative_gray(auxMap)
    auxMap = dilation(auxMap,size)
    auxMap = f.negative_gray(auxMap)

    return auxMap

def opening(map, size):
    auxMap = np.copy(map)

    auxMap = erosion(auxMap, size)
    auxMap = dilation(auxMap, size)

    return auxMap

def closing(map, size):
    auxMap = np.copy(map)

    auxMap = dilation(auxMap, size)
    auxMap = erosion(auxMap, size)

    return auxMap

def geodesic_dilation(I, J):
    height, width =  I.shape
    flag = True

    while(flag):

        img_auxiliar = np.copy(J)

        for j in range(1, height):
            for i in range(1, width-1):
                list1 = (   J[j-1, i-1], J[j-1, i],   J[j-1, i+1],
                            J[j, i-1],   J[j, i])
                J[j, i] = min([max(list1), I[j,i]])

        for j in range(height-2, -1, -1):
            for i in range(width-2, 0, -1):
                list2 = (                   J[j, i],     J[j, i+1],
                            J[j+1, i-1], J[j+1, i],   J[j+1, i+1] )
                J[j, i] = min([max(list2), I[j, i]])

        dif = J - img_auxiliar

        if np.amax(dif) == 0:
            flag = False

    return J

def maxima(img):
    height, width =  img.shape
    img_auxiliar = np.copy(img)

    for j in range(0, height):
        for i in range(0, width):
            if img_auxiliar[j,i] > 0:
                img_auxiliar[j,i] = img_auxiliar[j,i] - 1

    img_auxiliar = geodesic_dilation(img, img_auxiliar)
    img = img - img_auxiliar
    img = f.threshold(img, 1)

    return img

def minima(img):
    img_auxiliar = np.copy(img)

    img_auxiliar = f.negative_gray(img_auxiliar)
    img_auxiliar = maxima(img_auxiliar)
#   img_auxiliar = f.negativoGrises(img_auxiliar)

    return img_auxiliar

def watershed(ime):
    height, width = ime.shape
    fp = np.copy(ime)
    gp = np.copy(ime)
    ims = np.copy(ime) # watershed
    mask = minima(ime) # minimos de ime
    imwl = etiquetado(mask) # vertientes

    # cv2.imshow("etiq", mask)

    imwl[0,:] = 1000000
    imwl[:,0] = 1000000
    imwl[height-1,:] = 1000000
    imwl[:,width-1] = 1000000

    lista = []
    for i in range(0, 256):
        lista.append(i)
    # # fifo jerarquica
    fifoj = {key: [] for key in lista}

    for j in range(1, height-1):
        for i in range(1, width-1):
            if imwl[j,i] != 0:
                ban_ = 255
                for k in range(j-1, j+2):
                    for l in range(i-1, i+2):
                        ban_ = ban_ & imwl[k,l]
                if ban_ == 0:
                    fifoj[ime[j,i]].append([j,i])

    i = 0
    while(i!=256):
        while(bool(fifoj[i]) is True):
            coord = fifoj[i].pop(0)

            for k in range(coord[0]-1, coord[0]+2):
                for l in range(coord[1]-1, coord[1]+2):
                    if imwl[k,l] == 0:
                        for n in range(k-1, k+2):
                            for m in range(l-1, l+2):
                                if imwl[n,m] != imwl[coord[0],coord[1]] and imwl[n,m] != 0 and imwl[n,m] != 1000000:
                                    ims[k,l] = 255
                                imwl[k,l] = imwl[coord[0],coord[1]]
                                fifoj[ime[k,l]].append([k,l])
        i = i + 1

    return ims, imwl

def etiquetado(img):
    imgAuxiliar = np.copy(img)
    img2 = np.copy(img)

    height, width =  img.shape

    k = 0
    l = 10
    fifo = []

    lista = []
    for i in range(0, 3000):
        lista.append(i)
    # # fifo jerarquica
    fifoj = {key: 0 for key in lista}

    imgAuxiliar[0,:] = 0
    imgAuxiliar[:,0] = 0
    imgAuxiliar[height-1,:] = 0
    imgAuxiliar[:,width-1] = 0

    for j in range(0, height):
        for i in range(0, width):
            if imgAuxiliar[j,i] != 0:
                k = k + 1
                l = l + 1
                fifo.append([j,i])
                imgAuxiliar[j,i] = 0
                img2[j,i] = k
                fifoj[k] += 1
                while(fifo):
                    primas = fifo.pop(0)
                    for n in range(primas[0] - 1, primas[0] + 2):
                        for m in range(primas[1] - 1, primas[1] + 2):
                            if imgAuxiliar[n,m] != 0:
                                fifo.append([n,m])
                                imgAuxiliar[n,m] = 0
                                img2[n,m] = k
                                fifoj[k] += 1

    return img2
