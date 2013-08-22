#! /usr/bin/python
# -*- coding: utf-8 -*-
#
#	Copyright (C) 2013 by Igor E. Novikov
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os


import wx

def check_config():
	home=os.path.expanduser('~')
	cfg_dir=os.path.join(home,'.cfg','test')
	if not os.path.lexists(cfg_dir):
		os.makedirs(cfg_dir)

class Frame(wx.Frame):
	def __init__(self, title):
		wx.Frame.__init__(self, None, title=title, size=(350,200))
		sizer=wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(sizer)
		panel=wx.Panel(self)
		psizer=wx.BoxSizer(wx.VERTICAL)
		panel.SetSizer(psizer)
		sizer.Add(panel,1,wx.ALL|wx.EXPAND)
		txt=wx.StaticText(panel, -1, sys.getdefaultencoding())
		psizer.Add(txt,0,wx.ALL)
		txt=wx.StaticText(panel, -1, sys.getfilesystemencoding())
		psizer.Add(txt,0,wx.ALL)
		txt=wx.StaticText(panel, -1, os.path.expanduser('~'))
		psizer.Add(txt,0,wx.ALL)
		button=wx.Button(panel,-1, u'Проба')
		button.Bind(wx.EVT_BUTTON, self.on_click)
		psizer.Add(button,0,wx.ALL)
		
		self.Layout()
		
	def on_click(self, event):
		ret=None
		dlg = wx.FileDialog(
			self, message="Open",
			defaultDir=os.path.expanduser('~'),
			defaultFile="",
			wildcard="All files|*.*",
			style=wx.OPEN | wx.CHANGE_DIR | wx.FILE_MUST_EXIST)
			
		dlg.CenterOnParent()
		if dlg.ShowModal() == wx.ID_OK:
			ret = dlg.GetPath()
		dlg.Destroy()
		print ret

check_config()
app = wx.App()
top = Frame("Hello World")
top.Show()
app.MainLoop()