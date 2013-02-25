# -*- coding: utf-8 -*-
#
#	Copyright (C) 2012 by Igor E. Novikov
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

import gtk

from pdesign import _, config

DIALOG = None
PREFS = None

def get_prefs_dialog(app):

	global DIALOG, PREFS

	if DIALOG is None:
		parent = app.mw
		title = _('%s Preferences') % (app.appdata.app_name)

		DIALOG = gtk.Dialog(title, parent,
		                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
		                   (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
		                    gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))


		vbox = gtk.VBox()
		vbox.set_border_width(5)
		vbox.show_all()
		DIALOG.vbox.pack_start(vbox)

	ret = DIALOG.run()
	if ret == gtk.RESPONSE_ACCEPT:
		app.proxy.force_redraw()
	DIALOG.hide()

class PrefsContainer(gtk.HPaned):

	def __init__(self, app):
		self.app = app
		gtk.HPaned.__init__(self)

class PrefsLeaf(gtk.VBox):

	childs = []

	def __init__(self, app):
		self.app = app
		gtk.HPaned.__init__(self)
