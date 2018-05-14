#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
UAQ Thermo Breast Cancer

main.py

author: Marco Garduno
email: mgarduno01@alumnos.uaq.mx
last modified: 14 March 2018
'''

import wx
import cv2
import numpy as np
import math
import time

import cv2
import numpy as np
import math
import time

from fpdf import FPDF

import functions as f
import functions_c as fc
import morphology as m
import morphology_c as mc

import thermogramDialog as td

ID_EXIT = 1
ID_ABOUT = 2
ID_TERMO = 3
ID_ROI = 4
ID_THRES = 5
ID_SEG = 6
ID_ANAL1 = 7
ID_RES = 8
ID_ANAL2 = 9

cropping = False
refPt = []
sel_rect_endpoint = []

class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        # Variables
        self.image = None
        self.image_original = None
        self.image_black = None
        self.path = None
        self.t_r = None
        self.name = "Ana Maria Trejo Chavez"

        # Configuration File .txt
        self.file = open("config.txt","r")
        data = self.file.readlines()
        self.file.close()
        self.t_min = float(data[1])
        self.t_max = float(data[3])

        self.t_left = None
        self.t_right = None

        # GUI design
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        editMenu = wx.Menu()
        diagMenu = wx.Menu()
        resMenu = wx.Menu()
        helpMenu = wx.Menu()

        fileMenu.Append(wx.ID_NEW, '&New')
        fileMenu.Append(wx.ID_OPEN, '&Open')
        fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        qmi = wx.MenuItem(fileMenu, ID_EXIT, '&Quit\tCtrl+Q')
        fileMenu.Append(qmi)

        editMenu.Append(ID_TERMO, '&1 Thermogram')
        editMenu.Append(ID_ROI, '&2 ROI')
        editMenu.Append(ID_THRES, '&3 Threshold')

        # diagMenu.Append(ID_SEG, '&4 Segmentation')
        diagMenu.Append(ID_ANAL1, '&4 Analysis One')
        diagMenu.Append(ID_ANAL2, '&5 Analysis Two')

        resMenu.Append(ID_RES, '&6 Results')

        helpMenu.Append(ID_ABOUT, '&About')

        self.Bind(wx.EVT_MENU, self.OnQuit, id=ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnNew, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)

        self.Bind(wx.EVT_MENU, self.AboutMessage, id=ID_ABOUT)

        self.Bind(wx.EVT_MENU, self.OnThermogram, id=ID_TERMO)
        self.Bind(wx.EVT_MENU, self.OnRoi, id=ID_ROI)
        self.Bind(wx.EVT_MENU, self.OnThreshold, id=ID_THRES)

        # self.Bind(wx.EVT_MENU, self.OnSegmentation, id=ID_SEG)
        self.Bind(wx.EVT_MENU, self.OnAnalysisOne, id=ID_ANAL1)
        self.Bind(wx.EVT_MENU, self.OnAnalysisTwo, id=ID_ANAL2)

        self.Bind(wx.EVT_MENU, self.OnResults, id=ID_RES)

        menubar.Append(fileMenu, '&File')
        menubar.Append(editMenu, '&Edit')
        menubar.Append(diagMenu, '&Analisis')
        menubar.Append(resMenu, '&Results')
        menubar.Append(helpMenu, '&Help')

        self.SetMenuBar(menubar)

        # Window parameters
        self.SetSize((500, 80))
        self.SetTitle('UAQ Thermo Breast Cancer')
        # self.Centre()
        self.Show(True)

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('UAQ Breast Cancer')

        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())

    def OnQuit(self, e):
        self.Close()

    def OnNew(self, e):
        cv2.destroyAllWindows()
        self.statusbar.SetStatusText("Seleccionar Termograma")
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "All files (*.png;*.jpp;)|*.png;*.jpg|PNG files (*.png)|*.png|JPEG files (*.jpg;*.jpeg)|*.jpg;*.jpeg",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        self.path = openFileDialog.GetPath()

        if self.path:
            self.image = cv2.imread(self.path, 0)
            self.image = cv2.resize(self.image, (0,0), fx=0.5, fy=0.5)
            cv2.imshow("Image", self.image)

            shape = self.image.shape
            self.image_original = np.copy(self.image)
            self.image_black = np.zeros((shape[0], shape[1]), np.uint8)

            path_text = self.path[0:len(self.path)-4] + ".txt"
            # print path_text

            try:
                self.t_r = np.loadtxt(path_text, delimiter=" ")
                self.statusbar.SetStatusText("Termograma encontrado")
            except:
                self.statusbar.SetStatusText("Termograma NO encontrado")

        openFileDialog.Destroy()

    def OnOpen(self, e):
        cv2.destroyAllWindows()
        self.statusbar.SetStatusText("Seleccionar Termograma")
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "All files (*.png;*.jpp;)|*.png;*.jpg|PNG files (*.png)|*.png|JPEG files (*.jpg;*.jpeg)|*.jpg;*.jpeg",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        self.path = openFileDialog.GetPath()
        self.statusbar.SetStatusText("Seleccionar Termograma")
        if self.path:
            self.image = cv2.imread(self.path, 0)
            self.image = cv2.resize(self.image, (0,0), fx=0.5, fy=0.5)
            cv2.imshow("Image", self.image)

            shape = self.image.shape
            self.image_original = np.copy(self.image)
            self.image_black = np.zeros((shape[0], shape[1]), np.uint8)

            path_text = self.path[0:len(self.path)-4] + ".txt"
            # print path_text

            try:
                self.t_r = np.loadtxt(path_text, delimiter=" ")
                self.statusbar.SetStatusText("Termograma encontrado")
            except:
                self.statusbar.SetStatusText("Termograma NO encontrado")

        openFileDialog.Destroy()

    def OnSave(self, e):
        if self.path != None:
            saveFileDialog = wx.FileDialog(self, "Save As", "", "",
                                           "All files (*.png;*.jpp;)|*.png;*.jpg|PNG files (*.png)|*.png|JPEG files (*.jpg;*.jpeg)|*.jpg;*.jpeg",
                                           wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            saveFileDialog.ShowModal()
            self.path = saveFileDialog.GetPath()
            cv2.imwrite(self.path, self.image)
            saveFileDialog.Destroy()
        else:
            self.statusbar.SetStatusText('No hay archivo que guardar')

    def OnThermogram(self, e):
        if self.path:
            self.statusbar.SetStatusText('Establece T max y T min')
            thermo = td.Thermogram(self, title='Thermogram')
            thermo.ShowModal()
            thermo.Destroy()

            self.statusbar.SetStatusText('Calculando termograma...')
            self.t_r = fc.thermogram(self.image, self.t_max, self.t_min)
            np.savetxt(self.path[0:len(self.path)-4] + ".txt", self.t_r, delimiter=' ', fmt='%2.4f')
            self.statusbar.SetStatusText('Listo')

    def OnRoi(self, e):
        def draw_circle(event, x, y, flags, param):
            global refPt
            global sel_rect_endpoint
            global cropping
            global r_dist

            r_dist = 0

            if event == cv2.EVENT_LBUTTONDOWN:
                refPt = [(x, y)]
                cropping = True
            elif event == cv2.EVENT_LBUTTONUP:
                refPt.append((x, y))
                r_dist =  int(math.sqrt((refPt[0][0]-refPt[1][0])**2 + (refPt[0][1]-refPt[1][1])**2))
                cv2.circle(self.image, refPt[0], r_dist, (255), 2)
                cv2.circle(self.image_black, refPt[0], r_dist, (255), -1)
                cropping = False
                r_dist = 0
                refPt = []
                sel_rect_endpoint = []
            elif event == cv2.EVENT_MOUSEMOVE and cropping:
                sel_rect_endpoint = [(x, y)]

        self.statusbar.SetStatusText('Enter/Espacio para aceptar, Esc para empezar de nuevo')

        image_aux = np.copy(self.image)
        cv2.setMouseCallback('Image', draw_circle)
        cv2.imshow('Image', self.image)

        while(1):
            if not cropping:
                cv2.imshow('Image', self.image)
            elif cropping and sel_rect_endpoint:
                rect_cpy = self.image.copy()
                r_dist =  int(math.sqrt((refPt[0][0]-sel_rect_endpoint[0][0])**2 + (refPt[0][1]-sel_rect_endpoint[0][1])**2))
                cv2.circle(rect_cpy, refPt[0], r_dist, (255), 2)
                cv2.imshow('Image', rect_cpy)

            k = cv2.waitKey(33)
            if k == 27:
                self.image = np.copy(image_aux)
            if k == 13 or k == 32:
                image_crop = fc.crop_roi(self.image_original, self.image_black)
                self.image = np.asarray(image_crop)

                self.statusbar.SetStatusText('Eliminando fondo...')
                th, image_umbral = cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                # image_closing = mc.closing(image_umbral, 1)
                # image_umbral = np.asarray(image_closing)
                image_umbral = np.asarray(image_umbral)
                image_crop = fc.crop_roi(self.image_original, image_umbral)
                self.image = np.asarray(image_crop)

                cv2.imshow('Image', self.image)
                self.statusbar.SetStatusText('Listo')

                break

    def OnThreshold(self, e):
        def nothing(x):
            pass

        self.statusbar.SetStatusText('Trabajando...')

        cv2.imshow('Image', self.image)
        cv2.createTrackbar('Umbral', 'Image', 210, 255, nothing)

        while(1):
            k = cv2.waitKey(33)

            value = cv2.getTrackbarPos('Umbral','Image')
            th, image_umbral = cv2.threshold(self.image, value, 255, cv2.THRESH_BINARY)
            image_add = cv2.add(self.image, image_umbral)
            cv2.imshow('Image', image_add)

            if k == 13 or k == 32 or k==27:
                break

        self.image = image_add
        image_chest = fc.chest_removal(image_umbral)
        image_umbral = np.asarray(image_chest)

        self.image = cv2.add(self.image, image_umbral)

        image_threshold = fc.threshold_2(self.image, 255)
        self.image = np.asarray(image_threshold)

        cv2.destroyWindow("Image")
        cv2.imshow('Image', self.image)

        self.statusbar.SetStatusText('Listo')

    '''
    def OnSegmentation(self, e):
        self.statusbar.SetStatusText('Realizando segmentacion...')
        # self.image, waterlines = mc.watershed(self.image)
        watershed = mc.watershed(self.image)
        self.image = np.asarray(watershed)
        cv2.imshow('Image', self.image)
        self.statusbar.SetStatusText('Listo')
    '''

    def OnAnalysisOne(self, e):
        self.statusbar.SetStatusText('Analizando imagen...')
        shape = self.image.shape
        self.t_right, self.t_left = fc.analysis_one(self.image, self.t_r)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.image, " %.2f C" % self.t_right, (shape[1]/3, shape[0]/5), font, 0.6, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(self.image, " %.2f C" % self.t_left , (2*shape[1]/3, shape[0]/5), font, 0.6, (255,255,255), 2, cv2.LINE_AA)
        cv2.imshow('Image', self.image)
        self.statusbar.SetStatusText('Listo')

        if abs(self.t_left-self.t_right) < 1:
            wx.MessageBox('SIN HALLAZGOS', 'Mensaje', wx.OK)
        else:
            wx.MessageBox('DIFERENCIA DE TEMPERATURA ANORMAL', 'Warning', wx.OK | wx.ICON_WARNING)

    def OnAnalysisTwo(self, e):
        self.statusbar.SetStatusText('Realizando segmentacion...')
        # self.image, waterlines = mc.watershed(self.image)
        watershed = fc.analysis_two(self.image, self.t_r)
        self.image = np.asarray(watershed)
        cv2.imshow('Image', self.image)
        self.statusbar.SetStatusText('Listo')

    def OnResults(self, e):
        class PDF(FPDF):
            def header(self):
                self.image('images/uaq.png', 10, 8, 25)
                self.image('images/ingenieria.png', 155, 8, 20)
                self.image('images/enfermeria.png', 177, 8, 30)
                self.add_font('DejaVuSans-Bold', '', 'fonts\DejaVuSans-Bold.ttf', uni=True)
                self.set_font('DejaVuSans-Bold', '', 13)
                self.cell(80)
                # fpdf.cell(w, h = 0, txt = '', border = 0, ln = 0, align = '', fill = False, link = '')
                self.cell(30, 10, "Universidad Autónoma de Querétaro", border=0, ln = 2, align='C')
                self.cell(30, 10, 'campus San Juan del Río', border=0, ln = 2, align='C')
                self.add_font('DejaVuSansCondensed', '', 'fonts/DejaVuSansCondensed.ttf', uni=True)
                pdf.set_font('DejaVuSansCondensed', '', 11)
                self.cell(30, 10, 'Hallazgos Termográficos', border=0, ln = 2, align='C')
                self.ln(20)

        img_temp = fc.negative_gray(self.image)
        # img_temp = cv2.applyColorMap(self.image, cv2.COLORMAP_JET)
        cv2.imwrite("images/temp.png", np.asarray(img_temp))
        self.statusbar.SetStatusText('Generando resultados...')

        ori_temp = fc.negative_gray(self.image_original)
        # ori_temp = cv2.applyColorMap(self.image_original, cv2.COLORMAP_JET)
        cv2.imwrite("images/ori.png", np.asarray(ori_temp))

        pdf = PDF('P', 'mm', 'Letter')
        pdf.add_page()
        pdf.add_font('DejaVuSansMono', '', 'fonts/DejaVuSansMono.ttf', uni=True)
        pdf.set_font('DejaVuSansMono', '', 10)
        pdf.cell(30, 10, 'Análisis de Termograma', border=0, ln = 0, align='L')
        pdf.cell(0, 10, 'Fecha: ' + time.strftime("%d/%m/%y"), border=0, ln = 1, align='R')
        pdf.cell(30, 10, 'Voluntaria: ' + self.name, border=0, ln = 2, align='L')
        pdf.image('images/ori.png', x=12, y=82, w=90)
        pdf.image('images/temp.png', x=114, y=82, w=90)

        pdf.ln(80)

        pdf.cell(30, 10, "Resultado", border=0, ln = 2, align='L')
        pdf.cell(30, 10, 'La temperatura promedio del seno derecho es de %.2f °C.' % self.t_right, border=0, ln = 2, align='L')
        pdf.cell(30, 10, 'La temperatura promedio del seno izquierdo es de %.2f °C.' % self.t_left, border=0, ln = 2, align='L')
        pdf.ln(10)
        pdf.cell(30, 10, 'El diferencial de temperaturas (ΔT) de es de %.2f °C. El rango considerado normal es ΔT < 1 °C. ' % abs(self.t_left-self.t_right), border=0, ln = 2, align='L')
        pdf.ln(10)
        if abs(self.t_left - self.t_right) < 1:
            pdf.cell(30, 10, "SIN HALLAZGOS", border=0, ln = 2, align='L')
        else:
            pdf.cell(30, 10, "DIFERENCIA DE TEMPERATURA ANORMAL", border=0, ln = 2, align='L')
        pdf.ln(10)

        pdf.cell(30, 10, "NOTA: La termografía no sustituye el ultrasonido ni la mastografía.", border=0, ln = 2, align='L')

        pdf.output(self.path[0:len(self.path)-4] + ".pdf", 'F')

        self.statusbar.SetStatusText('Listo')

    def AboutMessage(self, e):
        wx.MessageBox(
            'UAQ Thermo Breast Cancer \n Marco Garduño \n mgarduno01@alumnos.uaq.mx',
            'Info', wx.OK)
