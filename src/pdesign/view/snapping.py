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


class SnapManager:

	presenter = None
	doc = None
	methods = None

	snap_to_grid = False
	snap_to_guides = True
	snap_to_objects = False
	snap_to_page = False

	def __init__(self, presenter):

		self.presenter = presenter
		self.doc = self.presenter.doc_presenter
		self.methods = self.presenter.methods
		self.canvas = self.presenter.canvas

	def snap_point(self, point):pass

	def spap_bbox(self, bbox):pass

