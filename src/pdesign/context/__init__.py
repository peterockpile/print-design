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

import os, gtk

from pdesign import _, config, events
from pdesign.context.transform import GroupPlugin, MirrorPlugin, RotatePlugin, \
									ResizePlugin
from pdesign.context.units import UnitsPlugin
from pdesign.context.page_format import PageFormatPlugin

PLUGINS = [UnitsPlugin, GroupPlugin, MirrorPlugin, RotatePlugin, ResizePlugin,
		PageFormatPlugin, ]

NO_DOC = []
DEFAULT = ['PageFormatPlugin', 'UnitsPlugin', ]
MULTIPLE = ['ResizePlugin', 'GroupPlugin', 'RotatePlugin', 'MirrorPlugin']
GROUP = ['ResizePlugin', 'GroupPlugin', 'RotatePlugin', 'MirrorPlugin']
RECTANGLE = ['ResizePlugin', 'RotatePlugin', 'MirrorPlugin']
CURVE = ['ResizePlugin', 'RotatePlugin', 'MirrorPlugin']

class ContextPanel(gtk.HBox):

	plugins_dict = {}
	plugins = []

	def __init__(self, mw):
		gtk.HBox.__init__(self)

		self.mw = mw
		self.app = mw.app
		self.insp = self.app.inspector

		self.set_border_width(2)
		self.holder = PanelHolder()
		self.pack_start(self.holder, False, False, 0)

		for item in PLUGINS:
			plg = item(self.mw)
			self.plugins_dict[plg.name] = plg

		events.connect(events.NO_DOCS, self.rebuild)
		events.connect(events.DOC_CHANGED, self.rebuild)
		events.connect(events.SELECTION_CHANGED, self.rebuild)
		self.rebuild()

	def rebuild(self, *args):
		for item in self.plugins:
			self.remove(item)
		self.plugins = []
		mode = self.get_mode()
		if mode:
			for item in mode:
				self.pack_start(self.plugins_dict[item], False, False, 0)
				self.plugins.append(self.plugins_dict[item])
				self.plugins_dict[item].show_all()

	def get_mode(self):
		if not self.insp.is_doc():
			return NO_DOC
		if not self.insp.is_selection():
			return DEFAULT
		else:
			doc = self.app.current_doc
			sel = doc.selection.objs
			if len(sel) > 1:
				return MULTIPLE
			elif self.insp.is_obj_rect(sel[0]):
				return RECTANGLE
			elif self.insp.can_be_ungrouped():
				return GROUP
			elif self.insp.is_obj_curve(sel[0]):
				return CURVE
			else:
				return DEFAULT


class PanelHolder(gtk.Image):
	def __init__(self):
		gtk.Image.__init__(self)
		image_file = os.path.join(config.resource_dir, 'icons', 'panel-holder.png')
		self.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file(image_file))



