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

from pdesign import _
from pdesign.widgets import BOTTOM, EXPAND, ALL, VERTICAL, HORIZONTAL
from pdesign.widgets import const, HPanel, VPanel, Button

class LogViewerDialog(wx.Dialog):

	sizer = None
	box = None
	button_box = None
	ok_btn = None
	cancel_btn = None

	def __init__(self, parent, title, size=(500, 350)):

		wx.Dialog.__init__(self, parent, -1, title, wx.DefaultPosition, size)

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.sizer)

		margin = 5
		if not const.is_gtk(): margin = 10

		self.box = VPanel(self, border=BOTTOM, space=margin)
		self.sizer.Add(self.box, 1, ALL | EXPAND)

		self.build()

		self.bottom_box = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.bottom_box, 0, EXPAND, 5)
		self.clear_btn = wx.Button(self, -1, _('Clear history'), wx.DefaultPosition,
							wx.DefaultSize, 0)
		self.bottom_box.Add(self.clear_btn, 0, wx.ALL , 5)
		expander = HPanel(self)
		self.bottom_box.Add(expander, 1, wx.ALL , 5)

		self.button_box = wx.BoxSizer(wx.HORIZONTAL)
		self.bottom_box.Add(self.button_box, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

		self.open_btn = wx.Button(self, wx.ID_OPEN, "", wx.DefaultPosition,
							wx.DefaultSize, 0)
		self.Bind(wx.EVT_BUTTON, self.on_open, self.open_btn)

		self.cancel_btn = wx.Button(self, wx.ID_CANCEL, "", wx.DefaultPosition,
								wx.DefaultSize, 0)
		self.Bind(wx.EVT_BUTTON, self.on_cancel, self.cancel_btn)
		if const.is_gtk():
			self.button_box.Add(self.cancel_btn, 0, wx.ALIGN_RIGHT)
			self.button_box.Add(self.open_btn, 0, wx.ALIGN_RIGHT)
		elif const.is_msw():
			self.button_box.Add(self.open_btn, 0, ALL | wx.ALIGN_RIGHT)
			self.button_box.Add(self.cancel_btn, 0, ALL | wx.ALIGN_RIGHT)
		else:
			self.button_box.Add(self.open_btn, 0, ALL | wx.ALIGN_RIGHT, 5)
			self.button_box.Add(self.cancel_btn, 0, ALL | wx.ALIGN_RIGHT, 5)
		self.cancel_btn.SetDefault()

	def build(self):
		lc = wx.ListCtrl(self.box, -1, style=wx.LC_REPORT)
		self.box.add(lc, 1, ALL | EXPAND)

	def on_open(self, *args):
		self.EndModal(wx.ID_OK)

	def on_cancel(self, event):
		self.EndModal(wx.ID_CANCEL)

def log_viewer_dlg(parent):
	dlg = LogViewerDialog(parent, _("Recent documents"))
	dlg.Centre()
	dlg.ShowModal()
	dlg.Destroy()
