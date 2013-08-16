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
from pdesign.dialogs.license import LICENSE
from pdesign.dialogs.credits import CREDITS

def about_dialog(parent):

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

	wx.AboutBox(info)
