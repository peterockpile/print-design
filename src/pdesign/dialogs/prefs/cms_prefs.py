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

import gtk
from pdesign import _, appconst

from pdesign.dialogs.prefs.generic import GenericPrefsPlugin

class CmsPrefsPlugin(GenericPrefsPlugin):

	name = 'CmsPrefsPlugin'
	title = _('Color management and color profiles')
	short_title = _('Color Management')
	icon_file = 'prefs-cms.png'

	def __init__(self, app):
		GenericPrefsPlugin.__init__(self, app)

	def build(self):
		GenericPrefsPlugin.build(self)
		self.nb = gtk.Notebook()
		self.tabs = [CMSTab(self.app), RGBTab(self.app), CMYKTab(self.app),
					LabTab(self.app), DisplayTab(self.app)]
		for tab in self.tabs:
			self.nb.append_page(tab, tab.label)
		self.pack_end(self.nb, True, True, 0)


class PrefsTab(gtk.VBox):

	name = 'Tab'
	label = None

	def __init__(self, app):
		gtk.VBox.__init__(self)
		self.app = app
		self.label = gtk.Label(self.name)

class CMSTab(PrefsTab):

	name = _('Color Management')

	def __init__(self, app):
		PrefsTab.__init__(self, app)

class RGBTab(PrefsTab):

	name = _('RGB profiles')

	def __init__(self, app):
		PrefsTab.__init__(self, app)

class CMYKTab(PrefsTab):

	name = _('CMYK profiles')

	def __init__(self, app):
		PrefsTab.__init__(self, app)

class LabTab(PrefsTab):

	name = _('Lab profiles')

	def __init__(self, app):
		PrefsTab.__init__(self, app)

class DisplayTab(PrefsTab):

	name = _('Display profiles')

	def __init__(self, app):
		PrefsTab.__init__(self, app)
