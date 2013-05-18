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

import os
import gtk

from uc2.uc2const import COLOR_RGB, COLOR_CMYK, COLOR_LAB, COLOR_GRAY, COLOR_DISPLAY

from pdesign import _, config
from pdesign.widgets import SimpleListCombo, ImageStockButton
from pdesign.prefs.generic import GenericPrefsPlugin
from pdesign.prefs.profilemngr import get_profiles_dialog

COLORSPACES = [COLOR_RGB, COLOR_CMYK, COLOR_LAB, COLOR_GRAY, COLOR_DISPLAY]

class CmsPrefsPlugin(GenericPrefsPlugin):

	name = 'CmsPrefsPlugin'
	title = _('Color management and color profiles')
	short_title = _('Color Management')
	icon_file = 'prefs-cms.png'

	def __init__(self, app, dlg, pdxf_config):
		GenericPrefsPlugin.__init__(self, app, dlg, pdxf_config)

	def build(self):
		GenericPrefsPlugin.build(self)
		self.nb = gtk.Notebook()
		self.tabs = [ProfilesTab(self.app, self.dlg, self.pdxf_config),
					CMSTab(self.app, self.dlg, self.pdxf_config)]
		for tab in self.tabs:
			self.nb.append_page(tab, tab.label)
		self.pack_end(self.nb, True, True, 0)


class PrefsTab(gtk.VBox):

	name = 'Tab'
	label = None

	def __init__(self, app, dlg, pdxf_config):
		gtk.VBox.__init__(self)
		self.app = app
		self.dlg = dlg
		self.label = gtk.Label(self.name)
		self.pdxf_config = pdxf_config
		self.set_border_width(10)


class CMSTab(PrefsTab):

	name = _('Color Management')

	def __init__(self, app, dlg, pdxf_config):
		PrefsTab.__init__(self, app, dlg, pdxf_config)

