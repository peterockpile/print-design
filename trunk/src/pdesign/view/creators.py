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

from copy import deepcopy

import gtk, gobject

from uc2 import libgeom
from uc2.formats.pdxf import const, model

from pdesign import modes, config

from pdesign.view.controllers import AbstractController, PseudoEvent

RENDERING_DELAY = 50

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
	path = [[], [], const.CURVE_OPENED]
	points = []
	cursor = []
	create = False
	event = None
	obj = None

	def __init__(self, canvas, presenter):
		AbstractCreator.__init__(self, canvas, presenter)

	def start_(self):
		self.create = False
		sel_objs = self.selection.objs
		if len(sel_objs) == 1 and sel_objs[0].cid == model.CURVE:
			if self.obj is None:
				self.obj = sel_objs[0]
				self.update_from_obj()

	def update_from_obj(self):
		self.paths = libgeom.apply_trafo_to_paths(self.obj.paths, self.obj.trafo)
		path = self.paths[-1]
		if path[-1] == const.CURVE_OPENED:
			self.path = path
			self.points = self.path[1]
			paths = self.canvas.paths_doc_to_win(self.paths)
			self.canvas.renderer.paint_curve(paths)
		else:
			self.presenter.selection.clear()
			self.cursor = []
			self.points = []
			self.path = [[], [], const.CURVE_OPENED]
			paths = self.canvas.paths_doc_to_win(self.paths)
			self.canvas.renderer.paint_curve(paths)
			self.paths.append(self.path)
		self.draw = True


	def stop_(self):
		self.draw = False
		self.create = False
		self.cursor = []
		self.paths = []
		self.points = []
		self.path = [[], [], const.CURVE_OPENED]
		if not self.timer is None:
			gobject.source_remove(self.timer)
		self.canvas.renderer.paint_curve([])
		self.canvas.selection_repaint()
		self.obj = None

	def mouse_down(self, event):
		if event.button == LEFT_BUTTON:
			if not self.draw:
				self.presenter.selection.clear()
				self.draw = True
				self.paths = []
				self.points = []
				self.path = [[], [], const.CURVE_OPENED]
				self.paths.append(self.path)
			self.cursor = [event.x, event.y]
			self.create = True
			if not self.timer is None:
				gobject.source_remove(self.timer)
				self.timer = None
		elif event.button == MIDDLE_BUTTON:
			if not self.timer is None:
				gobject.source_remove(self.timer)
				self.timer = None
				self.repaint()
			self.canvas.set_temp_mode(modes.TEMP_FLEUR_MODE)

	def mouse_up(self, event):
		if self.draw:
			x, y = [event.x, event.y]
			self.create = False
			if self.path[0]:
				w0 = h0 = config.line_sensitivity_size
				x0, y0 = self.canvas.doc_to_win(self.path[0])
				if self.points:
					w = h = config.line_sensitivity_size
					if len(self.points[-1]) == 2:
						x1, y1 = self.canvas.doc_to_win(self.points[-1])
					else:
						x1, y1 = self.canvas.doc_to_win(self.points[-1][2])
					if libgeom.is_point_in_rect2([x, y], [x0, y0], w0, h0) and len(self.points) > 1:
						self.path[2] = const.CURVE_CLOSED
						self.points.append([] + self.path[0])
						if not event.state & gtk.gdk.CONTROL_MASK:
							self.mouse_double_click()
						else:
							self.repaint()
							self.points = []
							self.path = [[], [], const.CURVE_OPENED]
							self.paths.append(self.path)
					elif not libgeom.is_point_in_rect2([x, y], [x1, y1], w, h):
						self.points.append(self.canvas.win_to_doc([x, y]))
						self.path[1] = self.points
				else:
					if not libgeom.is_point_in_rect2([x, y], [x0, y0], w0, h0):
						self.points.append(self.canvas.win_to_doc([x, y]))
						self.path[1] = self.points
			else:
				self.path[0] = self.canvas.win_to_doc([event.x, event.y])
			self.repaint()

	def repaint(self, cursor=[]):
		if self.path[0]:
			paths = self.canvas.paths_doc_to_win(self.paths)
			self.canvas.renderer.paint_curve(paths, cursor)

	def mouse_double_click(self, event=None):
		if not event is None and event.state & gtk.gdk.CONTROL_MASK:
				if config.line_autoclose_flag:
					self.path[2] = const.CURVE_CLOSED
					self.points.append([] + self.path[0])
				self.points = []
				self.path = [[], [], const.CURVE_OPENED]
				self.paths.append(self.path)
				return
		if self.draw and self.paths and self.points:
			if config.line_autoclose_flag:
				self.path[2] = const.CURVE_CLOSED
				self.points.append([] + self.path[0])
			paths = self.paths
			obj = self.obj
			self.stop_()
			if obj is None:
				self.api.create_curve(paths)
			else:
				self.api.update_curve(obj, paths)

	def mouse_move(self, event):
		if self.draw:
			if self.create:
				if self.event is None:
					self.event = PseudoEvent()
					self.event.x = self.cursor[0]
					self.event.y = self.cursor[1]
					self.mouse_up(self.event)
					self.create = True
				self.event.x = event.x
				self.event.y = event.y
				if self.timer is None:
					self.timer = gobject.timeout_add(RENDERING_DELAY, self._create)
			else:
				self.cursor = [event.x, event.y]
				if self.timer is None:
					self.timer = gobject.timeout_add(RENDERING_DELAY, self._repaint)
		else:
			if not self.timer is None:
				gobject.source_remove(self.timer)
				self.timer = None
			self.counter += 1
			if self.counter > 5:
				self.counter = 0
				point = [event.x, event.y]
				dpoint = self.canvas.win_to_doc(point)
				if self.selection.is_point_over_marker(dpoint):
					mark = self.selection.is_point_over_marker(dpoint)[0]
					self.canvas.resize_marker = mark
					self.canvas.set_temp_mode(modes.RESIZE_MODE)


	def _repaint(self):
		if self.path[0] and self.cursor:
			paths = self.canvas.paths_doc_to_win(self.paths)
			self.canvas.renderer.paint_curve(paths, self.cursor)
		return True

	def _create(self):
		if not self.event is None:
			if self.create and self.cursor:
				x, y = [self.event.x, self.event.y]
				x0, y0 = self.cursor
				if abs(x - x0) > 2 or abs(y - y0) > 2:
					self.mouse_up(self.event)
					self.create = True
					self.cursor = [x, y]
			else:
				if not self.timer is None:
					gobject.source_remove(self.timer)
					self.timer = None
					self.event = None
		return True

