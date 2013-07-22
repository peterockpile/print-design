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

from pdesign import _, events, config
from pdesign.widgets import UnitLabel, UnitSpin, KeepRatioLabel

class JumpPlugin(gtk.HBox):

	name = 'JumpPlugin'

	def __init__(self, mw):
		gtk.HBox.__init__(self)
		self.mw = mw
		self.app = mw.app
		self.sep = gtk.VSeparator()
		self.pack_end(self.sep, False, False, 2)
		self.build()
		events.connect(events.NO_DOCS, self.set_state)
		events.connect(events.CONFIG_MODIFIED, self.config_changed)

	def build(self):
		ebox = gtk.EventBox()
		label = gtk.Image()
		image_file = os.path.join(config.resource_dir, 'icons', 'object-jump.png')
		label.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(image_file))
		ebox.add(label)
		ebox.set_tooltip_text(_('Default object jump'))
		self.pack_start(ebox, False, False, 2)

		self.jump_spin = UnitSpin(self.user_changes)
		self.pack_start(self.jump_spin, False, False, 0)
		self.jump_spin.set_point_value(config.obj_jump)

		label = UnitLabel()
		self.pack_start(label, False, False, 2)

	def user_changes(self, *args):
		val = self.jump_spin.get_point_value()
		if not config.obj_jump == val:
			config.obj_jump = val

	def config_changed(self, *args):
		if args[0][0] == 'obj_jump':
			val = self.jump_spin.get_point_value()
			if not config.obj_jump == val:
				self.jump_spin.set_point_value(config.obj_jump)


