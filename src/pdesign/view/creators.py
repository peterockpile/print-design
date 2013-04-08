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

import gtk, gobject

from uc2.libgeom import contra_point, bezier_base_point, apply_trafo_to_paths, \
						is_point_in_rect2
from uc2.formats.pdxf import const, model

from pdesign import modes, config

from pdesign.view.controllers import AbstractController

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

	#drawing data
	paths = []
	path = [[], [], const.CURVE_OPENED]
	points = []
	cursor = []
	obj = None

	#Actual event point
	point = []
	ctrl_mask = False
	alt_mask = False

	#Drawing timer to avoid repainting overhead
	timer = None

	#Flags
	draw = False #entering into drawing mode
	create = False #entering into continuous drawing mode

	def __init__(self, canvas, presenter):
		AbstractCreator.__init__(self, canvas, presenter)

	def start_(self):
		self.init_flags()
		self.init_data()
		self.init_timer()
		sel_objs = self.selection.objs
		if len(sel_objs) == 1 and sel_objs[0].cid == model.CURVE:
			if self.obj is None:
				self.obj = sel_objs[0]
				self.update_from_obj()
		self.presenter.selection.clear()
		self.repaint()

	def stop_(self):
		self.init_flags()
		self.init_data()
		self.init_timer()
		self.canvas.renderer.paint_curve([])
		self.canvas.selection_repaint()

	def standby(self):
		self.init_timer()
		self.cursor = []
		self.repaint()

	def restore(self):
		self.repaint()

	def mouse_down(self, event):
		if event.button == LEFT_BUTTON:
			if not self.draw:
				self.draw = True
				self.clear_data()
			self.point = [event.x, event.y]
			self.create = True
			self.init_timer()
		elif event.button == MIDDLE_BUTTON:
			self.canvas.set_temp_mode(modes.TEMP_FLEUR_MODE)

	def mouse_up(self, event):
		if event.button == LEFT_BUTTON and self.draw:
			self.create = False
			self.ctrl_mask = False
			self.alt_mask = False
			if event.state & gtk.gdk.CONTROL_MASK: self.ctrl_mask = True
			if event.state & gtk.gdk.MOD1_MASK : self.alt_mask = True
			self.add_point([event.x, event.y])
			self.repaint()

	def mouse_double_click(self, event):
		if self.ctrl_mask:
			self.draw = False
		else:
			self.release_curve()

	def mouse_move(self, event):
		if self.draw:
			if self.create:
				if self.point:
					self.add_point(self.point)
					self.point = []
				self.cursor = [event.x, event.y]
				self.set_drawing_timer()
			else:
				self.cursor = [event.x, event.y]
				self.set_repaint_timer()
		else:
			self.init_timer()
			self.counter += 1
			if self.counter > 5:
				self.counter = 0
				point = [event.x, event.y]
				dpoint = self.canvas.win_to_doc(point)
				if self.selection.is_point_over_marker(dpoint):
					mark = self.selection.is_point_over_marker(dpoint)[0]
					self.canvas.resize_marker = mark
					self.cursor = []
					self.canvas.set_temp_mode(modes.RESIZE_MODE)

	def repaint(self):
		if self.path[0] or self.paths:
			paths = self.canvas.paths_doc_to_win(self.paths)
			cursor = self.cursor
			if not self.path[0]: cursor = []
			self.canvas.renderer.paint_curve(paths, cursor)
		return True

	def continuous_draw(self):
		if self.create and self.cursor:
			self.add_point(self.cursor)
			self.repaint()
		else:
			self.init_timer()
		return True

	def init_timer(self):
		if not self.timer is None:
			gobject.source_remove(self.timer)
			self.timer = None

	def set_repaint_timer(self):
		if self.timer is None:
			self.timer = gobject.timeout_add(RENDERING_DELAY, self.repaint)

	def set_drawing_timer(self):
		if self.timer is None:
			self.timer = gobject.timeout_add(RENDERING_DELAY, self.continuous_draw)

	def init_data(self):
		self.cursor = []
		self.paths = []
		self.points = []
		self.path = [[], [], const.CURVE_OPENED]
		self.point = []
		self.obj = None

	def clear_data(self):
		self.cursor = []
		self.points = []
		self.path = [[], [], const.CURVE_OPENED]
		self.point = []

	def init_flags(self):
		self.create = False
		self.draw = False

	def update_from_obj(self):
		self.paths = apply_trafo_to_paths(self.obj.paths, self.obj.trafo)
		path = self.paths[-1]
		if path[-1] == const.CURVE_OPENED:
			self.path = path
			self.points = self.path[1]
			paths = self.canvas.paths_doc_to_win(self.paths)
			self.canvas.renderer.paint_curve(paths)
		else:
			paths = self.canvas.paths_doc_to_win(self.paths)
			self.canvas.renderer.paint_curve(paths)
		self.draw = True

	def add_point(self, point):
		subpoint = bezier_base_point(point)
		if self.path[0]:
			w = h = config.curve_point_sensitivity_size
			start = self.canvas.point_doc_to_win(self.path[0])
			if self.points:
				p = self.canvas.point_doc_to_win(self.points[-1])
				last = bezier_base_point(p)
				if is_point_in_rect2(subpoint, start, w, h) and len(self.points) > 1:
					self.path[2] = const.CURVE_CLOSED
					if len(point) == 2:
						self.points.append([] + self.path[0])
					else:
						p = self.canvas.point_win_to_doc(point)
						self.points.append([p[0], p[1], [] + self.path[0], p[3]])
					if not self.ctrl_mask:
						self.release_curve()
					else:
						self.draw = False
					self.repaint()
				elif not is_point_in_rect2(subpoint, last, w, h):
					self.points.append(self.canvas.point_win_to_doc(point))
					self.path[1] = self.points
			else:
				if not is_point_in_rect2(subpoint, start, w, h):
					self.points.append(self.canvas.point_win_to_doc(point))
					self.path[1] = self.points
		else:
			self.path[0] = self.canvas.point_win_to_doc(point)
			self.paths.append(self.path)

	def release_curve(self):
		if self.points:
			if config.curve_autoclose_flag and self.path[2] == const.CURVE_OPENED:
				self.path[2] = const.CURVE_CLOSED
				self.points.append([] + self.path[0])
			paths = self.paths
			obj = self.obj
			self.stop_()
			if obj is None:
				self.api.create_curve(paths)
			else:
				self.api.update_curve(obj, paths)


