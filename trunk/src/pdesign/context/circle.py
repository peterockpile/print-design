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

import wx

from uc2.formats.pdxf.const import ARC_ARC, ARC_CHORD, ARC_PIE_SLICE

from pdesign import _, events
from pdesign.resources import icons
from pdesign.widgets import const, LEFT, CENTER, VPanel
from pdesign.widgets import ImageToggleButton, Slider
from pdesign.pwidgets import BitmapToggle
from pdesign.pwidgets import AngleSpin
from generic import CtxPlugin

class CirclePlugin(CtxPlugin):

	name = 'CirclePlugin'
	update_flag = False
	circle_type = ARC_CHORD
	start = 0
	end = 0
	toggles = {}

	def __init__(self, app, parent):
		CtxPlugin.__init__(self, app, parent)
		events.connect(events.DOC_CHANGED, self.update)
		events.connect(events.SELECTION_CHANGED, self.update)

	def build(self):
		native = True
		if const.is_msw():native = False

		self.toggles[ARC_ARC] = ImageToggleButton(self, False,
								icons.CTX_CIRCLE_ARC,
								onchange=self.toggled, native=native,
								tooltip=_('Arc'))
		self.add(self.toggles[ARC_ARC], 0, LEFT | CENTER)

		self.toggles[ARC_CHORD] = ImageToggleButton(self, False,
								icons.CTX_CIRCLE_CHORD,
								onchange=self.toggled, native=native,
								tooltip=_('Chord'))
		self.add(self.toggles[ARC_CHORD], 0, LEFT | CENTER)

		self.toggles[ARC_PIE_SLICE] = ImageToggleButton(self, False,
								icons.CTX_CIRCLE_PIE_SLICE,
								onchange=self.toggled, native=native,
								tooltip=_('Pie slice'))
		self.add(self.toggles[ARC_PIE_SLICE], 0, LEFT | CENTER)

		self.slider = Slider(self, 0, (0, 360), onchange=self.slider_changes)
		self.add(self.slider, 0, LEFT | CENTER, 2)

		self.angle_spin = AngleSpin(self, onchange=self.angle_changes)
		self.add(self.angle_spin, 0, LEFT | CENTER, 2)

		txt1 = _('Start angle')
		txt2 = _('End angle')
		icons_dict = {True:[icons.CTX_CIRCLE_START_ANGLE, txt1, ],
				False:[icons.CTX_CIRCLE_END_ANGLE, txt2, ], }
		self.switch = BitmapToggle(self, True, icons_dict, self.switched)
		self.add(self.switch, 0, LEFT | CENTER, 2)

	def update(self, *args):
		if self.insp.is_selection():
			sel = self.app.current_doc.selection
			if len(sel.objs) == 1 and self.insp.is_obj_circle(sel.objs[0]):
				obj = sel.objs[0]


	def toggled(self, *args):pass
	def switched(self, *args):pass
	def angle_changes(self, *args):pass
	def slider_changes(self, *args):pass


