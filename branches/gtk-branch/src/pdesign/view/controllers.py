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

import math

import gtk
import gobject

from uc2 import libgeom, uc2const

from pdesign import config, modes
from pdesign.appconst import LEFT_BUTTON, MIDDLE_BUTTON, RIGHT_BUTTON, RENDERING_DELAY

ZOOM_IN = 1.25
ZOOM_OUT = 0.8

class AbstractController:

	draw = False
	canvas = None
	snap = None
	start = []
	end = []
	start_doc = []
	end_doc = []
	check_snap = False

	counter = 0
	timer = None

	mode = None

	def __init__(self, canvas, presenter):
		self.canvas = canvas
		self.app = presenter.app
		self.presenter = presenter
		self.selection = presenter.selection
		self.eventloop = presenter.eventloop
		self.api = presenter.api
		self.start = []
		self.end = []
		self.start_doc = []
		self.end_doc = []

	def set_cursor(self):
		if self.mode is None:
			self.canvas.set_canvas_cursor(self.canvas.mode)
		else:
			self.canvas.set_canvas_cursor(self.mode)

	def start_(self):pass
	def stop_(self):pass
	def standby(self):pass
	def restore(self):pass
	def repaint(self):pass
	def do_action(self, event): pass
	def mouse_double_click(self, event): pass

	def mouse_down(self, event):
		self.snap = self.presenter.snap
		self.start = []
		self.end = []
		self.start_doc = []
		self.end_doc = []

		self.counter = 0
		if not  self.timer is None:
			gobject.source_remove(self.timer)
		self.timer = None

		if event.button == LEFT_BUTTON:
			self.draw = True
			self.start = [event.x, event.y]
			self.end = [event.x, event.y]
			if self.check_snap:
				self.start, self.start_doc = self.snap.snap_point(self.start)[1:]
				self.end, self.end_doc = self.snap.snap_point(self.end)[1:]
			self.counter = 0
			self.timer = gobject.timeout_add(RENDERING_DELAY, self._draw_frame)
		elif event.button == MIDDLE_BUTTON:
			self.canvas.set_temp_mode(modes.TEMP_FLEUR_MODE)

	def mouse_up(self, event):
		if event.button == LEFT_BUTTON:
			if self.draw:
				gobject.source_remove(self.timer)
				self.draw = False
				self.counter = 0
				self.end = [event.x, event.y]
				if self.check_snap:
					self.end, self.end_doc = self.snap.snap_point(self.end)[1:]
				self.canvas.renderer.stop_draw_frame(self.start, self.end)
				self.do_action(event)

	def mouse_move(self, event):
		if self.draw:
			self.end = [event.x, event.y]
			if self.check_snap:
				self.end, self.end_doc = self.snap.snap_point(self.end)[1:]


	def wheel(self, event):
		va = self.canvas.mw.v_adj
		dy = va.get_step_increment()
		direction = 1
		if event.direction == gtk.gdk.SCROLL_DOWN:
			direction = -1
		va.set_value(va.get_value() - dy * direction)

	def _draw_frame(self, *args):
		if self.end:
			self.canvas.renderer.draw_frame(self.start, self.end)
			self.end = []
		return True

class FleurController(AbstractController):

	mode = modes.FLEUR_MODE
	move = False
	fleur_timer = None

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)

	def mouse_down(self, event):
		self.move = True

	def mouse_up(self, event):
		if self.start:
			if not self.fleur_timer is None:
				gobject.source_remove(self.fleur_timer)
			self.end = [event.x, event.y]
			dx = self.end[0] - self.start[0]
			dy = self.end[1] - self.start[1]
			ha = self.canvas.mw.h_adj
			va = self.canvas.mw.v_adj
			zoom = self.canvas.zoom
			ha.set_value(ha.get_value() - dx / zoom)
			va.set_value(va.get_value() - dy / zoom)

			self.start = []
			self.end = []
			self.move = False

	def mouse_move(self, event):
		if self.move:
			if self.start:
				self.end = [event.x, event.y]
			else:
				self.start = [event.x, event.y]
				self.fleur_timer = gobject.timeout_add(RENDERING_DELAY, self._scroll_canvas)

	def _scroll_canvas(self, *args):
		if self.start and self.end:
			dx = self.end[0] - self.start[0]
			dy = self.end[1] - self.start[1]
			if dx <> 0 or dy <> 0:
				ha = self.canvas.mw.h_adj
				va = self.canvas.mw.v_adj
				zoom = self.canvas.zoom
				ha.set_value(ha.get_value() - dx / zoom)
				va.set_value(va.get_value() - dy / zoom)
				self.start = self.end
		return True

class TempFleurController(FleurController):

	mode = modes.TEMP_FLEUR_MODE
	move = True

	def __init__(self, canvas, presenter):
		FleurController.__init__(self, canvas, presenter)

	def mouse_down(self, event):pass

	def mouse_up(self, event):
		FleurController.mouse_up(self, event)
		self.move = True
		self.canvas.restore_mode()

