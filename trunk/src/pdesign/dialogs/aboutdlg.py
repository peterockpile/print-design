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
from pdesign.resources import icons

from pdesign.widgets import const, EXPAND, ALL, LEFT, CENTER
from pdesign.widgets import HPanel, VPanel, Notebook, Label, HLine, HtmlLabel
from pdesign.widgets import Entry

from pdesign.dialogs.license import LICENSE
from pdesign.dialogs.credits import CREDITS

class PDAboutDialog(wx.Dialog):

	sizer = None
	app = None

	def __init__(self, app, parent, title, size=(500, 350)):
		self.app = app
		wx.Dialog.__init__(self, parent, -1, title, wx.DefaultPosition, size)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.SetSizer(self.sizer)

		margin = 5
		if not const.is_gtk(): margin = 10

		self.box = VPanel(self, space=margin)
		self.sizer.Add(self.box, 1, ALL | EXPAND)

		self.build()

		self.box.add(HLine(self), 0, ALL | EXPAND)

		self.button_box = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.button_box, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

		self.close_btn = wx.Button(self, wx.ID_CLOSE, "", wx.DefaultPosition,
							wx.DefaultSize, 0)
		self.button_box.Add(self.close_btn, 0, wx.ALIGN_RIGHT)
		self.Bind(wx.EVT_BUTTON, self.close_dlg, self.close_btn)
		self.close_btn.SetDefault()
		#self.sizer.Fit(self)

	def close_dlg(self, event):
		self.EndModal(wx.ID_OK)

	def build(self):
		header = AboutHeader(self.app, self.box)
		self.box.add(header, 0, ALL | EXPAND, 5)

		nb = Notebook(self.box)
		nb.add_page(AboutPage(self.app, nb), _('About'))
		nb.add_page(ComponentsPage(self.app, nb), _('Components'))
		nb.add_page(AuthorsPage(nb), _('Authors'))
		nb.add_page(ThanksPage(nb), _('Thanks to'))
		nb.add_page(LicensePage(nb), _('License'))
		self.box.add(nb, 1, ALL | EXPAND, 5)


class AboutHeader(HPanel):

	def __init__(self, app, parent):
		HPanel.__init__(self, parent)
		self.set_bg(const.UI_COLORS['pressed_border'])

		panel = HPanel(self)
		color = const.lighter_color(const.UI_COLORS['bg'], 0.9)
		panel.set_bg(color)
		bmp = wx.ArtProvider.GetBitmap(icons.PDESIGN_ICON32, size=const.DEF_SIZE)
		bitmap = wx.StaticBitmap(panel, -1, bmp)
		panel.add(bitmap, 0, ALL, 5)

		data = app.appdata

		p = VPanel(panel)
		p.set_bg(color)
		p.add(Label(p, data.app_name, True, 3), 0, ALL | EXPAND, 0)
		txt = ('%s: %s %s') % (_('Version'), data.version, data.revision)
		p.add(Label(p, txt), 0, ALL | EXPAND, 0)
		panel.add(p, 0, LEFT | CENTER, 0)

		self.add(panel, 1, ALL | EXPAND, 1)

class AboutPage(HPanel):

	def __init__(self, app, parent):
		HPanel.__init__(self, parent)
		self.add((50, 10))
		box = VPanel(self)
		self.add(box, 0, LEFT | CENTER, 5)
		data = app.appdata
		txt = data.app_name + ' - ' + _('vector graphics editor') + '\n'
		box.add(Label(box, txt, True, 2))
		txt = '(C) 2011-2013 sK1 Project team' + '\n'
		box.add(Label(box, txt))
		box.add(HtmlLabel(box, 'http://sk1project.org'))

class ComponentsPage(VPanel):

	def __init__(self, app, parent):
		VPanel.__init__(self, parent)
		lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
		lc.InsertColumn(0, _('Library'))
		lc.InsertColumn(1, _('Version'))
		data = app.appdata.components
		for item in data: lc.Append(item)
		self.add(lc, 1, EXPAND, 5)
		lc.SetColumnWidth(1, wx.wx.LIST_AUTOSIZE)

class AuthorsPage(VPanel):

	def __init__(self, parent):
		VPanel.__init__(self, parent)
		sep = "------------------------------\n"
		dev = "\nIgor E. Novikov\n"
		dev += "(PrintDesign, wxWidgets version; sK1, Tk version)\n"
		dev += "<igor.e.novikov@gmail.com>\n\n" + sep
		dev += 'PrintDesign is based on sK1 0.9.x and Skencil 0.6.x experience.'
		dev += '\n' + sep
		dev += "Bernhard Herzog (Skencil, Tk version)\n"
		dev += "<bernhard@users.sourceforge.net>\n" + sep
		entry = Entry(self, dev, multiline=True, editable=False)
		self.add(entry, 1, ALL | EXPAND, 5)

class ThanksPage(VPanel):

	def __init__(self, parent):
		VPanel.__init__(self, parent)
		from pdesign.dialogs.credits import CREDITS
		entry = Entry(self, CREDITS, multiline=True, editable=False)
		self.add(entry, 1, ALL | EXPAND, 5)

class LicensePage(VPanel):

	def __init__(self, parent):
		VPanel.__init__(self, parent)
		from pdesign.dialogs.license import LICENSE
		entry = Entry(self, LICENSE, multiline=True, editable=False)
		self.add(entry, 1, ALL | EXPAND, 5)

def about_dialog(app, parent):

	info = wx.AboutDialogInfo()
	info.Name = "PrintDesign"
	info.Version = "1.0"
	info.Copyright = "(C) 2013 Igor E. Novikov"
	descr = '(rev.497 preview build)\n'
	descr += _("Vector graphics editor based on sK1 0.9.x\n")
	descr += _("and Skencil 0.6.x experience.")
	info.Description = descr
	info.WebSite = ("http://sk1project.org", "http://sk1project.org")

	sep = "------------------------------\n"
	main_dev = "\nIgor E. Novikov\n"
	main_dev += "(PrintDesign, wxWidgets version; sK1, Tk version)\n"
	main_dev += "<igor.e.novikov@gmail.com>\n\n" + sep
	init_dev = "Bernhard Herzog (Skencil, Tk version)\n"
	init_dev += "<bernhard@users.sourceforge.net>\n" + sep
#	info.Developers = [main_dev, init_dev, CREDITS]

#	info.License = LICENSE
	title = _('About') + ' ' + app.appdata.app_name
	dlg = PDAboutDialog(app, parent, title)
	dlg.Centre()
	dlg.ShowModal()
	dlg.Destroy()
