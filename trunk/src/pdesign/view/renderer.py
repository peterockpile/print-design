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

import cairo, math

from uc2 import uc2const
from uc2.formats.pdxf import model, const
from uc2.formats.pdxf.crenderer import CairoRenderer
from uc2 import libcairo

from pdesign import config

CAIRO_BLACK = [0.0, 0.0, 0.0]
CAIRO_GRAY = [0.5, 0.5, 0.5]
CAIRO_WHITE = [1.0, 1.0, 1.0]

class PDRenderer(CairoRenderer):

	direct_matrix = None

	canvas = None
	ctx = None
	win_ctx = None
	surface = None
	presenter = None

	width = 0
	height = 0

	def __init__(self, canvas):

		self.canvas = canvas
		self.direct_matrix = cairo.Matrix(1.0, 0.0, 0.0, 1.0, 0.0, 0.0)

	#-------DOCUMENT RENDERING

	def paint_document(self):
		self.presenter = self.canvas.presenter
		self.cms = self.presenter.cms
		self.win_ctx = self.canvas.window.cairo_create()
		self.start()
		if self.canvas.draw_page_border:
			self.paint_page_border()
		self.render_doc()
		self.render_grid()
		self.render_guides()
#		self.finalize()
		self.paint_selection()

	def start(self):
		width = int(self.canvas.width)
		height = int(self.canvas.height)
		if self.surface is None:
			self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
			self.width = width
			self.height = height
		elif self.width <> width or self.height <> height:
			self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
			self.width = width
			self.height = height
		self.ctx = cairo.Context(self.surface)
		self.ctx.set_source_rgb(*CAIRO_WHITE)
		self.ctx.paint()
		self.ctx.set_matrix(self.canvas.matrix)

	def finalize(self):
		self.win_ctx.set_source_surface(self.surface)
		self.win_ctx.paint()

	def paint_page_border(self):
		self.ctx.set_line_width(1.0 / self.canvas.zoom)
		offset = 5.0 / self.canvas.zoom
		w, h = self.canvas.presenter.get_page_size()
		self.ctx.rectangle(-w / 2.0 + offset, -h / 2.0 - offset, w, h)
		self.ctx.set_source_rgb(*CAIRO_GRAY)
		self.ctx.fill()
		self.ctx.set_antialias(cairo.ANTIALIAS_NONE)
		self.ctx.rectangle(-w / 2.0, -h / 2.0, w, h)
		self.ctx.set_source_rgb(*CAIRO_WHITE)
		self.ctx.fill()
		self.ctx.rectangle(-w / 2.0, -h / 2.0, w, h)
		self.ctx.set_source_rgb(*CAIRO_BLACK)
		self.ctx.stroke()

	def render_doc(self):
		if self.canvas.draft_view:
			self.antialias_flag = False
		else:
			self.antialias_flag = True

		if self.canvas.stroke_view:
			self.contour_flag = True
		else:
			self.contour_flag = False

		page = self.presenter.active_page
		for layer in page.childs:
			if self.canvas.stroke_view:
				self.stroke_style = deepcopy(layer.style)
				stroke = self.stroke_style[1]
				stroke[1] = 1.0 / self.canvas.zoom
			self.render(self.ctx, layer.childs)

	#------GRID RENDERING
	def render_guides(self):
		guides = []
		methods = self.presenter.methods
		guide_layer = methods.get_guide_layer()
		for child in guide_layer.childs:
			if child.cid == model.GUIDE:
				guides.append(child)
		if guides:
			self.ctx.set_matrix(self.direct_matrix)
			self.ctx.set_antialias(cairo.ANTIALIAS_NONE)
			self.ctx.set_line_width(1.0)
			self.ctx.set_dash(config.guide_line_dash)
			self.ctx.set_source_rgba(*guide_layer.color)
			for item in guides:
				if item.orientation == uc2const.HORIZONTAL:
					y_win = self.canvas.point_doc_to_win([0, item.position])[1]
					self.ctx.move_to(0, y_win)
					self.ctx.line_to(self.width, y_win)
					self.ctx.stroke()
				else:
					x_win = self.canvas.point_doc_to_win([item.position, 0])[0]
					self.ctx.move_to(x_win, 0)
					self.ctx.line_to(x_win, self.height)
					self.ctx.stroke()

	def render_grid(self):
		methods = self.presenter.methods
		grid_layer = methods.get_gird_layer()
		if methods.is_layer_visible(grid_layer):

			self.ctx.set_matrix(self.direct_matrix)
			self.ctx.set_antialias(cairo.ANTIALIAS_NONE)
			self.ctx.set_source_rgba(*grid_layer.color)
			self.ctx.set_line_width(1.0)

			w, h = self.presenter.get_page_size()
			x, y, dx, dy = grid_layer.grid
			origin = self.presenter.model.doc_origin
			if origin == const.DOC_ORIGIN_LL:
				x0, y0 = self.canvas.point_doc_to_win([-w / 2.0 + x, -h / 2.0 + y])
			elif origin == const.DOC_ORIGIN_LU:
				x0, y0 = self.canvas.point_doc_to_win([-w / 2.0 + x, h / 2.0 + y])
			else:
				x0, y0 = self.canvas.point_doc_to_win([x, y])
			dx = dx * self.canvas.zoom
			dy = dy * self.canvas.zoom
			sdist = config.snap_distance

			i = 0.0
			while dx < sdist + 3:
				i = i + 0.5
				dx = dx * 10.0 * i
			if dx / 2.0 > sdist + 3:
				dx = dx / 2.0

			i = 0.0
			while dy < sdist + 3:
				i = i + 0.5
				dy = dy * 10.0 * i
			if dy / 2.0 > sdist + 3:
				dy = dy / 2.0

			sx = (x0 / dx - math.floor(x0 / dx)) * dx
			sy = (y0 / dy - math.floor(y0 / dy)) * dy

			i = pos = 0
			while pos < self.width:
				pos = sx + i * dx
				i += 1
				self.ctx.move_to(pos, 0)
				self.ctx.line_to(pos, self.height)
				self.ctx.stroke()
			i = pos = 0
			while pos < self.height:
				pos = sy + i * dy
				i += 1
				self.ctx.move_to(0, pos)
				self.ctx.line_to(self.width, pos)
				self.ctx.stroke()
			self.ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)

	#------MARKER RENDERING

	def start_soft_repaint(self):
		self.win_ctx = self.canvas.window.cairo_create()
		self.temp_surface = cairo.ImageSurface(cairo.FORMAT_RGB24,
								int(self.canvas.width),
								int(self.canvas.height))
		self.ctx = cairo.Context(self.temp_surface)
		self.ctx.set_source_surface(self.surface)
		self.ctx.paint()

	def end_soft_repaint(self):
		self.win_ctx.set_source_surface(self.temp_surface)
		self.win_ctx.paint()

	def draw_frame(self, start, end):
		if start and end:
			path = libcairo.convert_bbox_to_cpath(start + end)
			self._draw_frame(path)

	def reflect_snap(self):
		if self.canvas.show_snapping:
			snap = self.presenter.snap.active_snap
			if not snap[0] is None or not snap[1] is None:
				self.ctx.set_matrix(self.direct_matrix)
				self.ctx.set_antialias(cairo.ANTIALIAS_NONE)
				self.ctx.set_line_width(1.0)
				self.ctx.set_dash(config.snap_line_dash)
				self.ctx.set_source_rgba(*config.snap_line_color)
				if not snap[0] is None:
					x_win = self.canvas.point_doc_to_win([snap[0], 0])[0]
					self.ctx.move_to(x_win, 0)
					self.ctx.line_to(x_win, self.height)
					self.ctx.stroke()
				if not snap[1] is None:
					y_win = self.canvas.point_doc_to_win([0, snap[1]])[1]
					self.ctx.move_to(0, y_win)
					self.ctx.line_to(self.width, y_win)
					self.ctx.stroke()
				self.presenter.snap.active_snap = [None, None]

	def paint_guide_dragging(self, point=[], orient=uc2const.HORIZONTAL):
		self.start_soft_repaint()
		self.ctx.set_matrix(self.direct_matrix)
		self.ctx.set_antialias(cairo.ANTIALIAS_NONE)
		self.ctx.set_line_width(1.0)
		self.ctx.set_dash(config.guide_line_dash)
		self.ctx.set_source_rgba(*config.guide_line_dragging_color)
		if point:
			if orient == uc2const.HORIZONTAL:
				y_win = self.canvas.point_doc_to_win(point)[1]
				self.ctx.move_to(0, y_win)
				self.ctx.line_to(self.width, y_win)
				self.ctx.stroke()
			else:
				x_win = self.canvas.point_doc_to_win(point)[0]
				self.ctx.move_to(x_win, 0)
				self.ctx.line_to(x_win, self.height)
				self.ctx.stroke()
			self.reflect_snap()
		self.end_soft_repaint()

	def _draw_frame(self, path):
		self.start_soft_repaint()
		self.reflect_snap()
		self.ctx.set_matrix(self.direct_matrix)
		self.ctx.set_antialias(cairo.ANTIALIAS_NONE)
		self.ctx.set_line_width(1.0)
		self.ctx.set_dash([])
		self.ctx.set_source_rgb(*CAIRO_WHITE)
		self.ctx.new_path()
		self.ctx.append_path(path)
		self.ctx.stroke()
		self.ctx.set_dash(config.sel_frame_dash)
		self.ctx.set_source_rgb(*config.sel_frame_color)
		self.ctx.new_path()
		self.ctx.append_path(path)
		self.ctx.stroke()

		self.end_soft_repaint()

	def _paint_selection(self):
		selection = self.presenter.selection
		if selection.objs:
			selection.update_markers()
			zoom = self.canvas.zoom
			self.ctx.set_matrix(self.canvas.matrix)
			self.ctx.set_antialias(cairo.ANTIALIAS_NONE)

			#Frame
			if config.sel_frame_visible:
				x0, y0, x1, y1 = selection.frame
				self.ctx.set_line_width(1.0 / zoom)
				if config.sel_marker_frame_bgcolor:
					self.ctx.set_dash([])
					self.ctx.set_source_rgb(*config.sel_marker_frame_bgcolor)
					self.ctx.rectangle(x0, y0, x1 - x0, y1 - y0)
					self.ctx.stroke()
				if config.sel_marker_frame_color:
					self.ctx.set_source_rgb(*config.sel_marker_frame_color)
					a, b = config.sel_marker_frame_dash
					self.ctx.set_dash([a / zoom, b / zoom])
					self.ctx.rectangle(x0, y0, x1 - x0, y1 - y0)
					self.ctx.stroke()

			if config.sel_bbox_visible:
				x0, y0, x1, y1 = selection.bbox
				self.ctx.set_line_width(1.0 / zoom)
				if config.sel_bbox_bgcolor:
					self.ctx.set_dash([])
					self.ctx.set_source_rgb(*config.sel_bbox_bgcolor)
					self.ctx.rectangle(x0, y0, x1 - x0, y1 - y0)
					self.ctx.stroke()
				if config.sel_bbox_color:
					self.ctx.set_source_rgb(*config.sel_bbox_color)
					a, b = config.sel_bbox_dash
					self.ctx.set_dash([a / zoom, b / zoom])
					self.ctx.rectangle(x0, y0, x1 - x0, y1 - y0)
					self.ctx.stroke()

			#Selection markers
			markers = selection.markers
			size = config.sel_marker_size / zoom
			i = 0
			for marker in markers:
				if i == 9:
					cs = 3.0 / (2.0 * zoom)
					self.ctx.set_source_rgb(*config.sel_marker_fill)
					self.ctx.rectangle(marker[0], marker[1] + size / 2.0 - cs,
									size, 2.0 * cs)
					self.ctx.rectangle(marker[0] + size / 2.0 - cs, marker[1],
									2.0 * cs, size)
					self.ctx.fill()
					self.ctx.set_source_rgb(*config.sel_marker_stroke)
					self.ctx.move_to(marker[0] + size / 2.0, marker[1])
					self.ctx.line_to(marker[0] + size / 2.0, marker[1] + size)
					self.ctx.stroke()
					self.ctx.move_to(marker[0], marker[1] + size / 2.0)
					self.ctx.line_to(marker[0] + size, marker[1] + size / 2.0)
					self.ctx.stroke()
				elif i in [0, 1, 2, 3, 5, 6, 7, 8]:
					self.ctx.set_source_rgb(*config.sel_marker_fill)
					self.ctx.rectangle(marker[0], marker[1], size, size)
					self.ctx.fill_preserve()
					self.ctx.set_source_rgb(*config.sel_marker_stroke)
					self.ctx.set_line_width(1.0 / zoom)
					self.ctx.set_dash([])
					self.ctx.stroke()
				i += 1

			#Object markers
			objs = selection.objs
			self.ctx.set_source_rgb(*config.sel_object_marker_color)
			self.ctx.set_line_width(1.0 / zoom)
			self.ctx.set_dash([])
			offset = 2.0 / zoom
			for obj in objs:
				bbox = obj.cache_bbox
				self.ctx.rectangle(bbox[0] - offset, bbox[1] - offset,
								 2.0 * offset, 2.0 * offset)
				self.ctx.stroke()

	def	paint_selection(self):
		self.start_soft_repaint()
		self._paint_selection()
		self.end_soft_repaint()

	def stop_draw_frame(self, start, end):
		self.start_soft_repaint()
		self.end_soft_repaint()

	def show_move_frame(self):
		bbox = self.presenter.selection.bbox
		if bbox:
			path = libcairo.convert_bbox_to_cpath(bbox)
			libcairo.apply_trafo(path, self.canvas.trafo)
			self._draw_frame(path)

	def draw_move_frame(self, trafo):
		bbox = self.presenter.selection.bbox
		if bbox:
			path = libcairo.convert_bbox_to_cpath(bbox)
			libcairo.apply_trafo(path, trafo)
			libcairo.apply_trafo(path, self.canvas.trafo)
			self._draw_frame(path)

	def hide_move_frame(self):
		self.start_soft_repaint()
		self._paint_selection()
		self.end_soft_repaint()

	#------DRAWING MARKER RENDERING

	def draw_curve_point(self, point, size, fill, stroke, stroke_width):
		if len(point) == 2:
			cx, cy = point
		else:
			cx, cy = point[2]
		x = cx - int(size / 2.0)
		y = cy - int(size / 2.0)
		self.ctx.move_to(x, y)
		self.ctx.set_antialias(cairo.ANTIALIAS_NONE)
		self.ctx.set_source_rgb(*fill)
		self.ctx.rectangle(x, y, size, size)
		self.ctx.fill()
		self.ctx.set_line_width(stroke_width)
		self.ctx.set_source_rgb(*stroke)
		self.ctx.rectangle(x, y, size, size)
		self.ctx.stroke()
		self.ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)

	def paint_curve(self, paths, cursor=[], trace_path=[], cpoint=[]):
		self.start_soft_repaint()
		if paths:
			for path in paths:
				self.ctx.set_source_rgb(*config.curve_stroke_color)
				self.ctx.set_line_width(config.curve_stroke_width)
				self.ctx.move_to(*path[0])
				points = path[1]
				for point in points:
					if len(point) == 2:
						self.ctx.line_to(*point)
					else:
						x0, y0 = point[0]
						x1, y1 = point[1]
						x2, y2 = point[2]
						self.ctx.curve_to(x0, y0, x1, y1, x2, y2)
				if path[2]:
					self.ctx.close_path()
				self.ctx.stroke()

				self.draw_curve_point(path[0],
						config.curve_start_point_size,
						config.curve_start_point_fill,
						config.curve_start_point_stroke,
						config.curve_start_point_stroke_width)
				for point in points:
					self.draw_curve_point(point,
							config.curve_point_size,
							config.curve_point_fill,
							config.curve_point_stroke,
							config.curve_point_stroke_width)
				if points:
						self.draw_curve_point(points[-1],
								config.curve_last_point_size,
								config.curve_last_point_fill,
								config.curve_last_point_stroke,
								config.curve_last_point_stroke_width)
		if cursor:
			self.ctx.set_source_rgb(*config.curve_trace_color)
			self.ctx.set_line_width(config.curve_stroke_width)
			if trace_path:
				self.ctx.move_to(*trace_path[0])
				point = trace_path[1]
				x0, y0 = point[0]
				x1, y1 = point[1]
				x2, y2 = point[2]
				self.ctx.curve_to(x0, y0, x1, y1, x2, y2)
				self.ctx.stroke()
				if cpoint:
					self.ctx.set_source_rgb(*config.control_line_stroke_color)
					self.ctx.set_line_width(config.control_line_stroke_width)
					self.ctx.set_dash(config.control_line_stroke_dash)
					self.ctx.move_to(*trace_path[0])
					self.ctx.line_to(x0, y0)
					self.ctx.stroke()
					self.ctx.move_to(x2, y2)
					self.ctx.line_to(x1, y1)
					self.ctx.stroke()
					self.ctx.move_to(x2, y2)
					self.ctx.line_to(*cpoint)
					self.ctx.stroke()
					self.ctx.set_dash([])
					for point in [[x0, y0], [x1, y1], cpoint]:
						self.draw_curve_point(point,
								config.control_point_size,
								config.control_point_fill,
								config.control_point_stroke,
								config.control_point_stroke_width)
					self.draw_curve_point([x2, y2],
							config.curve_point_size,
							config.curve_point_fill,
							config.curve_point_stroke,
							config.curve_point_stroke_width)
			else:
				if paths[-1][1]:
					end_point = paths[-1][1][-1]
					if len(end_point) == 2:
						self.ctx.move_to(*end_point)
					else:
						self.ctx.move_to(*end_point[2])
				else:
					self.ctx.move_to(*paths[-1][0])
				self.ctx.line_to(*cursor)
				self.ctx.stroke()

		self.end_soft_repaint()

