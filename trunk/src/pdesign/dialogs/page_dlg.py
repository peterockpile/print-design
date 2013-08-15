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
from pdesign.widgets import Label, Spin
from generic import GenericDialog

class GotoPageDialog(GenericDialog):

	presenter = None

	def __init__(self, parent, title, presenter):
		self.presenter = presenter
		GenericDialog.__init__(self, parent, title)

	def build(self):
		label = Label(self, _("Page No.:"))
		self.hbox.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		pages = self.presenter.get_pages()
		page_num = len(pages)
		current_page = pages.index(self.presenter.active_page) + 1

		self.spin = Spin(self, current_page, (1, page_num))
		self.hbox.Add(self.spin, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

	def get_result(self):
		return self.spin.get_value() - 1

def goto_page_dlg(parent, presenter):
	dlg = GotoPageDialog(parent, _("Go to page..."), presenter)
	dlg.Centre()
	if dlg.ShowModal() == wx.ID_OK:
		ret = dlg.get_result()
	else:
		ret = None
	dlg.Destroy()
	return ret
