#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
ZetCode wxPython tutorial

This example shows a simple menu.

author: Jan Bodnar
website: www.zetcode.com
last modified: September 2011
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

class Window(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.InitUI()

    def InitUI(self):
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
        fileMenu.Append(qmi)

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
        openFileDialog.Destroy()
        self.image = cv2.imread(path)
        cv2.imshow("Image", self.image)

    def OnOpen(self, e):
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "Image files (*.png)|*.png",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()
        openFileDialog.Destroy()
        self.image = cv2.imread(path)
        cv2.imshow("Image", self.image)

    def OnSave(self, e):
        saveFileDialog = wx.FileDialog(self, "Save As", "", "",
                                       "Image files (*.png)|*.png",
                                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        saveFileDialog.ShowModal()
        path = saveFileDialog.GetPath()
        cv2.imwrite(path, self.image)
        saveFileDialog.Destroy()

    def AboutMessage(self, e):
        wx.MessageBox(
            'UAQ Thermo Breast Cancer \n Marco Garduño \n mgarduno01@alumnos.uaq.mx',
            'Info', wx.OK)

def main():
    app = wx.App()
    Window(None)
    app.MainLoop()

if __name__ == '__main__':
    main()
