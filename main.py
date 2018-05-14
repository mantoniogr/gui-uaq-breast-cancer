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
import mainWindow as mw

def main():
    ex = wx.App()
    mw.Example(None)
    ex.MainLoop()

if __name__ == '__main__':
    main()