class PathsCreator(PolyLineCreator):

	mode = modes.CURVE_MODE

	def __init__(self, canvas, presenter):
		PolyLineCreator.__init__(self, canvas, presenter)

	def mouse_up(self, event):
		if self.draw:
			x, y = [event.x, event.y]
			self.create = False
			if self.path[0]:
				w0 = h0 = config.line_sensitivity_size
				x0, y0 = self.canvas.doc_to_win(self.path[0])
				if self.points:
					w = h = config.line_sensitivity_size
					if len(self.points[-1]) == 2:
						x1, y1 = self.canvas.doc_to_win(self.points[-1])
					else:
						x1, y1 = self.canvas.doc_to_win(self.points[-1][2])
					if libgeom.is_point_in_rect2([x, y], [x0, y0], w0, h0) and len(self.points) > 1:
						self.path[2] = const.CURVE_CLOSED
						if len(self.points[-1]) == 2:
							p0 = [] + self.points[-1]
						else:
							p0 = [] + self.points[-1][2]
						p1 = [] + self.path[0]
						p2 = [] + p1
						self.points.append([p0, p1, p2, const.NODE_CUSP])
						if not event.state & gtk.gdk.CONTROL_MASK:
							self.mouse_double_click()
						else:
							self.repaint()
							self.points = []
							self.path = [[], [], const.CURVE_OPENED]
							self.paths.append(self.path)
					elif not libgeom.is_point_in_rect2([x, y], [x1, y1], w, h):
						if len(self.points[-1]) == 2:
							p0 = [] + self.points[-1]
						else:
							p0 = [] + self.points[-1][2]
						p1 = self.canvas.win_to_doc([x, y])
						p2 = [] + p1
						self.points.append([p0, p1, p2, const.NODE_CUSP])
						self.path[1] = self.points
				else:
					if not libgeom.is_point_in_rect2([x, y], [x0, y0], w0, h0):
						p0 = [] + self.path[0]
						p1 = self.canvas.win_to_doc([x, y])
						p2 = [] + p1
						self.points.append([p0, p1, p2, const.NODE_CUSP])
						self.path[1] = self.points
			else:
				self.path[0] = self.canvas.win_to_doc([event.x, event.y])
			self.repaint()

	def mouse_double_click(self, event=None):
		if not event is None and event.state & gtk.gdk.CONTROL_MASK:
				if config.line_autoclose_flag:
					self.path[2] = const.CURVE_CLOSED
					p0 = [] + self.points[-1]
					p1 = [] + self.path[0]
					p2 = [] + p1
					self.points.append([p0, p1, p2, const.NODE_CUSP])
				self.points = []
				self.path = [[], [], const.CURVE_OPENED]
				self.paths.append(self.path)
				return
		if self.draw and self.paths and self.points:
			if config.line_autoclose_flag:
				self.path[2] = const.CURVE_CLOSED
				self.points.append([] + self.path[0])
			paths = self.paths
			obj = self.obj
			self.stop_()
			if obj is None:
				self.api.create_curve(paths)
			else:
				self.api.update_curve(obj, paths)

	def mouse_move(self, event):
		if self.draw:
			if self.create:
				pass
#				if self.event is None:
#					self.event = PseudoEvent()
#					self.event.x = self.cursor[0]
#					self.event.y = self.cursor[1]
#					self.mouse_up(self.event)
#					self.create = True
#				self.event.x = event.x
#				self.event.y = event.y
#				if self.timer is None:
#					self.timer = gobject.timeout_add(RENDERING_DELAY, self._create)
			else:
				self.cursor = [event.x, event.y]
				if self.timer is None:
					self.timer = gobject.timeout_add(RENDERING_DELAY, self._repaint)
		else:
			if not self.timer is None:
				gobject.source_remove(self.timer)
				self.timer = None
			self.counter += 1
			if self.counter > 5:
				self.counter = 0
				point = [event.x, event.y]
				dpoint = self.canvas.win_to_doc(point)
				if self.selection.is_point_over_marker(dpoint):
					mark = self.selection.is_point_over_marker(dpoint)[0]
					self.canvas.resize_marker = mark
					self.canvas.set_temp_mode(modes.RESIZE_MODE)



