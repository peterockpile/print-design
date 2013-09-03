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

from pdesign import _
from pdesign.resources import icons, get_bmp
from pdesign.widgets import const, ImageButton, LEFT, CENTER
from pdesign.pwidgets import AngleSpin
from generic import CtxPlugin

class RotatePlugin(CtxPlugin):

	name = 'RotatePlugin'

	def __init__(self, app, parent):
		CtxPlugin.__init__(self, app, parent)

	def build(self):
		bmp = get_bmp(self, icons.CTX_ROTATE, _('Rotate selection'))
		self.add(bmp, 0, LEFT | CENTER, 2)

		self.angle_spin = AngleSpin(self, onchange=self.apply_changes)
		self.add(self.angle_spin, 0, LEFT | CENTER, 2)

		self.add((2, 2))

		native = False
		if const.is_gtk():native = True

		rot_left = ImageButton(self, icons.CTX_ROTATE_LEFT,
							tooltip=_('Rotate left 90°'), native=native,
							onclick=self.rotate_left)
		self.add(rot_left, 0, LEFT | CENTER)

		rot_right = ImageButton(self, icons.CTX_ROTATE_RIGHT,
							tooltip=_('Rotate right 90°'), native=native,
							onclick=self.rotate_right)
		self.add(rot_right, 0, LEFT | CENTER)

	def rotate_left(self, *args):
		self.app.current_doc.api.rotate_selected(math.pi / 2.0)

	def rotate_right(self, *args):
		self.app.current_doc.api.rotate_selected(-math.pi / 2.0)

	def apply_changes(self, *args):
		val = self.angle_spin.get_angle_value()
		if val <> 0.0: self.app.current_doc.api.rotate_selected(val)

class MirrorPlugin(CtxPlugin):

	name = 'MirrorPlugin'

	def __init__(self, app, parent):
		CtxPlugin.__init__(self, app, parent)

	def build(self):

		native = False
		if const.is_gtk():native = True

		mh = ImageButton(self, icons.CTX_MIRROR_H,
							tooltip=_('Horizontal mirror'), native=native,
							onclick=self.mirror_h)
		self.add(mh, 0, LEFT | CENTER)

		mv = ImageButton(self, icons.CTX_MIRROR_V,
							tooltip=_('Vertical mirror'), native=native,
							onclick=self.mirror_v)
		self.add(mv, 0, LEFT | CENTER)

	def mirror_h(self, *args):
		self.app.current_doc.api.mirror_selected(False)

	def mirror_v(self, *args):
		self.app.current_doc.api.mirror_selected()