class ZoomController(AbstractController):

	mode = modes.ZOOM_MODE

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)

	def mouse_down(self, event):
		if event.button == LEFT_BUTTON:
			AbstractController.mouse_down(self, event)
		elif event.button == RIGHT_BUTTON:
			self.start = [event.x, event.y]
			cursor = self.canvas.app.cursors[modes.ZOOM_OUT_MODE]
			self.canvas.set_temp_cursor(cursor)
		elif event.button == MIDDLE_BUTTON:
			self.canvas.set_temp_mode(modes.TEMP_FLEUR_MODE)

	def mouse_up(self, event):
		if event.button == LEFT_BUTTON:
			AbstractController.mouse_up(self, event)
		if event.button == RIGHT_BUTTON:
			if not self.draw:
				self.canvas.zoom_at_point(self.start, ZOOM_OUT)
				self.canvas.restore_cursor()

	def do_action(self, event):
		if self.start and self.end:
			change_x = abs(self.end[0] - self.start[0])
			change_y = abs(self.end[1] - self.start[1])
			if change_x < 5 and change_y < 5:
				self.canvas.zoom_at_point(self.start, ZOOM_IN)
			else:
				self.canvas.zoom_to_rectangle(self.start, self.end)
			self.start = []
			self.end = []

class SelectController(AbstractController):

	mode = modes.SELECT_MODE

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)

	def mouse_move(self, event):
		self.snap = self.presenter.snap
		if self.draw:
			AbstractController.mouse_move(self, event)
		else:
			self.counter += 1
			if self.counter > 5:
				self.counter = 0
				point = [event.x, event.y]
				dpoint = self.canvas.win_to_doc(point)
				if self.selection.is_point_over(dpoint):
					self.canvas.set_temp_mode(modes.MOVE_MODE)
				elif self.selection.is_point_over_marker(dpoint):
					mark = self.selection.is_point_over_marker(dpoint)[0]
					self.canvas.resize_marker = mark
					self.canvas.set_temp_mode(modes.RESIZE_MODE)
				elif self.snap.is_over_guide(point)[0]:
					self.canvas.set_temp_mode(modes.GUIDE_MODE)

	def do_action(self, event):
		if self.start and self.end:
			add_flag = False
			if event.state & gtk.gdk.SHIFT_MASK:
				add_flag = True
			change_x = abs(self.end[0] - self.start[0])
			change_y = abs(self.end[1] - self.start[1])
			if change_x < 5 and change_y < 5:
				self.canvas.select_at_point(self.start, add_flag)
			else:
				self.canvas.select_by_rect(self.start, self.end, add_flag)

			dpoint = self.canvas.win_to_doc(self.start)
			if self.selection.is_point_over(dpoint):
				self.canvas.set_temp_mode(modes.MOVE_MODE)

class PickController(AbstractController):

	mode = modes.PICK_MODE

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)

	def mouse_down(self, event):pass

	def mouse_up(self, event):
		if event.button == LEFT_BUTTON:
			self.end = [event.x, event.y]
			self.do_action()

	def mouse_move(self, event):pass

	def do_action(self):
		obj = self.canvas.pick_at_point(self.end)
		if not self.callback(obj):
			self.callback = None
			self.canvas.restore_mode()

class GuideController(AbstractController):

	mode = modes.HGUIDE_MODE
	guide = None

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)

	def mouse_down(self, event):
		self.draw = True
		self.end = [event.x, event.y]
		self.timer = gobject.timeout_add(RENDERING_DELAY, self.repaint)

	def mouse_move(self, event):
		self.end = [event.x, event.y]
		if not self.draw:
			ret = self.snap.is_over_guide(self.end)[0]
			if not ret:
				self.canvas.restore_mode()

	def mouse_up(self, event):
		self.end = [event.x, event.y]
		self.draw = False
		if self.mode == modes.HGUIDE_MODE and self.end[1] > 0:
			p_doc = self.presenter.snap.snap_point(self.end, snap_x=False)[2]
			pos = p_doc[1]
			orient = uc2const.HORIZONTAL
			self.presenter.api.set_guide_propeties(self.guide, pos, orient)
		elif self.mode == modes.VGUIDE_MODE and self.end[0] > 0:
			p_doc = self.presenter.snap.snap_point(self.end, snap_y=False)[2]
			orient = uc2const.VERTICAL
			pos = p_doc[0]
			self.presenter.api.set_guide_propeties(self.guide, pos, orient)
		else:
			self.presenter.api.delete_guides([self.guide])
		self.repaint()
		self.canvas.selection_repaint()
		self.canvas.restore_mode()

	def start_(self):
		self.snap = self.presenter.snap
		if not self.snap.active_guide is None:
			self.guide = self.snap.active_guide

	def stop_(self):
		if not  self.timer is None:
			gobject.source_remove(self.timer)
		self.end = []
		self.guide = None

	def set_cursor(self):
		if not self.guide is None:
			if self.guide.orientation == uc2const.HORIZONTAL:
				mode = modes.HGUIDE_MODE
			else:
				mode = modes.VGUIDE_MODE
			self.mode = mode
			self.canvas.set_canvas_cursor(mode)

	def repaint(self, *args):
		p_doc = []
		orient = uc2const.HORIZONTAL
		if self.end:
			if self.mode == modes.HGUIDE_MODE:
				p_doc = self.presenter.snap.snap_point(self.end, snap_x=False)[2]
			else:
				p_doc = self.presenter.snap.snap_point(self.end, snap_y=False)[2]
				orient = uc2const.VERTICAL
		self.canvas.renderer.paint_guide_dragging(p_doc, orient)
		return True

