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

APP_EXIT = 1
ROI = 2
TH = 3
Segm = 4
Proc = 5
About = 6
Termo = 7
ID_ROI = 8

class Roi(wx.Dialog):
    def __init__(self, *args, **kw):
        super(Roi, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        self.SetSize((250, 150))

        # Panel
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.sp1 = wx.SpinCtrl(pnl, size=(90,-1), min=1, max=120)
        self.sp2 = wx.SpinCtrl(pnl, size=(90,-1), min=1, max=120)
        self.sp3 = wx.SpinCtrl(pnl, size=(90,-1), min=1, max=120)
        self.sp4 = wx.SpinCtrl(pnl, size=(90,-1), min=1, max=120)

        sb = wx.StaticBox(pnl, label='ROI Info')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(pnl, label='X1'))
        hbox1.Add(self.sp1, flag=wx.LEFT, border=10)
        hbox1.Add(wx.StaticText(pnl, label=' X2'))
        hbox1.Add(self.sp2, flag=wx.LEFT, border=10)
        sbs.Add(hbox1)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(wx.StaticText(pnl, label='Y1'))
        hbox2.Add(self.sp3, flag=wx.LEFT, border=10)
        hbox2.Add(wx.StaticText(pnl, label=' Y2'))
        hbox2.Add(self.sp4, flag=wx.LEFT, border=10)
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
        self.Destroy()

    def OnClose(self, e):
        self.Destroy()

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
        self.image = None
        self.path = None

        # Configuration File .txt
        self.file = open("config.txt","r")
        data = self.file.readlines()
        self.file.close()

        self.t_min = float(data[1])
        self.t_max = float(data[3])

        menubar = wx.MenuBar()

        fileMenu = wx.Menu()
        editMenu = wx.Menu()
        diagMenu = wx.Menu()
        helpMenu = wx.Menu()

        fileMenu.Append(wx.ID_NEW, '&New')
        fileMenu.Append(wx.ID_OPEN, '&Open')
        fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
        fileMenu.Append(qmi)

        editMenu.Append(Termo, '&Thermogram')
        editMenu.Append(ID_ROI, '&ROI')
        editMenu.Append(TH, '&Threshold')
        editMenu.Append(Segm, '&Segmentation')

        diagMenu.Append(Proc, '&Process')

        helpMenu.Append(About, '&About')

        self.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)
        self.Bind(wx.EVT_MENU, self.OnNew, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)

        self.Bind(wx.EVT_MENU, self.AboutMessage, id=About)

        self.Bind(wx.EVT_MENU, self.OnThermogram, id=Termo)
        self.Bind(wx.EVT_MENU, self.OnRoi, id=ID_ROI)
        self.Bind(wx.EVT_MENU, self.OnProcess, id=Proc)

        menubar.Append(fileMenu, '&File')
        menubar.Append(editMenu, '&Edit')
        menubar.Append(diagMenu, '&Diagnosis')
        menubar.Append(helpMenu, '&Help')
        self.SetMenuBar(menubar)

        # Window parameters
        self.SetSize((500,60))
        self.SetTitle('UAQ Thermo Breast Cancer')
        self.Centre()
        self.Show(True)
        # Window parameters

    def OnQuit(self, e):
        self.Close()

    def OnNew(self, e):
        cv2.destroyAllWindows()

        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "Image files (*.png)|*.png",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        self.path = openFileDialog.GetPath()
        if self.path:
            self.image = cv2.imread(self.path)
            cv2.imshow("Image", self.image)
        openFileDialog.Destroy()

    def OnOpen(self, e):
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "Image files (*.png)|*.png",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        self.path = openFileDialog.GetPath()
        if self.path:
            self.image = cv2.imread(self.path, 0)
            cv2.imshow("Image", self.image)
        openFileDialog.Destroy()

    def OnSave(self, e):
        saveFileDialog = wx.FileDialog(self, "Save As", "", "",
                                       "Image files (*.png)|*.png",
                                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        saveFileDialog.ShowModal()
        self.path = saveFileDialog.GetPath()
        cv2.imwrite(self.path, self.image)
        saveFileDialog.Destroy()

    def OnProcess(self, e):
        thresh1, self.image = cv2.threshold(self.image, 127, 255, cv2.THRESH_BINARY)
        cv2.imshow("Image", self.image)

    def OnRoi(self, e):
        # mouse callback function
        image_aux = np.copy(self.image)

        def draw_circle(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDBLCLK:
                cv2.circle(self.image, (x,y), 25, (255), 3)

        cv2.setMouseCallback('Image', draw_circle)
        cv2.imshow('Image',self.image)

        while(1):
            cv2.imshow('Image',self.image)
            k = cv2.waitKey(33)
            if k == 27:
                self.image = np.copy(image_aux)
            if k == 13 or k == 32:
                break

    def OnThermogram(self, e):
        if self.path:
            thermo = Thermogram(self, title='Thermogram')
            thermo.ShowModal()
            thermo.Destroy()

            t_r = f.thermogram(self.image, self.t_max, self.t_min)
            np.savetxt(self.path[0:len(self.path)-4] + ".txt", t_r, delimiter=' ', fmt='%2.4f')

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
