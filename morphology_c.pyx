#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
UAQ Thermo Breast Cancer

functions.pyx

author: Marco Garduno
mail: mgarduno01@alumnos.uaq.mx
last modified: 14 March 2018
'''

import cv2
import numpy as np
import functions_c as fc
import cython

@cython.boundscheck(False)
cpdef unsigned char[:,:] dilation(unsigned char [:,:] map, int size):
# def dilation(map, int size):
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

@cython.boundscheck(False)
cpdef unsigned char[:,:] erosion(unsigned char [:,:] map, int size):
# def erosion(map, int size):
    auxMap = np.copy(map)

    auxMap = fc.negative_gray(auxMap)
    auxMap = dilation(auxMap,size)
    auxMap = fc.negative_gray(auxMap)

    return auxMap

@cython.boundscheck(False)
cpdef unsigned char[:,:] opening(unsigned char [:,:] map, int size):
# def opening(map, int size):
    auxMap = np.copy(map)

    auxMap = erosion(auxMap, size)
    auxMap = dilation(auxMap, size)

    return auxMap

@cython.boundscheck(False)
cpdef unsigned char[:,:] closing(unsigned char [:,:] map, int size):
# def closing(map, int size):
    auxMap = np.copy(map)

    auxMap = dilation(auxMap, size)
    auxMap = erosion(auxMap, size)

    return auxMap

@cython.boundscheck(False)
cpdef unsigned char[:,:] geodesic_dilation(unsigned char [:,:] I, unsigned char [:,:] J):
# def geodesic_dilation(I, J):
    cdef int i, j, w, h

    h = I.shape[0]
    w = I.shape[1]

    flag = True

    while(flag):

        img_auxiliar = np.copy(J)

        for j in range(1, h):
            for i in range(1, w-1):
                list1 = (   J[j-1, i-1], J[j-1, i],   J[j-1, i+1],
                            J[j, i-1],   J[j, i])
                J[j, i] = min([max(list1), I[j,i]])

        for j in range(h-2, -1, -1):
            for i in range(w-2, 0, -1):
                list2 = (                   J[j, i],     J[j, i+1],
                            J[j+1, i-1], J[j+1, i],   J[j+1, i+1] )
                J[j, i] = min([max(list2), I[j, i]])

        dif = J - img_auxiliar

        if np.amax(dif) == 0:
            flag = False

    return J

@cython.boundscheck(False)
cpdef unsigned char[:,:] geodesic_erosion(unsigned char [:,:] I, unsigned char [:,:] J):
# def geodesic_erosion(I, J):

    I = fc.negative_gray(I)
    J = fc.negative_gray(J)

    J = geodesic_dilation(I,J)

    I = fc.negative_gray(I)
    J = fc.negative_gray(J)

    return J

@cython.boundscheck(False)
cpdef unsigned char[:,:] closing_by_reconstruction(unsigned char [:,:] map, int n):
# def closing_by_reconstruction(map, n):
    img_auxiliar = np.copy(map)
    Y = np.copy(map)

    Y = dilation(map, n)
    dilatada = np.copy(Y)
    J = geodesic_erosion(img_auxiliar, Y)

    return J

@cython.boundscheck(False)
cpdef unsigned char[:,:] maxima(unsigned char [:,:] img):
# def maxima(img):
    cdef int i, j, w, h

    h = img.shape[0]
    w = img.shape[1]

    img_auxiliar = np.copy(img)

    for j in range(0, h):
        for i in range(0, w):
            if img_auxiliar[j, i] > 0:
                img_auxiliar[j, i] = img_auxiliar[j, i] - 1

    img_auxiliar = geodesic_dilation(img, img_auxiliar)
    # img = img - img_auxiliar
    img = fc.difference(img, img_auxiliar)
    img = fc.threshold(img, 1)

    return img

@cython.boundscheck(False)
cpdef unsigned char[:,:] minima(unsigned char [:,:] img):
# def minima(img):
    img_auxiliar = np.copy(img)

    img_auxiliar = fc.negative_gray(img_auxiliar)
    img_auxiliar = maxima(img_auxiliar)

    return img_auxiliar

@cython.boundscheck(False)
cpdef unsigned char[:,:] watershed(unsigned char [:,:] ime):
# def watershed(ime):
    cdef int i, j, w, h, k, l, m, n

    ime = fc.negative_gray(ime)
    ime = cv2.GaussianBlur(np.asarray(ime), (3,3), 0)

    h = ime.shape[0]
    w = ime.shape[1]

    fp = np.copy(ime)
    gp = np.copy(ime)
    ims = np.copy(ime) # watershed
    mask = minima(ime) # minimos de ime
    imwl = etiquetado(mask) # vertientes

    imwl[0,:] = 255
    imwl[:,0] = 255
    imwl[h-1,:] = 255
    imwl[:,w-1] = 255

    lista = []
    for i in range(0, 256):
        lista.append(i)
    # # fifo jerarquica
    fifoj = {key: [] for key in lista}

    for j in range(1, h-1):
        for i in range(1, w-1):
            if imwl[j,i] != 0:
                ban_ = 255
                for k in range(j-1, j+2):
                    for l in range(i-1, i+2):
                        ban_ = ban_ & imwl[k,l]
                if ban_ == 0:
                    fifoj[ime[j, i]].append([j, i])

    i = 0
    while(i!=256):
        while(bool(fifoj[i]) is True):
            coord = fifoj[i].pop(0)

            for k in range(coord[0]-1, coord[0]+2):
                for l in range(coord[1]-1, coord[1]+2):
                    if imwl[k, l] == 0:
                        for n in range(k-1, k+2):
                            for m in range(l-1, l+2):
                                if imwl[n, m] != imwl[coord[0], coord[1]] and imwl[n, m] != 0 and imwl[n, m] != 255:
                                    ims[k, l] = 255
                                imwl[k, l] = imwl[coord[0],coord[1]]
                                fifoj[ime[k, l]].append([k, l])
        i = i + 1

    ims = fc.negative_gray(ims)

    # return ims, imwl
    return imwl

@cython.boundscheck(False)
cpdef unsigned char[:,:] etiquetado(unsigned char [:,:] img):
# def etiquetado(img):
    cdef int i, j, w, h, k, l, m, n

    imgAuxiliar = np.copy(img)
    img2 = np.copy(img)

    h = img.shape[0]
    w = img.shape[1]

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
    imgAuxiliar[h-1,:] = 0
    imgAuxiliar[:,w-1] = 0

    for j in range(0, h):
        for i in range(0, w):
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
