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
