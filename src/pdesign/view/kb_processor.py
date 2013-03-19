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

import gtk

from pdesign import modes

KEY_UP = 65362
KEY_DOWN = 65364
KEY_LEFT = 65361
KEY_RIGHT = 65363
KEY_KP_UP = 65431
KEY_KP_DOWN = 65433
KEY_KP_LEFT = 65430
KEY_KP_RIGHT = 65432
KEY_ESCAPE = 65307

class KeyboardProcessor:

	def __init__(self, app, canvas):
		self.app = app
		self.insp = app.inspector
		self.proxy = app.proxy
		self.canvas = canvas

	def check_keypress(self, keyval):

#		keyname = gtk.gdk.keyval_name(keyval)
#		print "Key %s (%d) was pressed" % (keyname, keyval)

		if self.canvas.mode == modes.SELECT_MODE:
			return self.select_mode(keyval)
		if self.canvas.mode == modes.LINE_MODE:
			return self.line_mode(keyval)
		elif self.canvas.mode == modes.RECT_MODE:
			return self.rect_mode(keyval)
		elif self.canvas.mode == modes.ELLIPSE_MODE:
			return self.ellipse_mode(keyval)
		elif self.canvas.mode == modes.POLYGON_MODE:
			return self.rect_mode(keyval)

		return False

	#=========MODES================

	def select_mode(self, keyval):
		if self.check_moving(keyval): return True
		return False

	def line_mode(self, keyval):
		if self.check_moving(keyval): return True
		if self.check_escape(keyval): return True
		return False

	def rect_mode(self, keyval):
		if self.check_moving(keyval): return True
		if self.check_escape(keyval): return True
		return False

	def ellipse_mode(self, keyval):
		if self.check_moving(keyval): return True
		if self.check_escape(keyval): return True
		return False

	def polygon_mode(self, keyval):
		if self.check_moving(keyval): return True
		if self.check_escape(keyval): return True
		return False

	#=========ACTIONS================

	def check_escape(self, keyval):
		if keyval == KEY_ESCAPE:
			self.canvas.set_mode(modes.SELECT_MODE)
			return True
		return False

	def check_moving(self, keyval):
		if keyval in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT,
					KEY_KP_UP, KEY_KP_DOWN, KEY_KP_LEFT, KEY_KP_RIGHT]:
			if keyval in [KEY_RIGHT, KEY_KP_RIGHT]:
				self.proxy.move_right()
			elif keyval in [KEY_LEFT, KEY_KP_LEFT]:
				self.proxy.move_left()
			elif keyval in [KEY_UP, KEY_KP_UP]:
				self.proxy.move_up()
			elif keyval in [KEY_DOWN, KEY_KP_DOWN]:
				self.proxy.move_down()
			return True
		return False

