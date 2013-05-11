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

import gtk, cairo

from uc2 import uc2const
from uc2.uc2const import point_dict
from uc2.formats.pdxf.const import FILL_SOLID
from pdesign import _, events, config

FILL_SWATCH = 0
OUTLINE_SWATCH = 1

class ColorMonitorWidget(gtk.HBox):

	start = None
	left = None
	label = None
	right = None
	end = None

	def __init__(self, app):

		gtk.HBox.__init__(self)
		self.app = app
		self.insp = app.inspector

		self.set_border_width(2)

		self.fill_label = FillLabel(self.app)
		self.pack_start(self.fill_label, False, False, 5)

		self.fill_swatch = ColorSwatch(self.app, FILL_SWATCH)
		self.pack_start(self.fill_swatch, False, False, 0)

		self.outline_label = OutlineLabel(self.app)
		self.pack_start(self.outline_label, False, False, 5)

		self.outline_swatch = ColorSwatch(self.app, OUTLINE_SWATCH)
		self.pack_start(self.outline_swatch, False, False, 0)

		events.connect(events.NO_DOCS, self.update)
		events.connect(events.DOC_CHANGED, self.update)
		events.connect(events.SELECTION_CHANGED, self.update)
		events.connect(events.DOC_MODIFIED, self.update)

	def update(self, *args):
		if not self.insp.is_doc():
			self.set_visible(False)
			return

		if not self.insp.is_selection():
			self.set_visible(False)
			return

		doc = self.app.current_doc
		sel = doc.selection.objs

		if not len(sel) == 1:
			self.set_visible(False)
			return

		obj = sel[0]

		if not self.insp.is_obj_primitive(obj):
			self.set_visible(False)
			return

		self.set_visible(True)
		self.fill_label.update_from_obj(obj)
		self.fill_swatch.update_from_obj(obj)
		self.outline_label.update_from_obj(obj)
		self.outline_swatch.update_from_obj(obj)


class FillLabel(gtk.Label):

	colorspace = None
	color = []
	alpha = 1.0
	color_name = ''
	non_solid = False

	def __init__(self, app):
		gtk.Label.__init__(self)

	def update_from_obj(self, obj):
		fill = obj.style[0]
		if fill:
			if fill[1] == FILL_SOLID:
				self.non_solid = False
				self.colorspace = fill[2][0]
				self.color = [] + fill[2][1]
				self.alpha = fill[2][2]
				self.color_name = '' + fill[2][3]
			else:
				self.non_solid = True
		else:
			self.colorspace = None
			self.color = []
			self.alpha = 1.0
			self.color_name = ''
			self.non_solid = False
		self.update_val()

	def update_val(self):
		text = _('Fill:')
		if self.non_solid:
			pass
		elif self.colorspace is None:
			text += ' ' + _('None')
		else:
			if self.colorspace == uc2const.COLOR_CMYK:
				c, m, y, k = self.color
				text += ' C-%d%% M-%d%% Y-%d%% K-%d%%' % (c * 100, m * 100,
														 y * 100, k * 100)
			elif self.colorspace == uc2const.COLOR_RGB:
				r, g, b = self.color
				text += ' R-%d G-%d B-%d' % (r * 255, g * 255, b * 255)
			elif self.colorspace == uc2const.COLOR_LAB:
				l, a, b = self.color
				text += ' L-%d a-%d b-%d' % (l * 255, a * 255, b * 255)
			elif self.colorspace == uc2const.COLOR_GRAY:
				gray, = self.color
				text += ' gray-%d' % (gray * 255)
			elif self.colorspace == uc2const.COLOR_SPOT:
				text += ' %s' % (self.color_name)
			else:
				pass

			if self.alpha < 1.0:
				if self.colorspace == uc2const.COLOR_CMYK:
					alpha = int(round(self.alpha * 100))
					text += ' A-%d%%' % (alpha)
				else:
					alpha = int(round(self.alpha * 255))
					text += ' A-%d' % (alpha)

		self.set_text(text)

