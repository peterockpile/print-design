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

from pdesign import events
from pdesign.widgets import const, ALL, EXPAND, HPanel
from pdesign.context import PLUGINS, NO_DOC, DEFAULT, MULTIPLE, GROUP, \
RECTANGLE, CIRCLE, POLYGON, CURVE, TEXT, PIXMAP

class AppCtxPanel(HPanel):

	app = None

	plugins_dict = {}
	plugins = []

	def __init__(self, app, parent):
		self.app = app
		self.insp = app.insp
		HPanel.__init__(self, parent)
		spacer = (5, 30)
		self.add(spacer)

		for item in PLUGINS:
			plg = item(self.app, self)
			self.plugins_dict[plg.name] = plg

		events.connect(events.NO_DOCS, self.rebuild)
		events.connect(events.DOC_CHANGED, self.rebuild)
		events.connect(events.SELECTION_CHANGED, self.rebuild)
		self.rebuild()

	def rebuild(self, *args):
		for item in self.plugins:
			item.hide()
			self.remove(item)
		self.plugins = []
		mode = self.get_mode()
		if mode:
			for item in mode:
				self.add(self.plugins_dict[item], 0, ALL | EXPAND)
				self.plugins_dict[item].show()
				self.plugins.append(self.plugins_dict[item])
		self.Layout()

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
			elif self.insp.is_obj_circle(sel[0]):
				return CIRCLE
			elif self.insp.is_obj_polygon(sel[0]):
				return POLYGON
			elif self.insp.is_obj_curve(sel[0]):
				return CURVE
			elif self.insp.can_be_ungrouped():
				return GROUP
			else:
				return DEFAULT
