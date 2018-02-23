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
import math

import functions as f
import functions_c as fc
import morphology as m
import morphology_c as mc

ID_EXIT = 1
ID_ABOUT = 2
ID_TERMO = 3
ID_ROI = 4
ID_THRES = 5
ID_SEG = 6
ID_ANAL = 7

class Thermogram(wx.Dialog):
    def __init__(self, *args, **kw):
        super(Thermogram, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        self.SetSize((200, 150))

        # Configuration File .txt
        self.file = open("config.txt","r")
        data = self.file.readlines()
        self.file.close()
        self.t_min = float(data[1])
        self.t_max = float(data[3])

        # Panel
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.tx1 = wx.TextCtrl(pnl)
        self.tx2 = wx.TextCtrl(pnl)

        self.tx1.SetValue(str(float(self.t_min)))
        self.tx2.SetValue(str(float(self.t_max)))

        sb = wx.StaticBox(pnl, label='Thermogram Info')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(pnl, label='T min'))
        hbox1.Add(self.tx1, flag=wx.LEFT, border=10)
        hbox1.Add(wx.StaticText(pnl, label=' ° C'))
        sbs.Add(hbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(wx.StaticText(pnl, label='T max'))
        hbox2.Add(self.tx2, flag=wx.LEFT, border=9)
        hbox2.Add(wx.StaticText(pnl, label=' ° C'))
        sbs.Add(hbox2)

        pnl.SetSizer(sbs)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Accept')
        closeButton = wx.Button(self, label='Close')
        hbox3.Add(okButton)
        hbox3.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox3,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=5)

        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnAccept)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnAccept(self, e):
        self.t_min = self.tx1.GetValue()
        self.t_max = self.tx2.GetValue()

        if(self.t_min > self.t_max):
            print "Error"
        elif(float(self.t_min) < 0):
            print "Error"
        else:
            file = open("config.txt","w")
            file.write("T_MIN\n")
            file.write(str(self.t_min)+"\n")
            file.write("T_MAX\n")
            file.write(str(self.t_max))
            file.close()
            self.Destroy()

            return self.t_min, self.t_max

    def OnClose(self, e):
        self.Destroy()

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

        # Configuration File .txt
        self.file = open("config.txt","r")
        data = self.file.readlines()
        self.file.close()
        self.t_min = float(data[1])
        self.t_max = float(data[3])

        # GUI design
        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        editMenu = wx.Menu()
        diagMenu = wx.Menu()
        helpMenu = wx.Menu()

        fileMenu.Append(wx.ID_NEW, '&New')
        fileMenu.Append(wx.ID_OPEN, '&Open')
        fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        qmi = wx.MenuItem(fileMenu, ID_EXIT, '&Quit\tCtrl+Q')
        fileMenu.Append(qmi)

        editMenu.Append(ID_TERMO, '&Thermogram')
        editMenu.Append(ID_ROI, '&ROI')
        editMenu.Append(ID_THRES, '&Threshold')

        diagMenu.Append(ID_SEG, '&Segmentation')
        diagMenu.Append(ID_ANAL, '&Analysis')

        helpMenu.Append(ID_ABOUT, '&About')

        self.Bind(wx.EVT_MENU, self.OnQuit, id=ID_EXIT)
        self.Bind(wx.EVT_MENU, self.OnNew, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)

        self.Bind(wx.EVT_MENU, self.AboutMessage, id=ID_ABOUT)

        self.Bind(wx.EVT_MENU, self.OnThermogram, id=ID_TERMO)
        self.Bind(wx.EVT_MENU, self.OnRoi, id=ID_ROI)
        self.Bind(wx.EVT_MENU, self.OnThreshold, id=ID_THRES)

        self.Bind(wx.EVT_MENU, self.OnSegmentation, id=ID_SEG)
        self.Bind(wx.EVT_MENU, self.OnAnalysis, id=ID_ANAL)

        menubar.Append(fileMenu, '&File')
        menubar.Append(editMenu, '&Edit')
        menubar.Append(diagMenu, '&Diagnosis')
        menubar.Append(helpMenu, '&Help')

        self.SetMenuBar(menubar)

        # Window parameters
        self.SetSize((500, 80))
        self.SetTitle('UAQ Thermo Breast Cancer')
        self.Centre()
        self.Show(True)

        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('UAQ Breast Cancer')

        self.SetMinSize(self.GetSize())
        self.SetMaxSize(self.GetSize())

    def OnQuit(self, e):
        self.Close()

    def OnNew(self, e):
        cv2.destroyAllWindows()

        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "All files (*.png;*.jpp;)|*.png;*.jpg|PNG files (*.png)|*.png|JPEG files (*.jpg;*.jpeg)|*.jpg;*.jpeg",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        self.path = openFileDialog.GetPath()
        if self.path:
            self.image = cv2.imread(self.path, 0)
            cv2.imshow("Image", self.image)

            shape = self.image.shape
            self.image_original = np.copy(self.image)
            self.image_black = np.zeros((shape[0], shape[1]), np.uint8)

            path_text = self.path[0:len(self.path)-4] + ".txt"
            print path_text

            try:
                self.t_r = np.loadtxt(path_text, delimiter=" ")
                print "Termograma encontrado"
            except:
                print "Termograma NO encontrado"

        openFileDialog.Destroy()

    def OnOpen(self, e):
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "All files (*.png;*.jpp;)|*.png;*.jpg|PNG files (*.png)|*.png|JPEG files (*.jpg;*.jpeg)|*.jpg;*.jpeg",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        self.path = openFileDialog.GetPath()
        if self.path:
            self.image = cv2.imread(self.path, 0)
            cv2.imshow("Image", self.image)

            shape = self.image.shape
            self.image_original = np.copy(self.image)
            self.image_black = np.zeros((shape[0], shape[1]), np.uint8)

            path_text = self.path[0:len(self.path)-4] + ".txt"
            print path_text

            try:
                self.t_r = np.loadtxt(path_text, delimiter=" ")
                print "Termograma encontrado"
            except:
                print "Termograma NO encontrado"

        openFileDialog.Destroy()

    def OnSave(self, e):
        saveFileDialog = wx.FileDialog(self, "Save As", "", "",
                                       "All files (*.png;*.jpp;)|*.png;*.jpg|PNG files (*.png)|*.png|JPEG files (*.jpg;*.jpeg)|*.jpg;*.jpeg",
                                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        saveFileDialog.ShowModal()
        self.path = saveFileDialog.GetPath()
        cv2.imwrite(self.path, self.image)
        saveFileDialog.Destroy()

    def OnThermogram(self, e):
        if self.path:
            self.statusbar.SetStatusText('Establece T max y T min')
            thermo = Thermogram(self, title='Thermogram')
            thermo.ShowModal()
            thermo.Destroy()

            self.statusbar.SetStatusText('Calculando termograma...')
            self.t_r = fc.thermogram(self.image, self.t_max, self.t_min)
            np.savetxt(self.path[0:len(self.path)-4] + ".txt", self.t_r, delimiter=' ', fmt='%2.4f')
            self.statusbar.SetStatusText('Listo')

    def OnRoi(self, e):
        def draw_circle(event, x, y, flags, param):
            global refPt
            if event == cv2.EVENT_LBUTTONDOWN:
                refPt = [(x, y)]
            elif event == cv2.EVENT_LBUTTONUP:
                refPt.append((x, y))
                r_dist =  int(math.sqrt((refPt[0][0]-refPt[1][0])**2 + (refPt[0][1]-refPt[1][1])**2))
                cv2.circle(self.image, refPt[0], r_dist, (255), 2)
                cv2.circle(self.image_black, refPt[0], r_dist, (255), -1)

        self.statusbar.SetStatusText('Enter/Espacio para aceptar, Esc para empezar de nuevo')

        image_aux = np.copy(self.image)
        cv2.setMouseCallback('Image', draw_circle)
        cv2.imshow('Image', self.image)

        while(1):
            cv2.imshow('Image', self.image)
            k = cv2.waitKey(33)
            if k == 27:
                self.image = np.copy(image_aux)
            if k == 13 or k == 32:
                self.image = fc.crop_roi(self.image_original, self.image_black)

                self.statusbar.SetStatusText('Eliminando fondo...')
                th, image_umbral = cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                image_umbral = mc.closing(image_umbral, 3)
                self.image = fc.crop_roi(self.image_original, image_umbral)
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
        image_umbral = fc.chest_removal(image_umbral)
        self.image = cv2.add(self.image, image_umbral)
        self.image = fc.threshold_2(self.image, 255)

        cv2.destroyWindow("Image")
        cv2.imshow('Image', self.image)

        self.statusbar.SetStatusText('Listo')

    def OnSegmentation(self, e):
        self.statusbar.SetStatusText('Realizando segmentacion...')
        self.image, waterlines = m.watershed(self.image)
        cv2.imshow('Image', self.image)
        self.statusbar.SetStatusText('Listo')

    def OnAnalysis(self, e):
        self.statusbar.SetStatusText('Analizando imagen...')
        shape = self.image.shape
        t_left, t_right = f.analysis(self.image, self.t_r)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.image, " %.2f C" % t_left, (shape[1]/3, shape[0]/5), font, 0.6, (255,255,255), 2, cv2.LINE_AA)
        cv2.putText(self.image, " %.2f C" % t_right , (2*shape[1]/3, shape[0]/5), font, 0.6, (255,255,255), 2, cv2.LINE_AA)
        cv2.imshow('Image', self.image)
        self.statusbar.SetStatusText('Listo')

    def AboutMessage(self, e):
        wx.MessageBox(
            'UAQ Thermo Breast Cancer \n Marco Garduño \n mgarduno01@alumnos.uaq.mx',
            'Info', wx.OK)

def main():
    ex = wx.App()
    Example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()
