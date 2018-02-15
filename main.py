#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
UAQ Thermo Breast Cancer

author: Marco Garduno
website:
last modified: August 2018
'''

import wx
import cv2
import numpy

APP_EXIT = 1
ROI = 2
TH = 3
Segm = 4
Proc = 5
About = 6
Termo = 7

class Thermogram(wx.Dialog):
    def __init__(self, *args, **kw):
        super(Thermogram, self).__init__(*args, **kw)
        self.InitUI()

    def InitUI(self):
        self.SetSize((200, 150))
        # self.SetTitle("Thermogram")

        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.tx1 = wx.TextCtrl(pnl)
        self.tx2 = wx.TextCtrl(pnl)

        self.tx1.SetValue("20.0")
        self.tx2.SetValue("25.0")

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
        t_min = self.tx1.GetValue()
        t_max = self.tx2.GetValue()

        if(t_min > t_max):
            print "Error"
        elif(float(t_min) < 0):
            print "Error"
        else:
            file = open("config.txt","w")
            file.write("T_MIN\n")
            file.write(str(t_min)+"\n")
            file.write("T_MAX\n")
            file.write(str(t_max))
            file.close()
            self.Destroy()

    def OnClose(self, e):
        self.Destroy()

class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
        # Configuration File .txt
        self.file = open("config.txt","r")
        data = self.file.readlines()
        self.file.close()
        self.t_min = float(data[1])
        self.t_max = float(data[3])

        menubar = wx.MenuBar()
        self.image = None

        fileMenu = wx.Menu()
        editMenu = wx.Menu()
        diagMenu = wx.Menu()
        helpMenu = wx.Menu()

        fileMenu.Append(wx.ID_NEW, '&New')
        fileMenu.Append(wx.ID_OPEN, '&Open')
        fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()
        qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
        #qmi.SetBitmap(wx.Bitmap('close_red.png'))
        fileMenu.Append(qmi)

        editMenu.Append(Termo, '&Thermogram')
        editMenu.Append(ROI, '&ROI')
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
        path = openFileDialog.GetPath()
        if path:
            self.image = cv2.imread(path)
            cv2.imshow("Image", self.image)
        openFileDialog.Destroy()

    def OnOpen(self, e):
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "Image files (*.png)|*.png",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()
        if path:
            self.image = cv2.imread(path)
            cv2.imshow("Image", self.image)
        openFileDialog.Destroy()

    def OnSave(self, e):
        saveFileDialog = wx.FileDialog(self, "Save As", "", "",
                                       "Image files (*.png)|*.png",
                                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        saveFileDialog.ShowModal()
        path = saveFileDialog.GetPath()
        cv2.imwrite(path, self.image)
        saveFileDialog.Destroy()

    def OnProcess(self, e):
        thresh1, self.image = cv2.threshold(self.image, 127, 255, cv2.THRESH_BINARY)
        cv2.imshow("Image", self.image)

    def OnThermogram(self, e):
        thermo = Thermogram(None, title='Thermogram')
        thermo.ShowModal()
        thermo.Destroy()

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
