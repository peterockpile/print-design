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

from pdesign import events, modes, config
from pdesign.resources import pdids

EDIT = [wx.ID_CUT, wx.ID_COPY, wx.ID_PASTE, wx.ID_DELETE, None, wx.ID_SELECTALL]

class CtxMenuBuilder:

	app = None
	mw = None
	insp = None
	actions = None
	items = []

	def __init__(self, app, parent):
		self.app = app
		self.mw = app.mw
		self.parent = parent
		self.insp = self.app.insp
		self.actions = self.app.actions
		self.menu = wx.Menu()

	def build_menu(self):
		for item in self.items: self.menu.RemoveItem(item)
		self.items = []

		entries = EDIT
		for item in entries:
			if item is None:
				self.items.append(self.menu.AppendSeparator())
			else:
				action = self.app.actions[item]
				menuitem = CtxActionMenuItem(self.parent, self.menu, action)
				self.menu.AppendItem(menuitem)
				menuitem.update()
				self.items.append(menuitem)
		return self.menu

class CtxActionMenuItem(wx.MenuItem):

	def __init__(self, mw, parent, action):
		self.mw = mw
		self.parent = parent
		self.action = action
		action_id = action.action_id
		text = self.action.get_menu_text()
		if self.action.is_acc:
			text += '\t' + self.action.get_shortcut_text()
		wx.MenuItem.__init__(self, parent, action_id, text=text)
		if not config.is_mac() and self.action.is_icon:
			bmp = self.action.get_icon(config.menu_size, wx.ART_MENU)
			if bmp: self.SetBitmap(bmp)
		self.action.register(self)
		self.mw.Bind(wx.EVT_MENU, self.action.do_call, id=action_id)
		if self.action.is_toggle():
			self.SetCheckable(True)

	def update(self):
		self.set_enable(self.action.enabled)
		if self.action.is_toggle():
			self.set_active(self.action.active)

	def set_enable(self, enabled):
		self.Enable(enabled)

	def set_active(self, val):
		if not self.IsChecked() == val and self.IsCheckable():
			self.Toggle()
