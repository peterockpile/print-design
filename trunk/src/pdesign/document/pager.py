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

from pdesign.widgets import VPanel

class DocPager(VPanel):

	presenter = None

	def __init__(self, presenter, parent):
		self.presenter = presenter
		VPanel.__init__(self, parent)
		self.add((100, 20))

	def destroy(self):
		self.Destroy()
		fields = self.__dict__
		items = fields.keys()
		for item in items:
			fields[item] = None
