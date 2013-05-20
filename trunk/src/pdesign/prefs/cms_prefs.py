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

import copy
import gtk

from uc2.uc2const import COLOR_RGB, COLOR_CMYK, COLOR_LAB, COLOR_GRAY, COLOR_DISPLAY
from uc2.cms import rgb_to_hexcolor, gdk_hexcolor_to_rgb

from pdesign import _, config
from pdesign.widgets import SimpleListCombo, ImageStockButton
from pdesign.prefs.generic import GenericPrefsPlugin
from pdesign.prefs.profilemngr import get_profiles_dialog
from uc2 import uc2const

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

	def apply_changes(self):
		for tab in self.tabs:
			tab.apply_changes()

	def restore_defaults(self):
		index = self.nb.get_current_page()
		self.tabs[index].restore_defaults()


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

	def apply_changes(self):pass
	def restore_defaults(self):pass


class CMSTab(PrefsTab):

	name = _('Color Management')
	build = True

	rgb_intent = uc2const.INTENT_RELATIVE_COLORIMETRIC
	cmyk_intent = uc2const.INTENT_PERCEPTUAL
	proof_flag = False
	gamutcheck_flag = False
	alarmcodes = []
	spot_flag = False
	bpc_flag = False
	bpt_flag = False

	def __init__(self, app, dlg, pdxf_config):
		PrefsTab.__init__(self, app, dlg, pdxf_config)

		self.get_config_vals()

		#Rendering intents frame
		self.intents = uc2const.INTENTS.keys()
		self.intents.sort()
		self.intents_names = []
		for item in self.intents:
			self.intents_names.append(uc2const.INTENTS[item])

		intent_frame = gtk.Frame(' ' + _('Rendering intents') + ' ')
		tab = gtk.Table(2, 2, False)
		tab.set_row_spacings(5)
		tab.set_col_spacings(10)
		tab.set_border_width(5)

		label = gtk.Label(_('Display/RGB intent:'))
		tab.attach(label, 0, 1, 0, 1, gtk.SHRINK, gtk.SHRINK)
		self.rgb_intent_combo = SimpleListCombo(self.intents_names)
		self.rgb_intent_combo.set_active(config.cms_rgb_intent)
		self.rgb_intent_combo.connect('changed', self.update_vals)
		tab.attach(self.rgb_intent_combo, 1, 2, 0, 1, gtk.SHRINK, gtk.SHRINK)

		label = gtk.Label(_('Printer/CMYK intent:'))
		tab.attach(label, 0, 1, 1, 2, gtk.SHRINK, gtk.SHRINK)
		self.cmyk_intent_combo = SimpleListCombo(self.intents_names)
		self.cmyk_intent_combo.set_active(config.cms_cmyk_intent)
		self.cmyk_intent_combo.connect('changed', self.update_vals)
		tab.attach(self.cmyk_intent_combo, 1, 2, 1, 2, gtk.SHRINK, gtk.SHRINK)

		intent_frame.add(tab)
		self.pack_start(intent_frame, False, True, 0)

		#Printer simulation
		printer_frame = gtk.Frame()
		self.printer_check = gtk.CheckButton(_('Simulate Printer on the Screen'))
		self.printer_check.set_active(True)
		self.printer_check.connect('toggled', self.update_vals)
		printer_frame.set_label_widget(self.printer_check)

		vbox = gtk.VBox()
		vbox.set_border_width(10)
		printer_frame.add(vbox)
		txt = _('Show colors that are out of the printer gamut')
		self.gamut_check = gtk.CheckButton(txt)
		self.gamut_check.connect('toggled', self.update_vals)
		vbox.pack_start(self.gamut_check, True, True, 0)

		hbox = gtk.HBox()
		self.alarm_label = gtk.Label('Alarm color:')
		hbox.pack_start(self.alarm_label, False, False, 5)

		self.cb = gtk.ColorButton()
		self.cb.connect('color-set', self.update_vals)
		self.cb.set_size_request(100, -1)
		self.cb.set_title(_('Select alarm color'))
		self.cb.set_color(gtk.gdk.Color(rgb_to_hexcolor(config.cms_alarmcodes)))
		hbox.pack_start(self.cb, False, False, 5)

		vbox.pack_start(hbox, True, True, 0)

		txt = _('Separation for SPOT colors')
		self.spot_check = gtk.CheckButton(txt)
		self.spot_check.connect('toggled', self.update_vals)
		vbox.pack_start(self.spot_check, False, True, 5)

		self.pack_start(printer_frame, False, True, 0)

		#Flags
		txt = _('Use Blackpoint Compensation')
		self.bpc_check = gtk.CheckButton(txt)
		self.bpc_check.connect('toggled', self.update_vals)
		self.pack_start(self.bpc_check, False, True, 5)

		txt = _('Use Black preserving transforms')
		self.bpt_check = gtk.CheckButton(txt)
		self.bpt_check.connect('toggled', self.update_vals)
		self.pack_start(self.bpt_check, False, True, 0)

		self.update_widgets()

	def get_config_vals(self):
		self.rgb_intent = config.cms_rgb_intent
		self.cmyk_intent = config.cms_cmyk_intent
		self.proof_flag = config.cms_proofing
		self.gamutcheck_flag = config.cms_gamutcheck
		self.alarmcodes = copy.copy(config.cms_alarmcodes)
		self.spot_flag = config.cms_proof_for_spot
		self.bpc_flag = config.cms_bpc_flag
		self.bpt_flag = config.cms_bpt_flag

	def update_widgets(self):
		self.build = True
		self.rgb_intent_combo.set_active(self.rgb_intent)
		self.cmyk_intent_combo.set_active(self.cmyk_intent)
		self.printer_check.set_active(self.proof_flag)
		#---
		self.gamut_check.set_sensitive(self.proof_flag)
		self.alarm_label.set_sensitive(self.proof_flag)
		self.cb.set_sensitive(self.proof_flag)
		self.spot_check.set_sensitive(self.proof_flag)
		#---
		self.gamut_check.set_active(self.gamutcheck_flag)
		if self.proof_flag:
			self.alarm_label.set_sensitive(self.gamutcheck_flag)
			self.cb.set_sensitive(self.gamutcheck_flag)
		self.cb.set_color(gtk.gdk.Color(rgb_to_hexcolor(self.alarmcodes)))
		self.spot_check.set_active(self.spot_flag)
		self.bpc_check.set_active(self.bpc_flag)
		self.bpt_check.set_active(self.bpt_flag)
		self.build = False

	def update_vals(self, *args):
		if not self.build:
			self.rgb_intent = self.rgb_intent_combo.get_active()
			self.cmyk_intent = self.cmyk_intent_combo.get_active()
			self.proof_flag = self.printer_check.get_active()
			self.gamutcheck_flag = self.gamut_check.get_active()
			color = gdk_hexcolor_to_rgb(self.cb.get_color().to_string())
			self.alarmcodes = color
			self.spot_flag = self.spot_check.get_active()
			self.bpc_flag = self.bpc_check.get_active()
			self.bpt_flag = self.bpt_check.get_active()
			self.update_widgets()

	def restore_defaults(self):
		defaults = config.get_defaults()
		self.rgb_intent = defaults['cms_rgb_intent']
		self.cmyk_intent = defaults['cms_cmyk_intent']
		self.proof_flag = defaults['cms_proofing']
		self.gamutcheck_flag = defaults['cms_gamutcheck']
		self.alarmcodes = copy.copy(defaults['cms_alarmcodes'])
		self.spot_flag = defaults['cms_proof_for_spot']
		self.bpc_flag = defaults['cms_bpc_flag']
		self.bpt_flag = defaults['cms_bpt_flag']
		self.update_widgets()

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
				'embedded into document. The profile for your hardware '
				'you can get either from monitor manufacture or '
				'calibrating monitor (prefered option) or download '
				'from ICC Profile Taxi service http://icc.opensuse.org/</span>')
		note.set_markup(text)
		note.set_line_wrap(True)
		note.set_alignment(0, 1)
		note.set_sensitive(False)
		note.set_size_request(430, -1)
		tab.attach(note, 0, 2, 8, 9, gtk.FILL | gtk.EXPAND, gtk.SHRINK)

		button = TaxiButton(self.app)
		tab.attach(button, 2, 3, 8, 9, gtk.SHRINK, gtk.SHRINK)

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
		combo.set_list(self.cs_profiles[colorspace])
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

class TaxiButton(ImageStockButton):

	colorspace = ''
	owner = None

	def __init__(self, app):
		self.app = app
		text = _('Download profile from ICC Profile Taxi')
		ImageStockButton.__init__(self, text, gtk.STOCK_GOTO_BOTTOM, False)
		self.connect('clicked', self.action)

	def action(self, *args):
		self.app.open_url('http://icc.opensuse.org/')

