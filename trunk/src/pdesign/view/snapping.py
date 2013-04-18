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

import math

from uc2.formats.pdxf import const
from uc2 import libgeom

from pdesign import config
from pdesign.appconst import SNAP_TO_GRID, SNAP_TO_GUIDES, SNAP_TO_OBJECTS, SNAP_TO_PAGE

class SnapManager:

	presenter = None
	doc = None
	methods = None
	canvas = None

	active_snap = [None, None]

	snap_to_grid = config.snap_to_grid
	snap_to_guides = config.snap_to_guides
	snap_to_objects = config.snap_to_objects
	snap_to_page = config.snap_to_page
	snap_dict = {}
	snap_point_dict = {}

	snap_x = True
	snap_y = True

	grid_win = []
	grid_doc = []
	page_grid = []

	def __init__(self, presenter):

		self.active_snap = [None, None]

		self.presenter = presenter
		self.doc = self.presenter.doc_presenter
		self.methods = self.presenter.methods
		self.canvas = self.presenter.canvas
		self.snap_point_dict = {SNAP_TO_GRID:self.snap_point_to_grid,
						SNAP_TO_GUIDES:self.snap_point_to_guides,
						SNAP_TO_OBJECTS:self.snap_point_to_objects,
						SNAP_TO_PAGE:self.snap_point_to_page, }
		self.snap_bbox_dict = {SNAP_TO_GRID:self.snap_bbox_to_grid,
						SNAP_TO_GUIDES:self.snap_bbox_to_guides,
						SNAP_TO_OBJECTS:self.snap_bbox_to_objects,
						SNAP_TO_PAGE:self.snap_bbox_to_page, }
		el = self.presenter.eventloop
		el.connect(el.VIEW_CHANGED, self.update)
		el.connect(el.DOC_MODIFIED, self.update)
		el.connect(el.PAGE_CHANGED, self.update)

	def update(self, *args):
		self._calc_grid()
		self._calc_page_grid()

	def _calc_grid(self):
		grid_layer = self.methods.get_gird_layer()
		w, h = self.presenter.get_page_size()
		x, y, dx, dy = grid_layer.grid
		origin = self.presenter.model.doc_origin
		if origin == const.DOC_ORIGIN_LL:
			x0, y0 = self.canvas.point_doc_to_win([-w / 2.0 + x, -h / 2.0 + y])
			x0_doc, y0_doc = [-w / 2.0 + x, -h / 2.0 + y]
		elif origin == const.DOC_ORIGIN_LU:
			x0, y0 = self.canvas.point_doc_to_win([-w / 2.0 + x, h / 2.0 + y])
			x0_doc, y0_doc = [-w / 2.0 + x, h / 2.0 + y]
		else:
			x0, y0 = self.canvas.point_doc_to_win([x, y])
			x0_doc, y0_doc = [x, y]
		self.grid_doc = [x0_doc, y0_doc, dx, dy]
		dx = dx * self.canvas.zoom
		dy = dy * self.canvas.zoom
		sdist = config.snap_distance
		i = 0.0
		while dx < sdist + 3:
			i = i + 0.5
			dx = dx * 10.0 * i
			self.grid_doc[2] = self.grid_doc[2] * 10.0 * i
		if dx / 2.0 > sdist + 3:
			dx = dx / 2.0
			self.grid_doc[2] = self.grid_doc[2] / 2.0

		i = 0.0
		while dy < sdist + 3:
			i = i + 0.5
			dy = dy * 10.0 * i
			self.grid_doc[3] = self.grid_doc[3] * 10.0 * i
		if dy / 2.0 > sdist + 3:
			dy = dy / 2.0
			self.grid_doc[3] = self.grid_doc[3] / 2.0

		sx = (x0 / dx - math.floor(x0 / dx)) * dx
		sy = (y0 / dy - math.floor(y0 / dy)) * dy
		self.grid_win = [sx, sy, dx, dy]

	def _calc_page_grid(self):
		w, h = self.presenter.get_page_size()
		self.page_grid = [[-w / 2.0, 0, w / 2.0], [-h / 2.0, 0, h / 2.0]]

	#---------- Point snapping --------------------

	def snap_point(self, point, win_point=True, snap_x=True, snap_y=True):
		self.snap_dict = {SNAP_TO_GRID:self.snap_to_grid,
						SNAP_TO_GUIDES:self.snap_to_guides,
						SNAP_TO_OBJECTS:self.snap_to_objects,
						SNAP_TO_PAGE:self.snap_to_page, }
		flag = False
		self.snap_x = snap_x
		self.snap_y = snap_y
		self.active_snap = [None, None]

		if win_point:
			result = [] + point
			result_doc = self.canvas.point_win_to_doc(point)
		else:
			result = self.canvas.point_doc_to_win(point)
			result_doc = [] + point
		for item in config.snap_order:
			if self.snap_dict[item]:
				flag, p, p_doc = self.snap_point_dict[item](result, result_doc)
				if flag:
					result = p
					result_doc = p_doc
					break
		return flag, result, result_doc

	def snap_point_to_grid(self, point, doc_point):
		ret = False
		self.active_snap = [None, None]
		x = point[0]
		x_doc = doc_point[0]
		y = point[1]
		y_doc = doc_point[1]
		p = self.canvas.point_win_to_doc([x, y])

		if self.snap_x:
			val = round((point[0] - self.grid_win[0]) / self.grid_win[2])
			val = int(val * self.grid_win[2] + self.grid_win[0])
			if abs(val - point[0]) <= config.snap_distance:
				ret = True
				x = val
				x_doc = round((p[0] - self.grid_doc[0]) / self.grid_doc[2])
				x_doc = x_doc * self.grid_doc[2] + self.grid_doc[0]
				self.active_snap[0] = x_doc

		if self.snap_y:
			val = round((point[1] - self.grid_win[1]) / self.grid_win[3])
			val = int(val * self.grid_win[3] + self.grid_win[1])
			if abs(val - point[1]) <= config.snap_distance:
				ret = True
				y = val
				y_doc = round((p[1] - self.grid_doc[1]) / self.grid_doc[3])
				y_doc = y_doc * self.grid_doc[3] + self.grid_doc[1]
				self.active_snap[1] = y_doc

		return ret, [x, y], [x_doc, y_doc]

	def snap_point_to_guides(self, point, doc_point):
		return False, point, doc_point

	def snap_point_to_objects(self, point, doc_point):
		return False, point, doc_point

	def snap_point_to_page(self, point, doc_point):
		ret = False
		self.active_snap = [None, None]
		x = point[0]
		x_doc = doc_point[0]
		y = point[1]
		y_doc = doc_point[1]
		snap_dist = config.snap_distance / self.canvas.zoom

		if self.snap_x:
			for item in self.page_grid[0]:
				if abs(item - doc_point[0]) < snap_dist:
					ret = True
					x = self.canvas.point_doc_to_win([item, doc_point[1]])[0]
					x_doc = item
					self.active_snap[0] = x_doc
					break

		if self.snap_y:
			for item in self.page_grid[1]:
				if abs(item - doc_point[1]) < snap_dist:
					ret = True
					y = self.canvas.point_doc_to_win([doc_point[0], item])[1]
					y_doc = item
					self.active_snap[1] = y_doc
					break

		return ret, [x, y], [x_doc, y_doc]

	#---------- Bbox snapping --------------------

	def snap_bbox(self, bbox, trafo):
		if not trafo[1] == 0 or not trafo[2] == 0:
			return trafo
		result = [] + trafo

		points = libgeom.bbox_middle_points(bbox)
		tr_points = libgeom.apply_trafo_to_points(points, trafo)
		active_snap = [None, None]

		if trafo[0] == 1.0 and trafo[3] == 1.0:
			shift_x = []
			snap_x = []
			for point in [tr_points[0], tr_points[2], tr_points[1]]:
				flag, wp, dp = self.snap_point(point, False, snap_y=False)
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
				flag, wp, dp = self.snap_point(point, False, snap_x=False)
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

		elif trafo[0] == 1.0 and not trafo[3] == 1.0:
			pass
		elif not trafo[0] == 1.0 and trafo[3] == 1.0:
			pass

		else:
			pass

		self.active_snap = [] + active_snap

		return result

	def snap_bbox_to_grid(self, bbox, trafo):
		ret = False
		result = [] + trafo
		return ret, result

	def snap_bbox_to_guides(self, bbox, trafo):
		return False, trafo

	def snap_bbox_to_objects(self, bbox, trafo):
		return False, trafo

	def snap_bbox_to_page(self, bbox, trafo):
		return False, trafo
