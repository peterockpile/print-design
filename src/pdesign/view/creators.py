# -*- coding: utf-8 -*-
#
#	Copyright (C) 2011-2012 by Igor E. Novikov 
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

from uc2.formats.pdxf import const

from pdesign import modes

from pdesign.view.controllers import AbstractController

LEFT_BUTTON = 1
MIDDLE_BUTTON = 2
RIGHT_BUTTON = 3

class AbstractCreator(AbstractController):

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)

	def mouse_move(self, event):
		if self.draw:
			AbstractController.mouse_move(self, event)
		else:
			self.counter += 1
			if self.counter > 5:
				self.counter = 0
				point = [event.x, event.y]
				dpoint = self.canvas.win_to_doc(point)
				if self.selection.is_point_over_marker(dpoint):
					mark = self.selection.is_point_over_marker(dpoint)[0]
					self.canvas.resize_marker = mark
					self.canvas.set_temp_mode(modes.RESIZE_MODE)

class RectangleCreator(AbstractCreator):

	mode = modes.RECT_MODE

	def __init__(self, canvas, presenter):
		AbstractCreator.__init__(self, canvas, presenter)

	def do_action(self, event):
		if self.start and self.end:
			if abs(self.end[0] - self.start[0]) > 2 and \
			abs(self.end[1] - self.start[1]) > 2:
				rect = self.start + self.end
				self.api.create_rectangle(rect)

class EllipseCreator(AbstractCreator):

	mode = modes.ELLIPSE_MODE

	def __init__(self, canvas, presenter):
		AbstractCreator.__init__(self, canvas, presenter)

	def do_action(self, event):
		if self.start and self.end:
			if abs(self.end[0] - self.start[0]) > 2 and \
			abs(self.end[1] - self.start[1]) > 2:
				rect = self.start + self.end
				self.api.create_ellipse(rect)

class PolygonCreator(AbstractCreator):

	mode = modes.POLYGON_MODE

	def __init__(self, canvas, presenter):
		AbstractCreator.__init__(self, canvas, presenter)

	def do_action(self, event):
		if self.start and self.end:
			if abs(self.end[0] - self.start[0]) > 2 and \
			abs(self.end[1] - self.start[1]) > 2:
				rect = self.start + self.end
				self.api.create_polygon(rect)

class TextBlockCreator(AbstractCreator):

	mode = modes.TEXT_MODE

	def __init__(self, canvas, presenter):
		AbstractCreator.__init__(self, canvas, presenter)

	def do_action(self, event):
		if self.start and self.end:
			if abs(self.end[0] - self.start[0]) > 2 and \
			abs(self.end[1] - self.start[1]) > 2:
				rect = self.start + self.end
				self.api.create_text(rect)
			else:
				rect = self.start + self.start
				self.api.create_text(rect, width=const.TEXTBLOCK_WIDTH)

class PolyLineCreator(AbstractCreator):

	mode = modes.LINE_MODE
	paths = []
	path = [[], [], []]
	points = []

	def __init__(self, canvas, presenter):
		AbstractCreator.__init__(self, canvas, presenter)

	def stop(self):
		self.draw = False
		self.paths = []
		self.points = []
		self.path = [[], [], []]
		self.canvas.renderer.paint_polyline([])
		self.canvas.selection_repaint()

	def mouse_down(self, event):
		if event.button == LEFT_BUTTON:
			if not self.draw:
				self.presenter.selection.clear()
				self.draw = True
				self.paths = []
				self.points = []
				self.path = [[], [], []]
				self.paths.append(self.path)
		elif event.button == MIDDLE_BUTTON:
			self.canvas.set_temp_mode(modes.TEMP_FLEUR_MODE)

	def mouse_up(self, event):
		if self.draw:
			if self.path[0]:
				self.points.append(self.canvas.win_to_doc([event.x, event.y]))
				self.path[1] = self.points
			else:
				self.path[0] = self.canvas.win_to_doc([event.x, event.y])
			self.repaint()

	def repaint(self):
		if self.path[0]:
			paths = self.canvas.paths_doc_to_win(self.paths)
			self.canvas.renderer.paint_polyline(paths)

	def mouse_double_click(self, event):
		paths = self.paths
		self.stop()
		self.api.create_curve(paths)

	def mouse_move(self, event):pass