class PathsCreator(PolyLineCreator):

	mode = modes.CURVE_MODE
	curve_point = []
	control_point0 = []
	control_point1 = []
	control_point2 = []

	def __init__(self, canvas, presenter):
		PolyLineCreator.__init__(self, canvas, presenter)

	def standby(self):
		self.init_timer()
		self.cursor = []
		self.repaint()
		self.point = self.canvas.point_win_to_doc(self.point)
		self.curve_point = self.canvas.point_win_to_doc(self.curve_point)
		self.control_point0 = self.canvas.point_win_to_doc(self.control_point0)
		self.control_point1 = self.canvas.point_win_to_doc(self.control_point1)
		self.control_point2 = self.canvas.point_win_to_doc(self.control_point2)

	def restore(self):
		self.point = self.canvas.point_doc_to_win(self.point)
		self.curve_point = self.canvas.point_doc_to_win(self.curve_point)
		self.control_point0 = self.canvas.point_doc_to_win(self.control_point0)
		self.control_point1 = self.canvas.point_doc_to_win(self.control_point1)
		self.control_point2 = self.canvas.point_doc_to_win(self.control_point2)
		self.repaint()

	def update_from_obj(self):
		self.paths = apply_trafo_to_paths(self.obj.paths, self.obj.trafo)
		path = self.paths[-1]
		if path[-1] == const.CURVE_OPENED:
			self.path = path
			self.points = self.path[1]
			paths = self.canvas.paths_doc_to_win(self.paths)
			self.canvas.renderer.paint_curve(paths)
			last = bezier_base_point(self.points[-1])
			self.control_point0 = self.canvas.point_doc_to_win(last)
			self.point = [] + self.control_point0
			self.control_point2 = [] + self.control_point0
			self.curve_point = [] + self.control_point0
		else:
			paths = self.canvas.paths_doc_to_win(self.paths)
			self.canvas.renderer.paint_curve(paths)
		self.draw = True

	def mouse_down(self, event):
		if event.button == LEFT_BUTTON:
			if not self.draw:
				self.draw = True
				self.clear_data()
			self.curve_point = [event.x, event.y]
			self.control_point2 = []
			self.create = True
			self.init_timer()
		elif event.button == MIDDLE_BUTTON:
			self.canvas.set_temp_mode(modes.TEMP_FLEUR_MODE)

	def mouse_up(self, event):
		if event.button == LEFT_BUTTON and self.draw:
			self.create = False
			self.ctrl_mask = False
			self.alt_mask = False
			self.control_point2 = [event.x, event.y]
			if event.state & gtk.gdk.CONTROL_MASK: self.ctrl_mask = True
			if event.state & gtk.gdk.MOD1_MASK : self.alt_mask = True
			if self.path[0]:
				if self.alt_mask:
					self.point = [event.x, event.y]
					self.add_point([event.x, event.y])
					self.control_point0 = [event.x, event.y]
					self.cursor = [event.x, event.y]
					self.curve_point = [event.x, event.y]
				elif self.control_point2:
					self.point = [] + self.curve_point
					self.control_point1 = contra_point(self.control_point2,
															 self.curve_point)
					self.add_point([self.control_point0, self.control_point1,
								self.curve_point, const.NODE_SYMMETRICAL])
					self.control_point0 = [] + self.control_point2
					self.cursor = [event.x, event.y]
					self.curve_point = [event.x, event.y]
			else:
				self.point = [event.x, event.y]
				self.add_point([event.x, event.y])
				self.control_point0 = [event.x, event.y]
			self.repaint()

	def mouse_move(self, event):
		if self.draw:
			if self.create:
				self.control_point2 = [event.x, event.y]
				self.cursor = [event.x, event.y]
			else:
				self.control_point2 = [event.x, event.y]
				self.cursor = [event.x, event.y]
				self.curve_point = [event.x, event.y]
			self.set_repaint_timer()
		else:
			self.init_timer()
			self.counter += 1
			if self.counter > 5:
				self.counter = 0
				point = [event.x, event.y]
				dpoint = self.canvas.win_to_doc(point)
				if self.selection.is_point_over_marker(dpoint):
					mark = self.selection.is_point_over_marker(dpoint)[0]
					self.canvas.resize_marker = mark
					self.cursor = []
					self.canvas.set_temp_mode(modes.RESIZE_MODE)

	def repaint(self):
		if self.path[0] or self.paths:
			paths = self.canvas.paths_doc_to_win(self.paths)
			cursor = self.cursor
			if not self.path[0]: cursor = []
			path = []
			if self.control_point0:
				self.control_point1 = contra_point(self.control_point2,
												self.curve_point)
				path = [self.point, [self.control_point0,
									self.control_point1,
									self.curve_point]]
			cpoint = []
			if self.create: cpoint = self.control_point2
			self.canvas.renderer.paint_curve(paths, cursor, path, cpoint)
		return True

	def init_data(self):
		PolyLineCreator.init_data(self)
		self.curve_point = []
		self.control_point0 = []
		self.control_point1 = []
		self.control_point2 = []





