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

from pdesign import events, modes
from pdesign.document.renderer import PDRenderer

class AppCanvas(wx.Panel):

	presenter = None
	app = None
	eventloop = None
	renderer = None

	mode = None
	controller = None
	ctrls = {}
	current_cursor = None

	def __init__(self, presenter, parent):
		self.presenter = presenter
		self.eventloop = self.presenter.eventloop
		self.app = presenter.app
		self.doc = self.presenter.model
		self.renderer = PDRenderer(self)
		wx.Panel.__init__(self, parent)
		self.SetBackgroundColour(wx.Colour(255, 255, 255))
		self.ctrls = self.init_controllers()

	def init_controllers(self):
		dummy = DummyController(self, self.presenter)
		ctrls = {
		modes.SELECT_MODE: dummy,
		modes.SHAPER_MODE: dummy,
		modes.ZOOM_MODE: dummy,
		modes.FLEUR_MODE: dummy,
		modes.TEMP_FLEUR_MODE: dummy,
		modes.PICK_MODE: dummy,
		modes.LINE_MODE: dummy,
		modes.CURVE_MODE: dummy,
		modes.RECT_MODE: dummy,
		modes.ELLIPSE_MODE: dummy,
		modes.TEXT_MODE: dummy,
		modes.POLYGON_MODE: dummy,
		modes.MOVE_MODE: dummy,
		modes.RESIZE_MODE: dummy,
		modes.GUIDE_MODE: dummy,
		}
		return ctrls

	def set_mode(self, mode=modes.SELECT_MODE):
		if not mode == self.mode:
			if not self.controller is None:
				self.controller.stop_()
			self.mode = mode
			self.controller = self.ctrls[mode]
			self.controller.set_cursor()
			self.controller.start_()
			events.emit(events.MODE_CHANGED, mode)

	def set_canvas_cursor(self, mode):
		self.current_cursor = self.app.cursors[mode]
		self.SetCursor(self.current_cursor)

	def on_paint(self, event):pass

	def destroy(self):
		self.presenter = None
		self.app = None
		self.mode = None
		self.controller = None
		self.ctrls = {}
		self.current_cursor = None

class DummyController:

	def __init__(self, canvas, presenter):
		self.canvas = canvas
		self.presenter = presenter

	def stop_(self):pass
	def start_(self):pass

	def set_cursor(self):
		self.canvas.set_canvas_cursor(self.canvas.mode)

