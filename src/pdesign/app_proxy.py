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

class AppProxy:

	def __init__(self, app):
		self.app = app

	def update(self):
		self.insp = self.app.insp
		self.mw = self.app.mw

	def stub(self, *args):
		print 'event'

	def new(self, *args):
		self.app.new()

	def open(self, *args):
		self.app.open()

	def close(self, *args):
		self.app.close()

	def exit(self, *args):pass

	def set_mode(self, mode):
		self.app.current_doc.canvas.set_mode(mode)

	def open_url(self, url):
		self.app.open_url(url)
