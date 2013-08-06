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

import wx, cairo

from uc2.uc2const import mm_to_pt
from uc2.libcairo import normalize_bbox

from pdesign import events, modes, config
from pdesign.document.renderer import PDRenderer
from pdesign.document import controllers

PAGEFIT = 0.9
ZOOM_IN = 1.25
ZOOM_OUT = 0.8


WORKSPACE_HEIGHT = 2000 * mm_to_pt
WORKSPACE_WIDTH = 4000 * mm_to_pt

class AppCanvas(wx.Panel):

	presenter = None
	app = None
	eventloop = None
	renderer = None
	hscroll = None
	vscroll = None
	timer = None

	mode = None
	previous_mode = None
	controller = None
	ctrls = {}
	current_cursor = None

	workspace = (WORKSPACE_WIDTH, WORKSPACE_HEIGHT)
	matrix = None
	trafo = []
	zoom = 1.0
	width = 0
	height = 0
	orig_cursor = None
	current_cursor = None
	resize_marker = 0

	stroke_view = False
	draft_view = False
	soft_repaint = False
	full_repaint = False
	selection_repaint = True
	draw_page_border = True
	show_snapping = config.show_snap
	dragged_guide = ()

	my_changes = False

	def __init__(self, presenter, parent):
		self.presenter = presenter
		self.eventloop = self.presenter.eventloop
		self.app = presenter.app
		self.doc = self.presenter.model
		self.renderer = PDRenderer(self)
		wx.Panel.__init__(self, parent, style=wx.FULL_REPAINT_ON_RESIZE)
		self.SetBackgroundColour(wx.Colour(255, 255, 255))

		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self._on_timer)

		self.ctrls = self.init_controllers()
		self.SetDoubleBuffered(True)
		self.Bind(wx.EVT_PAINT, self.on_paint, self)
		#----- Mouse binding
		self.Bind(wx.EVT_LEFT_DOWN, self.mouse_left_down)
		self.Bind(wx.EVT_LEFT_UP, self.mouse_left_up)
		self.Bind(wx.EVT_LEFT_DCLICK, self.mouse_left_dclick)
		self.Bind(wx.EVT_RIGHT_DOWN, self.mouse_right_down)
		self.Bind(wx.EVT_RIGHT_UP, self.mouse_right_up)
		self.Bind(wx.EVT_MIDDLE_DOWN, self.mouse_middle_down)
		self.Bind(wx.EVT_MIDDLE_UP, self.mouse_middle_up)
		self.Bind(wx.EVT_MOUSEWHEEL, self.mouse_wheel)
		self.Bind(wx.EVT_MOTION, self.mouse_move)
		#-----
		self.eventloop.connect(self.eventloop.DOC_MODIFIED, self.doc_modified)
		self.eventloop.connect(self.eventloop.PAGE_CHANGED, self.doc_modified)
		self.eventloop.connect(self.eventloop.SELECTION_CHANGED,
							self.selection_redraw)

	#----- SCROLLING

	def _set_scrolls(self, hscroll, vscroll):
		self.hscroll = hscroll
		self.vscroll = vscroll
		self.hscroll.SetScrollbar(50, 10, 110, 10, refresh=True)
		self.vscroll.SetScrollbar(50, 10, 110, 10, refresh=True)
		self.hscroll.Bind(wx.EVT_SCROLL, self._scrolling, self.hscroll)
		self.vscroll.Bind(wx.EVT_SCROLL, self._scrolling, self.vscroll)

	def _scrolling(self, *args):
		if self.my_changes:return
		xpos = self.hscroll.GetThumbPosition() / 100.0
		ypos = (100 - self.vscroll.GetThumbPosition()) / 100.0
		x = (xpos - 0.5) * self.workspace[0]
		y = (ypos - 0.5) * self.workspace[1]
		center = self.doc_to_win((x, y))
		self._set_center(center)
		self.force_redraw()

	def update_scrolls(self):
		self.my_changes = True
		center = self._get_center()
		x = (center[0] + self.workspace[0] / 2.0) / self.workspace[0]
		y = (center[1] + self.workspace[1] / 2.0) / self.workspace[1]
		hscroll = int(100 * x)
		vscroll = int(100 - 100 * y)
		self.hscroll.SetScrollbar(hscroll, 10, 110, 10, refresh=True)
		self.vscroll.SetScrollbar(vscroll, 10, 110, 10, refresh=True)
		self.my_changes = False

	#----- CONTROLLERS

	def init_controllers(self):
		dummy = controllers.AbstractController(self, self.presenter)
		ctrls = {
		modes.SELECT_MODE: controllers.SelectController(self, self.presenter),
		modes.SHAPER_MODE: dummy,
		modes.ZOOM_MODE: controllers.ZoomController(self, self.presenter),
		modes.FLEUR_MODE:  controllers.FleurController(self, self.presenter),
		modes.TEMP_FLEUR_MODE: controllers.TempFleurController(self, self.presenter),
		modes.PICK_MODE: controllers.PickController(self, self.presenter),
		modes.LINE_MODE: dummy,
		modes.CURVE_MODE: dummy,
		modes.RECT_MODE: controllers.RectangleCreator(self, self.presenter),
		modes.ELLIPSE_MODE: controllers.EllipseCreator(self, self.presenter),
		modes.TEXT_MODE: dummy,
		modes.POLYGON_MODE: controllers.PolygonCreator(self, self.presenter),
		modes.MOVE_MODE: controllers.MoveController(self, self.presenter),
		modes.RESIZE_MODE: controllers.TransformController(self, self.presenter),
		modes.GUIDE_MODE: controllers.GuideController(self, self.presenter),
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

	def set_temp_mode(self, mode=modes.SELECT_MODE, callback=None):
		if not mode == self.mode:
			self.previous_mode = self.mode
			self.ctrls[self.mode].standby()
			self.mode = mode
			self.controller = self.ctrls[mode]
			self.controller.callback = callback
			self.controller.start_()
			self.controller.set_cursor()

	def restore_mode(self):
		if not self.previous_mode is None:
			if not self.controller is None:
				self.controller.stop_()
			self.mode = self.previous_mode
			self.controller = self.ctrls[self.mode]
			self.controller.set_cursor()
			self.controller.restore()
			events.emit(events.MODE_CHANGED, self.mode)
			self.previous_mode = None

	def set_temp_cursor(self, cursor):
		self.orig_cursor = self.app.cursors[self.mode]
		self.current_cursor = cursor
		self.SetCursor(cursor)

	def restore_cursor(self):
		if not self.orig_cursor is None:
			self.SetCursor(self.orig_cursor)
			self.current_cursor = self.orig_cursor
			self.orig_cursor = None

	#----- CANVAS MATH

	def _keep_center(self):
		w, h = self.GetSize()
		w = float(w)
		h = float(h)
		if not w == self.width or not h == self.height:
			_dx = (w - self.width) / 2.0
			_dy = (h - self.height) / 2.0
			m11, m12, m21, m22, dx, dy = self.trafo
			dx += _dx
			dy += _dy
			self.trafo = [m11, m12, m21, m22, dx, dy]
			self.matrix = cairo.Matrix(m11, m12, m21, m22, dx, dy)
			self.width = w
			self.height = h
			self.update_scrolls()

	def _set_center(self, center):
		x, y = center
		_dx = self.width / 2.0 - x
		_dy = self.height / 2.0 - y
		m11, m12, m21, m22, dx, dy = self.trafo
		dx += _dx
		dy += _dy
		self.trafo = [m11, m12, m21, m22, dx, dy]
		self.matrix = cairo.Matrix(m11, m12, m21, m22, dx, dy)
		self.update_scrolls()

	def _get_center(self):
		x = self.width / 2.0
		y = self.height / 2.0
		return self.win_to_doc((x, y))

	def doc_to_win(self, point=[0.0, 0.0]):
		x, y = point
		m11, m12, m21, m22, dx, dy = self.trafo
		x_new = m11 * x + dx
		y_new = m22 * y + dy
		return [x_new, y_new]

	def point_doc_to_win(self, point=[0.0, 0.0]):
		if not point:return []
		if len(point) == 2:
			return self.doc_to_win(point)
		else:
			return [self.doc_to_win(point[0]),
				self.doc_to_win(point[1]),
				self.doc_to_win(point[2]), point[3]]

	def win_to_doc(self, point=[0, 0]):
		x, y = point
		x = float(x)
		y = float(y)
		m11, m12, m21, m22, dx, dy = self.trafo
		x_new = (x - dx) / m11
		y_new = (y - dy) / m22
		return [x_new, y_new]

	def point_win_to_doc(self, point=[0.0, 0.0]):
		if not point:return []
		if len(point) == 2:
			return self.win_to_doc(point)
		else:
			return [self.win_to_doc(point[0]),
				self.win_to_doc(point[1]),
				self.win_to_doc(point[2]), point[3]]

	def paths_doc_to_win(self, paths):
		result = []
		for path in paths:
			new_path = []
			new_points = []
			new_path.append(self.doc_to_win(path[0]))
			for point in path[1]:
				new_points.append(self.point_doc_to_win(point))
			new_path.append(new_points)
			new_path.append(path[2])
			result.append(new_path)
		return result

	def scroll(self, cdx, cdy):
		m11, m12, m21, m22, dx, dy = self.trafo
		dx += cdx
		dy += cdy
		self.trafo = [m11, m12, m21, -m11, dx, dy]
		self.matrix = cairo.Matrix(*self.trafo)
		self.update_scrolls()
		self.force_redraw()

	#----- ZOOMING

	def _fit_to_page(self):
		width, height = self.presenter.get_page_size()
		w, h = self.GetSize()
		w = float(w)
		h = float(h)
		self.width = w
		self.height = h
		zoom = min(w / width, h / height) * PAGEFIT
		dx = w / 2.0
		dy = h / 2.0
		self.trafo = [zoom, 0, 0, -zoom, dx, dy]
		self.matrix = cairo.Matrix(zoom, 0, 0, -zoom, dx, dy)
		self.zoom = zoom
		self.update_scrolls()

	def zoom_fit_to_page(self):
		self._fit_to_page()
		self.force_redraw()

	def _zoom(self, dzoom=1.0):
		m11, m12, m21, m22, dx, dy = self.trafo
		m11 *= dzoom
		_dx = (self.width * dzoom - self.width) / 2.0
		_dy = (self.height * dzoom - self.height) / 2.0
		dx = dx * dzoom - _dx
		dy = dy * dzoom - _dy
		self.trafo = [m11, m12, m21, -m11, dx, dy]
		self.matrix = cairo.Matrix(*self.trafo)
		self.zoom = m11
		self.update_scrolls()
		self.force_redraw()

	def zoom_in(self):
		self._zoom(ZOOM_IN)

	def zoom_out(self):
		self._zoom(ZOOM_OUT)

	def zoom_100(self):
		self._zoom(1.0 / self.zoom)

	def zoom_at_point(self, point, zoom):
		self._set_center(point)
		self._zoom(zoom)

	def zoom_to_rectangle(self, start, end):
		w, h = self.GetSize()
		w = float(w)
		h = float(h)
		self.width = w
		self.height = h
		width = abs(end[0] - start[0])
		height = abs(end[1] - start[1])
		zoom = min(w / width, h / height) * 0.95
		center = [start[0] + (end[0] - start[0]) / 2,
				start[1] + (end[1] - start[1]) / 2]
		self._set_center(center)
		self._zoom(zoom)

	def zoom_selected(self):
		x0, y0, x1, y1 = self.presenter.selection.frame
		start = self.doc_to_win([x0, y0])
		end = self.doc_to_win([x1, y1])
		self.zoom_to_rectangle(start, end)

	#----- SELECTION STUFF

	def select_at_point(self, point, flag=False):
		point = self.win_to_doc(point)
		self.presenter.selection.select_at_point(point, flag)

	def pick_at_point(self, point):
		point = self.win_to_doc(point)
		return self.presenter.selection.pick_at_point(point)

	def select_by_rect(self, start, end, flag=False):
		start = self.win_to_doc(start)
		end = self.win_to_doc(end)
		rect = start + end
		rect = normalize_bbox(rect)
		self.presenter.selection.select_by_rect(rect, flag)

	#----- RENDERING -----
	def selection_redraw(self, *args):
		if not self.full_repaint:
			self.soft_repaint = True
		self.force_redraw()

	def doc_modified(self, *args):
		self.full_repaint = True
		self.force_redraw()

	def force_redraw(self, *args):
		w, h = self.GetSize()
		self.Refresh(rect=wx.Rect(0, 0, w, h))

	def on_paint(self, event):
		if self.matrix is None:
			self.zoom_fit_to_page()
			self.set_mode(modes.SELECT_MODE)
		self._keep_center()
		if self.soft_repaint and not self.full_repaint:
			if self.selection_repaint: self.renderer.paint_selection()
			self.soft_repaint = False
		else:
			self.renderer.paint_document()
			if self.selection_repaint: self.renderer.paint_selection()
			self.eventloop.emit(self.eventloop.VIEW_CHANGED)
			self.full_repaint = False
			self.soft_repaint = False
		if not self.controller is None: self.controller.repaint()
		if self.dragged_guide:
			self.renderer.paint_guide_dragging(*self.dragged_guide)
			if not self.mode == modes.GUIDE_MODE: self.dragged_guide = ()
		self.renderer.finalize()

	def destroy(self):
		if self.timer.IsRunning():self.timer.Stop()
		self.presenter = None
		self.app = None
		self.mode = None
		self.controller = None
		self.ctrls = {}
		self.current_cursor = None

#==============EVENT CONTROLLING==========================

	def _on_timer(self, event):
		self.controller.on_timer()

	def mouse_left_down(self, event):
		self.controller.set_cursor()
		self.controller.mouse_down(event)

	def mouse_left_up(self, event):
		self.controller.mouse_up(event)

	def mouse_left_dclick(self, event):
		self.controller.set_cursor()
		self.controller.mouse_double_click(event)

	def mouse_move(self, event):
		self.controller.mouse_move(event)

	def mouse_right_down(self, event):
		self.controller.mouse_right_down(event)

	def mouse_right_up(self, event):
		self.controller.mouse_right_up(event)

	def mouse_middle_down(self, event):
		self.controller.mouse_middle_down(event)

	def mouse_middle_up(self, event):
		self.controller.mouse_middle_up(event)

	def mouse_wheel(self, event):
		self.controller.wheel(event)