class MoveController(AbstractController):

	start = None
	end = None
	trafo = []
	mode = modes.MOVE_MODE

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)
		self.move = False
		self.moved = False
		self.copy = False
		self.trafo = []

	def mouse_down(self, event):
		self.snap = self.presenter.snap
		if event.button == LEFT_BUTTON:
			self.start = [event.x, event.y]
			self.move = True
			self.canvas.renderer.show_move_frame()
			self.timer = gobject.timeout_add(RENDERING_DELAY, self._draw_frame)

	def _draw_frame(self, *args):
		if self.end:
			self.canvas.renderer.draw_move_frame(self.trafo)
			self.end = []
		return True

	def _calc_trafo(self, point1, point2):
		start_point = self.canvas.win_to_doc(point1)
		end_point = self.canvas.win_to_doc(point2)
		dx = end_point[0] - start_point[0]
		dy = end_point[1] - start_point[1]
		return [1.0, 0.0, 0.0, 1.0, dx, dy]

	def mouse_move(self, event):
		if self.move:
			self.moved = True
			new = [event.x, event.y]
			if event.state & gtk.gdk.CONTROL_MASK:
				change = [new[0] - self.start[0], new[1] - self.start[1]]
				if abs(change[0]) > abs(change[1]):
					new[1] = self.start[1]
				else:
					new[0] = self.start[0]
			self.end = new
			self.trafo = self._calc_trafo(self.start, self.end)
			bbox = self.presenter.selection.bbox
			self.trafo = self._snap(bbox, self.trafo)
		else:
			point = [event.x, event.y]
			dpoint = self.canvas.win_to_doc(point)
			if self.selection.is_point_over(dpoint):
				if self.selection.is_point_over_marker(dpoint):
					mark = self.selection.is_point_over_marker(dpoint)[0]
					self.canvas.resize_marker = mark
					self.canvas.restore_mode()
					self.canvas.set_temp_mode(modes.RESIZE_MODE)
			else:
				self.canvas.restore_mode()

	def mouse_up(self, event):
		if self.move and event.button == LEFT_BUTTON:
			gobject.source_remove(self.timer)
			new = [event.x, event.y]
			if event.state & gtk.gdk.CONTROL_MASK:
				change = [new[0] - self.start[0], new[1] - self.start[1]]
				if abs(change[0]) > abs(change[1]):
					new[1] = self.start[1]
				else:
					new[0] = self.start[0]
			self.end = new
			self.canvas.renderer.hide_move_frame()
			self.move = False
			if self.moved:
				self.trafo = self._calc_trafo(self.start, self.end)
				bbox = self.presenter.selection.bbox
				self.trafo = self._snap(bbox, self.trafo)
				self.api.transform_selected(self.trafo, self.copy)
			elif event.state & gtk.gdk.SHIFT_MASK:
				self.canvas.select_at_point(self.start, True)
				if not self.selection.is_point_over(self.start):
					self.canvas.restore_mode()
			if self.copy:
				self.canvas.restore_cursor()
			self.moved = False
			self.copy = False
			self.start = []
			self.end = []

		elif self.moved and event.button == RIGHT_BUTTON:
			self.copy = True
			cursor = self.app.cursors[modes.COPY_MODE]
			self.canvas.set_temp_cursor(cursor)

	def _snap(self, bbox, trafo):
		result = [] + trafo
		points = libgeom.bbox_middle_points(bbox)
		tr_points = libgeom.apply_trafo_to_points(points, trafo)
		active_snap = [None, None]

		shift_x = []
		snap_x = []
		for point in [tr_points[0], tr_points[2], tr_points[1]]:
			flag, wp, dp = self.snap.snap_point(point, False, snap_y=False)
			if flag:
				shift_x.append(dp[0] - point[0])
				snap_x.append(dp[0])
		if shift_x:
			if len(shift_x) > 1:
				if abs(shift_x[0]) < abs(shift_x[1]):
					dx = shift_x[0]
					active_snap[0] = snap_x[0]
				else:
					dx = shift_x[1]
					active_snap[0] = snap_x[1]
			else:
				dx = shift_x[0]
				active_snap[0] = snap_x[0]
			result[4] += dx

		shift_y = []
		snap_y = []
		for point in [tr_points[1], tr_points[3], tr_points[2]]:
			flag, wp, dp = self.snap.snap_point(point, False, snap_x=False)
			if flag:
				shift_y.append(dp[1] - point[1])
				snap_y.append(dp[1])
		if shift_y:
			if len(shift_y) > 1:
				if abs(shift_y[0]) < abs(shift_y[1]):
					dy = shift_y[0]
					active_snap[1] = snap_y[0]
				else:
					dy = shift_y[1]
					active_snap[1] = snap_y[1]
			else:
				dy = shift_y[0]
				active_snap[1] = snap_y[0]
			result[5] += dy

		self.snap.active_snap = [] + active_snap
		return result