class ProfilesTab(PrefsTab):

	name = _('Color profiles')

	def __init__(self, app, dlg, pdxf_config):
		PrefsTab.__init__(self, app, dlg, pdxf_config)

		title = gtk.Label()
		text = _('Document related profiles')
		title.set_markup('<b>%s</b>' % (text))
		self.pack_start(title, False, False, 0)
		self.pack_start(gtk.HSeparator(), False, False, 5)

		tab = gtk.Table(9, 3, False)
		tab.set_row_spacings(5)
		tab.set_col_spacings(10)
		self.pack_start(tab, True, True, 0)
		self.cs_widgets = {}
		self.cs_profiles = {}
		self.cs_config_profiles = {}

		self.cs_config = {COLOR_RGB:self.pdxf_config.default_rgb_profile,
					COLOR_CMYK:self.pdxf_config.default_cmyk_profile,
					COLOR_LAB:self.pdxf_config.default_lab_profile,
					COLOR_GRAY:self.pdxf_config.default_gray_profile,
					COLOR_DISPLAY:config.cms_display_profile}

		index = 0
		for colorspace in COLORSPACES[:-1]:
			label = gtk.Label(_('%s profile:') % (colorspace))
			label.set_alignment(0, 0.5)
			tab.attach(label, 0, 1, index, index + 1, gtk.FILL, gtk.SHRINK)

			combo = SimpleListCombo()
			self.cs_widgets[colorspace] = combo
			tab.attach(combo, 1, 2, index, index + 1, gtk.FILL | gtk.EXPAND, gtk.SHRINK)
			self.update_combo(colorspace)

			button = ManageButton(self, colorspace)
			tab.attach(button, 2, 3, index, index + 1, gtk.SHRINK, gtk.SHRINK)

			index += 1

		note = gtk.Label()
		text = _('<span size="small"><b>Note:</b> The profiles are used for'
				' newly created document and will be embedded into the '
				'document (except built-in profiles).</span>')
		note.set_markup(text)
		note.set_line_wrap(True)
		note.set_alignment(0, 1)
		note.set_sensitive(False)
		note.set_size_request(450, -1)
		note.set_justify(gtk.JUSTIFY_FILL)
		hbox = gtk.HBox()
		hbox.pack_start(note, True, True, 0)
		tab.attach(hbox, 0, 3, 4, 5, gtk.FILL | gtk.EXPAND, gtk.SHRINK)

		title = gtk.Label()
		text = _('Application related profile')
		title.set_markup('<b>%s</b>' % (text))
		tab.attach(title, 0, 3, 5, 6, gtk.FILL, gtk.SHRINK)
		line = gtk.HSeparator()
		tab.attach(line, 0, 3, 6, 7, gtk.FILL, gtk.SHRINK)

		colorspace = COLOR_DISPLAY
		label = gtk.Label(_('%s profile:') % (colorspace))
		label.set_alignment(0, 0.5)
		tab.attach(label, 0, 1, 7, 8, gtk.FILL, gtk.SHRINK)

		combo = SimpleListCombo()
		self.cs_widgets[colorspace] = combo
		tab.attach(combo, 1, 2, 7, 8, gtk.FILL | gtk.EXPAND, gtk.SHRINK)
		self.update_combo(colorspace)

		button = ManageButton(self, colorspace)
		tab.attach(button, 2, 3, 7, 8, gtk.SHRINK, gtk.SHRINK)

		note = gtk.Label()
		text = _('<span size="small"><b>Note:</b> Display profile affects on '
				'document screen representation only. Therefore it is not '
				'embedded into document.</span>')
		note.set_markup(text)
		note.set_line_wrap(True)
		note.set_alignment(0, 1)
		note.set_sensitive(False)
		note.set_size_request(450, -1)
		tab.attach(note, 0, 3, 8, 9, gtk.FILL | gtk.EXPAND, gtk.SHRINK)

	def update_config_data(self, colorspace):
		if colorspace == COLOR_RGB:
			self.cs_config_profiles[colorspace] = config.cms_rgb_profiles.copy()
		elif colorspace == COLOR_CMYK:
			self.cs_config_profiles[colorspace] = config.cms_cmyk_profiles.copy()
		elif colorspace == COLOR_LAB:
			self.cs_config_profiles[colorspace] = config.cms_lab_profiles.copy()
		elif colorspace == COLOR_GRAY:
			self.cs_config_profiles[colorspace] = config.cms_gray_profiles.copy()
		else:
			self.cs_config_profiles[colorspace] = config.cms_display_profiles.copy()
		self.cs_profiles[colorspace] = self.get_profile_names(colorspace)


	def update_combo(self, colorspace, set_active=True):
		self.update_config_data(colorspace)
		combo = self.cs_widgets[colorspace]
		combo.clear()
		for name in self.cs_profiles[colorspace]: combo.append_text(name)
		if not set_active: return
		self.set_active_profile(combo, self.cs_config[colorspace], colorspace)

	def set_active_profile(self, widget, name, colorspace):
		profiles = self.get_profile_names(colorspace)
		if not name or not name in profiles:
			widget.set_active(0)
			if colorspace == COLOR_RGB:
				self.pdxf_config.default_rgb_profile = ''
			elif colorspace == COLOR_CMYK:
				self.pdxf_config.default_cmyk_profile = ''
			elif colorspace == COLOR_LAB:
				self.pdxf_config.default_lab_profile = ''
			elif colorspace == COLOR_GRAY:
				self.pdxf_config.default_gray_profile = ''
			else:
				config.display_profile = ''
			self.pdxf_config.save()
		else:
			widget.set_active(profiles.index(name))

	def get_profile_names(self, colorspace):
		names = []
		default = _('Built-in %s profile') % (colorspace)
		names.append(default)
		names += self.cs_config_profiles[colorspace].keys()
		return names

class ManageButton(ImageStockButton):

	colorspace = ''
	owner = None

	def __init__(self, owner, colorspace):
		self.owner = owner
		self.colorspace = colorspace
		text = _('Add/remove %s profiles') % (colorspace)
		ImageStockButton.__init__(self, text, gtk.STOCK_EDIT, False)
		self.connect('clicked', self.action)

	def action(self, *args):
		get_profiles_dialog(self.owner.app, self.owner.dlg,
						self.owner, self.colorspace)
