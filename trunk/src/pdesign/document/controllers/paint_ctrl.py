# -*- coding: utf-8 -*-
#
# 	Copyright (C) 2013 by Igor E. Novikov
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.

from uc2.libgeom import contra_point, bezier_base_point
from uc2.libgeom import apply_trafo_to_paths, is_point_in_rect2
from uc2.formats.pdxf import const, model

from pdesign import modes, config
from pdesign.appconst import RENDERING_DELAY

from creators import AbstractCreator

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
	doc_point = []
	ctrl_mask = False
	alt_mask = False

	#Drawing timer to avoid repainting overhead
	timer = None
	timer_callback = None

	#Flags
	draw = False#entering into drawing mode
	create = False#entering into continuous drawing mode

	def __init__(self, canvas, presenter):
		AbstractCreator.__init__(self, canvas, presenter)

	def start_(self):
		self.snap = self.presenter.snap
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
		if not self.draw:
			self.draw = True
			self.clear_data()
		point = list(event.GetPositionTuple())
		flag, self.point, self.doc_point = self.snap.snap_point(point)
		self.create = True
		self.init_timer()

	def mouse_up(self, event):
		if self.draw:
			self.create = False
			self.ctrl_mask = event.ControlDown()
			self.alt_mask = event.AltDown()
			point = list(event.GetPositionTuple())
			flag, point, doc_point = self.snap.snap_point(point)
			self.add_point(point, doc_point)
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
					self.add_point(self.point, self.doc_point)
					self.point = []
					self.doc_point = []
				self.cursor = list(event.GetPositionTuple())
				self.set_drawing_timer()
			else:
				self.cursor = list(event.GetPositionTuple())
				self.set_repaint_timer()
		else:
			self.init_timer()
			self.counter += 1
			if self.counter > 5:
				self.counter = 0
				point = list(event.GetPositionTuple())
				dpoint = self.canvas.win_to_doc(point)
				if self.selection.is_point_over_marker(dpoint):
					mark = self.selection.is_point_over_marker(dpoint)[0]
					self.canvas.resize_marker = mark
					self.cursor = []
					self.canvas.set_temp_mode(modes.RESIZE_MODE)

	def repaint(self):
		if self.path[0] or self.paths:
			paths = self.canvas.paths_doc_to_win(self.paths)
			if self.cursor:
				flag, cursor, doc_point = self.snap.snap_point(self.cursor)
			else:
				cursor = []
			if not self.path[0]: cursor = []
			self.canvas.renderer.paint_curve(paths, cursor)
		return True

	def continuous_draw(self):
		if self.create and self.cursor:
			flag, point, doc_point = self.snap.snap_point(self.cursor)
			self.add_point(point, doc_point)
			self.repaint()
		else:
			self.init_timer()
		return True

	def on_timer(self, event):
		if not self.timer_callback is None:
			self.timer_callback()

	def init_timer(self):
		if self.timer.IsRunning():
			self.timer.Stop()
			self.timer_callback = None

	def set_repaint_timer(self):
		if not self.timer.IsRunning():
			self.timer_callback = self.repaint
			self.timer.Start(RENDERING_DELAY)

	def set_drawing_timer(self):
		if not self.timer.IsRunning():
			self.timer_callback = self.continuous_draw
			self.timer.Start(RENDERING_DELAY)

	def init_data(self):
		self.cursor = []
		self.paths = []
		self.points = []
		self.path = [[], [], const.CURVE_OPENED]
		self.point = []
		self.doc_point = []
		self.obj = None

	def clear_data(self):
		self.cursor = []
		self.points = []
		self.path = [[], [], const.CURVE_OPENED]
		self.point = []
		self.doc_point = []

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

	def add_point(self, point, doc_point):
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
						p = doc_point
						self.points.append([p[0], p[1], [] + self.path[0], p[3]])
					if not self.ctrl_mask:
						self.release_curve()
					else:
						self.draw = False
					self.repaint()
				elif not is_point_in_rect2(subpoint, last, w, h):
					self.points.append(doc_point)
					self.path[1] = self.points
			else:
				if not is_point_in_rect2(subpoint, start, w, h):
					self.points.append(doc_point)
					self.path[1] = self.points
		else:
			self.path[0] = doc_point
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