class TransformController(AbstractController):

	mode = modes.RESIZE_MODE

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)
		self.move = False
		self.moved = False
		self.copy = False
		self.frame = []

	def mouse_move(self, event):
		if not self.move:
			point = self.canvas.win_to_doc([event.x, event.y])
			ret = self.selection.is_point_over_marker(point)
			if not ret:
				self.canvas.restore_mode()
			elif not ret[0] == self.canvas.resize_marker:
				self.canvas.resize_marker = ret[0]
				self.set_cursor()

		else:
			self.end = [event.x, event.y]
			self.trafo = self._calc_trafo(event)
			self.moved = True


	def mouse_down(self, event):
		self.snap = self.presenter.snap
		if event.button == LEFT_BUTTON:
			self.start = [event.x, event.y]
			self.move = True
			if not self.canvas.resize_marker == 9:
				self.canvas.renderer.show_move_frame()
				self.timer = gobject.timeout_add(RENDERING_DELAY, self._draw_frame)
			else:
				self.offset_start = [] + self.selection.center_offset
				self.timer = gobject.timeout_add(RENDERING_DELAY, self._draw_center)

	def mouse_up(self, event):
		if event.button == LEFT_BUTTON:
			gobject.source_remove(self.timer)
			self.end = [event.x, event.y]
			self.move = False
			if not self.canvas.resize_marker == 9:
				self.canvas.renderer.hide_move_frame()
				if self.moved:
					self.trafo = self._calc_trafo(event)
					self.api.transform_selected(self.trafo, self.copy)
				self.moved = False
				self.copy = False
				self.start = []
				self.end = []
				point = self.canvas.win_to_doc([event.x, event.y])
				if not self.selection.is_point_over_marker(point):
					self.canvas.restore_mode()
			else:
				self._draw_center()
				self.moved = False
				self.copy = False
				self.start = []
				self.end = []

		if event.button == RIGHT_BUTTON and self.moved:
			self.copy = True
			self.set_cursor()

	def set_cursor(self):
		mark = self.canvas.resize_marker
		mode = self.mode
		if mark == 0 or mark == 8:
			if self.copy: mode = modes.RESIZE_MODE1_COPY
			else: mode = modes.RESIZE_MODE1
		if mark == 1 or mark == 7:
			if self.copy: mode = modes.RESIZE_MODE2_COPY
			else: mode = modes.RESIZE_MODE2
		if mark == 2 or mark == 6:
			if self.copy: mode = modes.RESIZE_MODE3_COPY
			else: mode = modes.RESIZE_MODE3
		if mark == 3 or mark == 5:
			if self.copy: mode = modes.RESIZE_MODE4_COPY
			else: mode = modes.RESIZE_MODE4
		if mark == 9:
			mode = modes.RESIZE_MODE
		if mark in [10, 12, 15, 17]:
			if self.copy: mode = modes.RESIZE_MODE10_COPY
			else: mode = modes.RESIZE_MODE10
		if mark in [11, 16]:
			if self.copy: mode = modes.RESIZE_MODE11_COPY
			else: mode = modes.RESIZE_MODE11
		if mark in [13, 14]:
			if self.copy: mode = modes.RESIZE_MODE13_COPY
			else: mode = modes.RESIZE_MODE13
		self.mode = mode
		self.canvas.set_canvas_cursor(mode)

	def _calc_trafo(self, event):
		control = shift = False
		if event.state & gtk.gdk.CONTROL_MASK:
			control = True
		if event.state & gtk.gdk.SHIFT_MASK:
			shift = True
		mark = self.canvas.resize_marker
		start_point = self.canvas.win_to_doc(self.start)
		end_point = self.canvas.win_to_doc(self.end)
		bbox = self.presenter.selection.bbox
		middle_points = libgeom.bbox_middle_points(bbox)
		w = bbox[2] - bbox[0]
		h = bbox[3] - bbox[1]
		m11 = m22 = 1.0
		m12 = m21 = 0.0
		dx = dy = 0.0
		snap = [None, None]
		if mark == 0:
			dx = start_point[0] - end_point[0]
			dy = end_point[1] - start_point[1]
			if shift:
				if control:
					m11 = (w + 2.0 * dx) / w
					m22 = (h + 2.0 * dy) / h
					dx = -(bbox[2] * m11 - bbox[2]) + w * (m11 - 1.0) / 2.0
					dy = -(bbox[1] * m22 - bbox[1]) - h * (m22 - 1.0) / 2.0
					#---- snapping
					point = middle_points[0]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = point[0] - p_doc[0]
						m11 = (w + 2.0 * dx) / w
						dx = -(bbox[2] * m11 - bbox[2]) + w * (m11 - 1.0) / 2.0
						snap[0] = self.snap.active_snap[0]
					point = middle_points[1]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
					if f:
						dy = p_doc[1] - point[1]
						m22 = (h + 2.0 * dy) / h
						dy = -(bbox[1] * m22 - bbox[1]) - h * (m22 - 1.0) / 2.0
						snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping
				else:
					if abs(dx) < abs(dy):
						m11 = m22 = (w + 2.0 * dx) / w
					else:
						m11 = m22 = (h + 2.0 * dy) / h
					dx = -(bbox[2] * m11 - bbox[2]) + w * (m11 - 1.0) / 2.0
					dy = -(bbox[1] * m22 - bbox[1]) - h * (m22 - 1.0) / 2.0
					#---- snapping
					point = middle_points[0]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = point[0] - p_doc[0]
						m11 = m22 = (w + 2.0 * dx) / w
						dx = -(bbox[2] * m11 - bbox[2]) + w * (m11 - 1.0) / 2.0
						dy = -(bbox[1] * m22 - bbox[1]) - h * (m22 - 1.0) / 2.0
						snap[0] = self.snap.active_snap[0]
					else:
						point = middle_points[1]
						trafo = [m11, m21, m12, m22, dx, dy]
						p = libgeom.apply_trafo_to_point(point, trafo)
						f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
						if f:
							dy = p_doc[1] - point[1]
							m11 = m22 = (h + 2.0 * dy) / h
							dx = -(bbox[2] * m11 - bbox[2]) + w * (m11 - 1.0) / 2.0
							dy = -(bbox[1] * m22 - bbox[1]) - h * (m22 - 1.0) / 2.0
							snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping	
			else:
				if control:
					m11 = (w + dx) / w
					m22 = (h + dy) / h
					dx = -(bbox[2] * m11 - bbox[2])
					dy = -(bbox[1] * m22 - bbox[1])
					#---- snapping
					point = middle_points[0]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = point[0] - p_doc[0]
						m11 = (w + dx) / w
						dx = -(bbox[2] * m11 - bbox[2])
						snap[0] = self.snap.active_snap[0]
					point = middle_points[1]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
					if f:
						dy = p_doc[1] - point[1]
						m22 = (h + dy) / h
						dy = -(bbox[1] * m22 - bbox[1])
						snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping
				else:
					if abs(dx) < abs(dy):
						m11 = m22 = (w + dx) / w
					else:
						m11 = m22 = (h + dy) / h
					dx = -(bbox[2] * m11 - bbox[2])
					dy = -(bbox[1] * m22 - bbox[1])
					#---- snapping
					point = middle_points[0]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = point[0] - p_doc[0]
						m11 = m22 = (w + dx) / w
						dx = -(bbox[2] * m11 - bbox[2])
						dy = -(bbox[1] * m22 - bbox[1])
						snap[0] = self.snap.active_snap[0]
					else:
						point = middle_points[1]
						trafo = [m11, m21, m12, m22, dx, dy]
						p = libgeom.apply_trafo_to_point(point, trafo)
						f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
						if f:
							dy = p_doc[1] - point[1]
							m11 = m22 = (h + dy) / h
							dx = -(bbox[2] * m11 - bbox[2])
							dy = -(bbox[1] * m22 - bbox[1])
							snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping					
		if mark == 1:
			dy = end_point[1] - start_point[1]
			if shift:
				m22 = (h + 2.0 * dy) / h
				dy = -(bbox[1] * m22 - bbox[1]) - h * (m22 - 1.0) / 2.0
				#---- snapping
				point = middle_points[1]
				trafo = [m11, m21, m12, m22, dx, dy]
				p = libgeom.apply_trafo_to_point(point, trafo)
				f, p, p_doc = self.snap.snap_point(p, False)
				dy = p_doc[1] - point[1]
				m22 = (h + 2.0 * dy) / h
				dy = -(bbox[1] * m22 - bbox[1]) - h * (m22 - 1.0) / 2.0
				#---- snapping
			else:
				m22 = (h + dy) / h
				dy = -(bbox[1] * m22 - bbox[1])
				#---- snapping
				point = middle_points[1]
				trafo = [m11, m21, m12, m22, dx, dy]
				p = libgeom.apply_trafo_to_point(point, trafo)
				f, p, p_doc = self.snap.snap_point(p, False)
				dy = p_doc[1] - point[1]
				m22 = (h + dy) / h
				dy = -(bbox[1] * m22 - bbox[1])
				#---- snapping
		if mark == 2:
			dx = end_point[0] - start_point[0]
			dy = end_point[1] - start_point[1]
			if shift:
				if control:
					m11 = (w + 2.0 * dx) / w
					m22 = (h + 2.0 * dy) / h
					dx = -(bbox[0] * m11 - bbox[0]) - w * (m11 - 1.0) / 2.0
					dy = -(bbox[1] * m22 - bbox[1]) - h * (m22 - 1.0) / 2.0
					#---- snapping
					point = middle_points[2]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = p_doc[0] - point[0]
						m11 = (w + 2.0 * dx) / w
						dx = -(bbox[0] * m11 - bbox[0]) - w * (m11 - 1.0) / 2.0
						snap[0] = self.snap.active_snap[0]
					point = middle_points[1]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
					if f:
						dy = p_doc[1] - point[1]
						m22 = (h + 2.0 * dy) / h
						dy = -(bbox[1] * m22 - bbox[1]) - h * (m22 - 1.0) / 2.0
						snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping
				else:
					if abs(dx) < abs(dy):
						m11 = m22 = (w + 2.0 * dx) / w
					else:
						m11 = m22 = (h + 2.0 * dy) / h
					dx = -(bbox[0] * m11 - bbox[0]) - w * (m11 - 1.0) / 2.0
					dy = -(bbox[1] * m22 - bbox[1]) - h * (m22 - 1.0) / 2.0
					#---- snapping
					point = middle_points[2]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = p_doc[0] - point[0]
						m11 = m22 = (w + 2.0 * dx) / w
						dx = -(bbox[0] * m11 - bbox[0]) - w * (m11 - 1.0) / 2.0
						dy = -(bbox[1] * m22 - bbox[1]) - h * (m22 - 1.0) / 2.0
						snap[0] = self.snap.active_snap[0]
					else:
						point = middle_points[1]
						trafo = [m11, m21, m12, m22, dx, dy]
						p = libgeom.apply_trafo_to_point(point, trafo)
						f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
						if f:
							dy = p_doc[1] - point[1]
							m11 = m22 = (h + 2.0 * dy) / h
							dx = -(bbox[0] * m11 - bbox[0]) - w * (m11 - 1.0) / 2.0
							dy = -(bbox[1] * m22 - bbox[1]) - h * (m22 - 1.0) / 2.0
							snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping
			else:
				if control:
					m11 = (w + dx) / w
					m22 = (h + dy) / h
					dx = -(bbox[0] * m11 - bbox[0])
					dy = -(bbox[1] * m22 - bbox[1])
					#---- snapping
					point = middle_points[2]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = p_doc[0] - point[0]
						m11 = (w + dx) / w
						dx = -(bbox[0] * m11 - bbox[0])
						snap[0] = self.snap.active_snap[0]
					point = middle_points[1]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
					if f:
						dy = p_doc[1] - point[1]
						m22 = (h + dy) / h
						dy = -(bbox[1] * m22 - bbox[1])
						snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping
				else:
					if abs(dx) < abs(dy):
						m11 = m22 = (w + dx) / w
					else:
						m11 = m22 = (h + dy) / h
					dx = -(bbox[0] * m11 - bbox[0])
					dy = -(bbox[1] * m22 - bbox[1])
					#---- snapping
					point = middle_points[2]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = p_doc[0] - point[0]
						m11 = m22 = (w + dx) / w
						dx = -(bbox[0] * m11 - bbox[0])
						dy = -(bbox[1] * m22 - bbox[1])
						snap[0] = self.snap.active_snap[0]
					else:
						point = middle_points[1]
						trafo = [m11, m21, m12, m22, dx, dy]
						p = libgeom.apply_trafo_to_point(point, trafo)
						f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
						if f:
							dy = p_doc[1] - point[1]
							m11 = m22 = (h + dy) / h
							dx = -(bbox[0] * m11 - bbox[0])
							dy = -(bbox[1] * m22 - bbox[1])
							snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping			
		if mark == 3:
			dx = start_point[0] - end_point[0]
			if shift:
				m11 = (w + 2.0 * dx) / w
				dx = -(bbox[2] * m11 - bbox[2]) + w * (m11 - 1.0) / 2.0
				#---- snapping
				point = middle_points[0]
				trafo = [m11, m21, m12, m22, dx, dy]
				p = libgeom.apply_trafo_to_point(point, trafo)
				f, p, p_doc = self.snap.snap_point(p, False)
				dx = point[0] - p_doc[0]
				m11 = (w + 2.0 * dx) / w
				dx = -(bbox[2] * m11 - bbox[2]) + w * (m11 - 1.0) / 2.0
				#---- snapping
			else:
				m11 = (w + dx) / w
				dx = -(bbox[2] * m11 - bbox[2])
				#---- snapping
				point = middle_points[0]
				trafo = [m11, m21, m12, m22, dx, dy]
				p = libgeom.apply_trafo_to_point(point, trafo)
				f, p, p_doc = self.snap.snap_point(p, False)
				dx = point[0] - p_doc[0]
				m11 = (w + dx) / w
				dx = -(bbox[2] * m11 - bbox[2])
				#---- snapping
		if mark == 5:
			dx = end_point[0] - start_point[0]
			if shift:
				m11 = (w + 2.0 * dx) / w
				dx = -(bbox[0] * m11 - bbox[0]) - w * (m11 - 1.0) / 2.0
				#---- snapping
				point = middle_points[2]
				trafo = [m11, m21, m12, m22, dx, dy]
				p = libgeom.apply_trafo_to_point(point, trafo)
				f, p, p_doc = self.snap.snap_point(p, False)
				dx = p_doc[0] - point[0]
				m11 = (w + 2.0 * dx) / w
				dx = -(bbox[0] * m11 - bbox[0]) - w * (m11 - 1.0) / 2.0
				#---- snapping
			else:
				m11 = (w + dx) / w
				dx = -(bbox[0] * m11 - bbox[0])
				#---- snapping
				point = middle_points[2]
				trafo = [m11, m21, m12, m22, dx, dy]
				p = libgeom.apply_trafo_to_point(point, trafo)
				f, p, p_doc = self.snap.snap_point(p, False)
				dx = p_doc[0] - point[0]
				m11 = (w + dx) / w
				dx = -(bbox[0] * m11 - bbox[0])
				#---- snapping
		if mark == 6:
			dx = start_point[0] - end_point[0]
			dy = start_point[1] - end_point[1]
			if shift:
				if control:
					m11 = (w + 2.0 * dx) / w
					m22 = (h + 2.0 * dy) / h
					dx = -(bbox[2] * m11 - bbox[2]) + w * (m11 - 1.0) / 2.0
					dy = -(bbox[3] * m22 - bbox[3]) + h * (m22 - 1.0) / 2.0
					#---- snapping
					point = middle_points[0]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = point[0] - p_doc[0]
						m11 = (w + 2.0 * dx) / w
						dx = -(bbox[2] * m11 - bbox[2]) + w * (m11 - 1.0) / 2.0
						snap[0] = self.snap.active_snap[0]
					point = middle_points[3]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
					if f:
						dy = point[1] - p_doc[1]
						m22 = (h + 2.0 * dy) / h
						dy = -(bbox[3] * m22 - bbox[3]) + h * (m22 - 1.0) / 2.0
						snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping
				else:
					if abs(dx) < abs(dy):
						m11 = m22 = (w + 2.0 * dx) / w
					else:
						m11 = m22 = (h + 2.0 * dy) / h
					dx = -(bbox[2] * m11 - bbox[2]) + w * (m11 - 1.0) / 2.0
					dy = -(bbox[3] * m22 - bbox[3]) + h * (m22 - 1.0) / 2.0
					#---- snapping
					point = middle_points[0]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = point[0] - p_doc[0]
						m11 = m22 = (w + 2.0 * dx) / w
						dx = -(bbox[2] * m11 - bbox[2]) + w * (m11 - 1.0) / 2.0
						dy = -(bbox[3] * m22 - bbox[3]) + h * (m22 - 1.0) / 2.0
						snap[0] = self.snap.active_snap[0]
					else:
						point = middle_points[3]
						trafo = [m11, m21, m12, m22, dx, dy]
						p = libgeom.apply_trafo_to_point(point, trafo)
						f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
						if f:
							dy = point[1] - p_doc[1]
							m11 = m22 = (h + 2.0 * dy) / h
							dx = -(bbox[2] * m11 - bbox[2]) + w * (m11 - 1.0) / 2.0
							dy = -(bbox[3] * m22 - bbox[3]) + h * (m22 - 1.0) / 2.0
							snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping
			else:
				if control:
					m11 = (w + dx) / w
					m22 = (h + dy) / h
					dx = -(bbox[2] * m11 - bbox[2])
					dy = -(bbox[3] * m22 - bbox[3])
					#---- snapping
					point = middle_points[0]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = point[0] - p_doc[0]
						m11 = (w + dx) / w
						dx = -(bbox[2] * m11 - bbox[2])
						snap[0] = self.snap.active_snap[0]
					point = middle_points[3]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
					if f:
						dy = point[1] - p_doc[1]
						m22 = (h + dy) / h
						dy = -(bbox[3] * m22 - bbox[3])
						snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping
				else:
					if abs(dx) < abs(dy):
						m11 = m22 = (w + dx) / w
					else:
						m11 = m22 = (h + dy) / h
					dx = -(bbox[2] * m11 - bbox[2])
					dy = -(bbox[3] * m22 - bbox[3])
					#---- snapping
					point = middle_points[0]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = point[0] - p_doc[0]
						m11 = m22 = (w + dx) / w
						dx = -(bbox[2] * m11 - bbox[2])
						dy = -(bbox[3] * m22 - bbox[3])
						snap[0] = self.snap.active_snap[0]
					else:
						point = middle_points[3]
						trafo = [m11, m21, m12, m22, dx, dy]
						p = libgeom.apply_trafo_to_point(point, trafo)
						f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
						if f:
							dy = point[1] - p_doc[1]
							m11 = m22 = (h + dy) / h
							dx = -(bbox[2] * m11 - bbox[2])
							dy = -(bbox[3] * m22 - bbox[3])
							snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping	
		if mark == 7:
			dy = start_point[1] - end_point[1]
			if shift:
				m22 = (h + 2.0 * dy) / h
				dy = -(bbox[3] * m22 - bbox[3]) + h * (m22 - 1.0) / 2.0
				#---- snapping
				point = middle_points[3]
				trafo = [m11, m21, m12, m22, dx, dy]
				p = libgeom.apply_trafo_to_point(point, trafo)
				f, p, p_doc = self.snap.snap_point(p, False)
				dy = point[1] - p_doc[1]
				m22 = (h + 2.0 * dy) / h
				dy = -(bbox[3] * m22 - bbox[3]) + h * (m22 - 1.0) / 2.0
				#---- snapping
			else:
				m22 = (h + dy) / h
				dy = -(bbox[3] * m22 - bbox[3])
				#---- snapping
				point = middle_points[3]
				trafo = [m11, m21, m12, m22, dx, dy]
				p = libgeom.apply_trafo_to_point(point, trafo)
				f, p, p_doc = self.snap.snap_point(p, False)
				dy = point[1] - p_doc[1]
				m22 = (h + dy) / h
				dy = -(bbox[3] * m22 - bbox[3])
				#---- snapping
		if mark == 8:
			dx = end_point[0] - start_point[0]
			dy = start_point[1] - end_point[1]
			if shift:
				if control:
					m11 = (w + 2.0 * dx) / w
					m22 = (h + 2.0 * dy) / h
					dx = -(bbox[0] * m11 - bbox[0]) - w * (m11 - 1.0) / 2.0
					dy = -(bbox[3] * m22 - bbox[3]) + h * (m22 - 1.0) / 2.0
					#---- snapping
					point = middle_points[2]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = p_doc[0] - point[0]
						m11 = (w + 2.0 * dx) / w
						dx = -(bbox[0] * m11 - bbox[0]) - w * (m11 - 1.0) / 2.0
						snap[0] = self.snap.active_snap[0]
					point = middle_points[3]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
					if f:
						dy = point[1] - p_doc[1]
						m22 = (h + 2.0 * dy) / h
						dy = -(bbox[3] * m22 - bbox[3]) + h * (m22 - 1.0) / 2.0
						snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping
				else:
					if abs(dx) < abs(dy):
						m11 = m22 = (w + 2.0 * dx) / w
					else:
						m11 = m22 = (h + 2.0 * dy) / h
					dx = -(bbox[0] * m11 - bbox[0]) - w * (m11 - 1.0) / 2.0
					dy = -(bbox[3] * m22 - bbox[3]) + h * (m22 - 1.0) / 2.0
					#---- snapping
					point = middle_points[2]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = p_doc[0] - point[0]
						m11 = m22 = (w + 2.0 * dx) / w
						dx = -(bbox[0] * m11 - bbox[0]) - w * (m11 - 1.0) / 2.0
						dy = -(bbox[3] * m22 - bbox[3]) + h * (m22 - 1.0) / 2.0
						snap[0] = self.snap.active_snap[0]
					else:
						point = middle_points[3]
						trafo = [m11, m21, m12, m22, dx, dy]
						p = libgeom.apply_trafo_to_point(point, trafo)
						f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
						if f:
							dy = point[1] - p_doc[1]
							m11 = m22 = (h + 2.0 * dy) / h
							dx = -(bbox[0] * m11 - bbox[0]) - w * (m11 - 1.0) / 2.0
							dy = -(bbox[3] * m22 - bbox[3]) + h * (m22 - 1.0) / 2.0
							snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping
			else:
				if control:
					m11 = (w + dx) / w
					m22 = (h + dy) / h
					dx = -(bbox[0] * m11 - bbox[0])
					dy = -(bbox[3] * m22 - bbox[3])
					#---- snapping
					point = middle_points[2]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = p_doc[0] - point[0]
						m11 = (w + dx) / w
						dx = -(bbox[0] * m11 - bbox[0])
						snap[0] = self.snap.active_snap[0]
					point = middle_points[3]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
					if f:
						dy = point[1] - p_doc[1]
						m22 = (h + dy) / h
						dy = -(bbox[3] * m22 - bbox[3])
						snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping
				else:
					if abs(dx) < abs(dy):
						m11 = m22 = (w + dx) / w
					else:
						m11 = m22 = (h + dy) / h
					dx = -(bbox[0] * m11 - bbox[0])
					dy = -(bbox[3] * m22 - bbox[3])
					#---- snapping
					point = middle_points[2]
					trafo = [m11, m21, m12, m22, dx, dy]
					p = libgeom.apply_trafo_to_point(point, trafo)
					f, p, p_doc = self.snap.snap_point(p, False, snap_y=False)
					if f:
						dx = p_doc[0] - point[0]
						m11 = m22 = (w + dx) / w
						dx = -(bbox[0] * m11 - bbox[0])
						dy = -(bbox[3] * m22 - bbox[3])
						snap[0] = self.snap.active_snap[0]
					else:
						point = middle_points[3]
						trafo = [m11, m21, m12, m22, dx, dy]
						p = libgeom.apply_trafo_to_point(point, trafo)
						f, p, p_doc = self.snap.snap_point(p, False, snap_x=False)
						if f:
							dy = point[1] - p_doc[1]
							m11 = m22 = (h + dy) / h
							dx = -(bbox[0] * m11 - bbox[0])
							dy = -(bbox[3] * m22 - bbox[3])
							snap[1] = self.snap.active_snap[1]
					self.snap.active_snap = snap
					#---- snapping

		if mark == 11:
			change_x = end_point[0] - start_point[0]
			m12 = change_x / h
			dx = -bbox[1] * m12
		if mark == 16:
			change_x = start_point[0] - end_point[0]
			m12 = change_x / h
			dx = -bbox[3] * m12
		if mark == 13:
			change_y = start_point[1] - end_point[1]
			m21 = change_y / w
			dy = -bbox[2] * m21
		if mark == 14:
			change_y = end_point[1] - start_point[1]
			m21 = change_y / w
			dy = -bbox[0] * m21

		if mark in (10, 12, 15, 17):
			x0, y0 = bbox[:2]
			shift_x, shift_y = self.selection.center_offset
			center_x = x0 + w / 2.0 + shift_x
			center_y = y0 + h / 2.0 + shift_y
			a1 = math.atan2(start_point[1] - center_y, start_point[0] - center_x)
			a2 = math.atan2(end_point[1] - center_y, end_point[0] - center_x)
			angle = a2 - a1
			if control:
				step = config.rotation_step * math.pi / 180.0
				angle = round(angle / step) * step
			m21 = math.sin(angle)
			m11 = m22 = math.cos(angle)
			m12 = -m21
			dx = center_x - m11 * center_x + m21 * center_y;
			dy = center_y - m21 * center_x - m11 * center_y;

		if not m11: m11 = .0000000001
		if not m22: m22 = .0000000001
		return [m11, m21, m12, m22, dx, dy]

	def _draw_frame(self, *args):
		if self.end:
			self.canvas.renderer.draw_move_frame(self.trafo)
			self.end = []
		return True

	def _draw_center(self, *args):
		if self.end:
			start = self.canvas.win_to_doc(self.start)
			end = self.canvas.win_to_doc(self.end)
			dx = end[0] - start[0]
			dy = end[1] - start[1]
			x, y = self.offset_start
			cp = libgeom.bbox_center(self.selection.bbox)
			f, win_p, doc_p = self.snap.snap_point([cp[0] + x + dx, cp[1] + y + dy], False)
			self.selection.center_offset = [doc_p[0] - cp[0], doc_p[1] - cp[1]]
			self.canvas.renderer.paint_selection()
		return True