class OutlineLabel(gtk.Label):

	point_val = 0

	def __init__(self, app):
		gtk.Label.__init__(self)
		events.connect(events.CONFIG_MODIFIED, self.update_label)

	def update_label(self, *args):
		if args[0][0] == 'default_unit':
			self.update_val()

	def update_from_obj(self, obj):
		stroke = obj.style[1]
		if stroke:
			self.point_val = stroke[1]
		else:
			self.point_val = 0
		self.update_val()

	def update_val(self):
		text = _('Outline:')
		if self.point_val:
			val = str(round(self.point_val * point_dict[config.default_unit], 3))
			text += (' %s ') % (val)
			text += config.default_unit
		else:
			text += ' ' + _('None')
		self.set_text(text)


WHITE = [1, 1, 1]
BLACK = [0, 0, 0]
GRAY = [0.878, 0.878, 0.878]

class ColorSwatch(gtk.DrawingArea):

	ctx = None
	app = None
	insp = None
	cms = None

	width = 40
	height = 16
	color = []
	non_solid = False

	def __init__(self, app, mode):
		gtk.DrawingArea.__init__(self)

		self.app = app
		self.insp = app.inspector
		self.mode = mode
		self.set_size_request(self.width, self.height)
#		self.nofill_color = self.mw.get_style().fg[gtk.STATE_NORMAL]
#		self.modify_bg(gtk.STATE_NORMAL, self.nodocs_color)
		self.connect('expose_event', self.repaint)

	def update_from_obj(self, obj):
		if self.mode == FILL_SWATCH:
			fill = obj.style[0]
			if fill:
				if fill[1] == FILL_SOLID:
					self.non_solid = False
					self.color = fill[2]
				else:
					self.non_solid = True
			else:
				self.color = []
				self.non_solid = False
		else:
			stroke = obj.style[1]
			self.non_solid = False
			if stroke:
				self.color = stroke[2]
			else:
				self.color = []
		self.repaint()

	def repaint(self, *args):
		self.ctx = self.window.cairo_create()
		if self.insp.is_doc():
			self.cms = self.app.current_doc.cms
		else:
			self.cms = self.app.default_cms
		self.draw_white_bg()
		if self.non_solid:
			#TODO: implement gradient and tiled fill
			pass
		else:
			if self.color:
				self.draw_solid_color()
			else:
				self.draw_no_color()
		self.draw_black_border()

	def draw_white_bg(self):
		self.ctx.set_source_rgb(*WHITE)
		self.ctx.rectangle(0, 0, self.width, self.height)
		self.ctx.fill()

	def draw_transparency_bg(self):
		self.ctx.set_antialias(cairo.ANTIALIAS_NONE)
		self.ctx.set_source_rgb(*GRAY)
		size = self.height / 2
		for item in range(3):
			shift = 2 * item * size + self.width / 2
			self.ctx.rectangle(shift, 0, size, size)
			self.ctx.fill()
		for item in range(3):
			shift = 2 * item * size + size + self.width / 2
			self.ctx.rectangle(shift, size, size, size)
			self.ctx.fill()
		self.ctx.move_to(self.width / 2, 0)
		self.ctx.set_line_width(1)
		self.ctx.line_to(self.width / 2, self.height)
		self.ctx.stroke()
		self.ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)


	def draw_solid_color(self):
		if not self.color: return
		if self.color[2] < 1.0:
			self.draw_transparency_bg()
		r, g, b = self.cms.get_display_color(self.color)
		self.ctx.set_source_rgba(r, g, b, self.color[2])
		self.ctx.rectangle(0, 0, self.width, self.height)
		self.ctx.fill()

	def draw_black_border(self):
		self.ctx.set_source_rgb(*BLACK)
		self.ctx.set_line_width(1)
		self.ctx.set_antialias(cairo.ANTIALIAS_NONE)
		self.ctx.rectangle(0, 0, self.width - 1, self.height - 1)
		self.ctx.stroke()
		self.ctx.set_antialias(cairo.ANTIALIAS_DEFAULT)

	def draw_no_color(self):
		self.ctx.set_source_rgb(*BLACK)
		self.ctx.set_line_width(1)
		self.ctx.move_to(-1, 0)
		self.ctx.line_to(self.width - 1, self.height - 1)
		self.ctx.move_to(0, self.height - 1)
		self.ctx.line_to(self.width - 1, 1)
		self.ctx.stroke()

