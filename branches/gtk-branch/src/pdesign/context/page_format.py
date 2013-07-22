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

from uc2.uc2const import PAGE_FORMATS, PAGE_FORMAT_NAMES, PORTRAIT, LANDSCAPE

from pdesign import _, config, events
from pdesign.widgets import UnitSpin, ImageToggleButton, SimpleListCombo

class PageFormatPlugin(gtk.HBox):

	name = 'PageFormatPlugin'
	my_changes = False
	update_flag = False
	format = []

	def __init__(self, mw):
		gtk.HBox.__init__(self)
		self.mw = mw
		self.app = mw.app
		self.insp = self.app.inspector
		self.actions = self.app.actions
		self.sep = gtk.VSeparator()
		self.pack_end(self.sep, False, False, 2)
		self.build()

	def build(self):
		label = gtk.Label(_('Page:'))
		self.pack_start(label, False, False, 0)

		self.formats = PAGE_FORMAT_NAMES + [_('Custom'), ]

		self.combo = SimpleListCombo(self.formats)
		self.pack_start(self.combo.vbox, False, False, 2)

		self.width_spin = UnitSpin(self.width_spin_changed)
		self.pack_start(self.width_spin, False, False, 2)

		label = gtk.Label('x')
		self.pack_start(label, False, False, 0)

		self.height_spin = UnitSpin(self.height_spin_changed)
		self.pack_start(self.height_spin, False, False, 2)

		self.portrait = ImageToggleButton(_('Portrait'),
										['icons', 'page-portrait.png'])
		self.pack_start(self.portrait, False, False, 0)

		self.landscape = ImageToggleButton(_('Landscape'),
										['icons', 'page-landscape.png'])
		self.pack_start(self.landscape, False, False, 0)

		self.combo.connect('changed', self.combo_changed)
		self.portrait.connect("toggled", self.portrait_toggled)
		self.landscape.connect("toggled", self.landscape_toggled)
		events.connect(events.DOC_CHANGED, self.update)
		events.connect(events.DOC_MODIFIED, self.update)

	def combo_changed(self, *args):
		if self.update_flag: return
		if not self.format[0] == self.formats[self.combo.get_active()]:
			self.update_flag = True
			if not self.formats[self.combo.get_active()] == self.formats[-1]:
				format = self.formats[self.combo.get_active()]
				w, h = PAGE_FORMATS[format]
				if self.portrait.get_active() and w > h:
					self.width_spin.set_point_value(w)
					self.height_spin.set_point_value(h)
					self.portrait.set_active(False)
					self.landscape.set_active(True)
				elif self.landscape.get_active() and w > h:
					self.width_spin.set_point_value(w)
					self.height_spin.set_point_value(h)
				elif self.portrait.get_active() and w < h:
					self.width_spin.set_point_value(w)
					self.height_spin.set_point_value(h)
				else:
					self.width_spin.set_point_value(h)
					self.height_spin.set_point_value(w)
			self.update_flag = False
			self.changes()

	def width_spin_changed(self, *args):
		if self.update_flag: return
		if not self.format[1][0] == self.width_spin.get_point_value():
			self.update_flag = True
			w = self.width_spin.get_point_value()
			h = self.height_spin.get_point_value()
			if w > h and self.portrait.get_active():
				self.portrait.set_active(False)
				self.landscape.set_active(True)
			elif w < h and self.landscape.get_active():
				self.portrait.set_active(True)
				self.landscape.set_active(False)
			self.update_flag = False
			self.changes()

	def height_spin_changed(self, *args):
		if self.update_flag: return
		if not self.format[1][1] == self.height_spin.get_point_value():
			self.update_flag = True
			w = self.width_spin.get_point_value()
			h = self.height_spin.get_point_value()
			if w > h and self.portrait.get_active():
				self.portrait.set_active(False)
				self.landscape.set_active(True)
			elif w < h and self.landscape.get_active():
				self.portrait.set_active(True)
				self.landscape.set_active(False)
			self.update_flag = False
			self.changes()

	def portrait_toggled(self, *args):
		if self.update_flag: return
		if self.portrait.get_active():
			self.update_flag = True
			self.landscape.set_active(False)
			h = self.width_spin.get_point_value()
			w = self.height_spin.get_point_value()
			self.width_spin.set_point_value(w)
			self.height_spin.set_point_value(h)
			self.update_flag = False
			self.changes()

	def landscape_toggled(self, *args):
		if self.update_flag: return
		if self.landscape.get_active():
			self.update_flag = True
			self.portrait.set_active(False)
			h = self.width_spin.get_point_value()
			w = self.height_spin.get_point_value()
			self.width_spin.set_point_value(w)
			self.height_spin.set_point_value(h)
			self.update_flag = False
			self.changes()

	def changes(self):
		new_format = [self.formats[self.combo.get_active()], ]
		new_format += [(self.width_spin.get_point_value(),
					self.height_spin.get_point_value())]
		if self.portrait.get_active():
			new_format += [PORTRAIT, ]
		else:
			new_format += [LANDSCAPE, ]
		self.app.current_doc.api.set_page_format(new_format)

	def update(self, *args):
		if self.insp.is_doc():
			self.update_flag = True
			page_format = self.app.current_doc.active_page.page_format
			self.format = page_format
			width, height = page_format[1]
			if page_format[0] in PAGE_FORMAT_NAMES:
				self.combo.set_active(self.formats.index(page_format[0]))
				if page_format[2] == PORTRAIT:
					self.portrait.set_active(True)
					self.landscape.set_active(False)
				else:
					self.portrait.set_active(False)
					self.landscape.set_active(True)
				self.width_spin.set_point_value(width)
				self.height_spin.set_point_value(height)
				self.width_spin.set_sensitive(False)
				self.height_spin.set_sensitive(False)
			else:
				self.combo.set_active(self.formats.index(_('Custom')))
				if page_format[2] == PORTRAIT:
					self.portrait.set_active(True)
					self.landscape.set_active(False)
				else:
					self.portrait.set_active(False)
					self.landscape.set_active(True)
				self.width_spin.set_point_value(width)
				self.height_spin.set_point_value(height)
				self.width_spin.set_sensitive(True)
				self.height_spin.set_sensitive(True)
			self.update_flag = False



