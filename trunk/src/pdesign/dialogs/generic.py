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

import wx

from pdesign.widgets import HLine, const

class GenericDialog(wx.Dialog):

	def __init__(self, parent, title, size=(-1, -1)):

		wx.Dialog.__init__(self, parent, -1, title, wx.DefaultPosition, size)

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.sizer)

		self.hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.hbox, 0, wx.ALL)

		self.build()

		line = HLine(self)
		self.sizer.Add(line, 0, wx.ALL)

		self.button_box = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.button_box, 0, wx.ALL | wx.ALIGN_RIGHT)

		ok_btn = wx.Button(self, wx.ID_OK, "", wx.DefaultPosition, wx.DefaultSize, 0)
		self.Bind(wx.EVT_BUTTON, self.on_ok, ok_btn)

		cancel_btn = wx.Button(self, wx.ID_CANCEL, "", wx.DefaultPosition, wx.DefaultSize, 0)
		self.Bind(wx.EVT_BUTTON, self.on_cancel, cancel_btn)
		if const.is_gtk():
			self.button_box.Add(cancel_btn, 0, wx.ALL | wx.ALIGN_RIGHT)
			self.button_box.Add(ok_btn, 0, wx.ALL | wx.ALIGN_RIGHT)
		else:
			self.button_box.Add(ok_btn, 0, wx.ALL | wx.ALIGN_RIGHT)
			self.button_box.Add(cancel_btn, 0, wx.ALL | wx.ALIGN_RIGHT)
		self.sizer.Fit(self)

	def build(self):pass

	def on_ok(self, event):
		self.EndModal(wx.ID_OK)

	def on_cancel(self, event):
		self.EndModal(wx.ID_CANCEL)
