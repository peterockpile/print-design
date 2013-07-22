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
#
#   MacOS X env: export VERSIONER_PYTHON_PREFER_32_BIT=yes

import wx, const

from generic import Widget, DataWidget, RangeDataWidget
from const import FONT_SIZE, DEF_SIZE


class Application(wx.App):

	app_name = None

	mw = None
	mdi = None
	actions = []

	def __init__(self, name='', redirect=False):
		wx.App.__init__(self, redirect=redirect)
		if name:self.set_app_name(name)
		const.set_ui_colors(const.UI_COLORS)
		self._set_font_size()

	def _set_font_size(self):
		dc = wx.MemoryDC()
		dc.SetFont(wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT))
		FONT_SIZE[0] = dc.GetTextExtent('D')[0]
		FONT_SIZE[1] = dc.GetCharHeight()

	def set_app_name(self, name):
		self.app_name = name
		self.SetAppName(name)

	def update_actions(self):
		for item in self.actions.keys():
			self.actions[item].update()

	def call_after(self, *args):pass

	def run(self):
		if self.mw:
			self.SetTopWindow(self.mw)
			self.mw.build()
			self.mw.Show(True)
			self.mdi = self.mw.mdi
			if self.actions:self.update_actions()
			wx.CallAfter(self.call_after)
			self.MainLoop()
		else:
			raise RuntimeError, 'Main window is not defined!'

class MainWindow(wx.Frame):

	mdi = None

	def __init__(self, title='Frame', size=(100, 100), orientation=wx.VERTICAL):

		wx.Frame.__init__(self, None, wx.ID_ANY, title, pos=DEF_SIZE, size=size)
		self.Centre()
		self.box = wx.BoxSizer(orientation)
		self.SetSizer(self.box)
		self.set_title(title)

	def build(self):pass

	def add(self, *args, **kw):
		"""Arguments: object, expandable (0 or 1), flag, border"""
		self.box.Add(*args, **kw)

	def set_title(self, title):
		self.SetTitle(title)

	def set_minsize(self, w, h):
		self.SetMinSize((w, h))

class Panel(wx.Panel, Widget):

	def __init__(self, parent):
		wx.Panel.__init__(self, parent, wx.ID_ANY)

	def set_bg(self, color):
		self.SetBackgroundColour(wx.Colour(*color))

class SizedPanel(Panel):

	panel = None

	def __init__(self, parent, orientation=wx.HORIZONTAL):
		self.parent = parent
		self.orientation = orientation
		Panel.__init__(self, parent)
		self.box = wx.BoxSizer(orientation)
		self.SetSizer(self.box)
		self.panel = self

	def add(self, *args, **kw):
		"""Arguments: object, expandable (0 or 1), flag, border"""
		obj = args[0]
		if not isinstance(obj, tuple):
			if not obj.GetParent() == self.panel:
				obj.Reparent(self.panel)
		self.box.Add(*args, **kw)

	def box_add(self, *args, **kw):
		"""Arguments: object, expandable (0 or 1), flag, border"""
		self.box.Add(*args, **kw)

	def remove(self, obj):
		self.box.Remove(obj)


class BorderedPanel(SizedPanel):
	def __init__(self, parent, orientation=wx.HORIZONTAL, border=None, space=0):
		if border is None:
			if orientation == wx.HORIZONTAL:
				inner_orientation = wx.VERTICAL
			else:
				inner_orientation = wx.HORIZONTAL
		else:
			if orientation == wx.HORIZONTAL:
				inner_orientation = wx.HORIZONTAL
				orientation = wx.VERTICAL
			else:
				inner_orientation = wx.VERTICAL
				orientation = wx.HORIZONTAL
		SizedPanel.__init__(self, parent, orientation)
		if not border is None:
			self.inner_box = self.box
			if border in (wx.BOTH, wx.TOP, wx.LEFT):
				line = wx.StaticLine(self, style=inner_orientation)
				self.add(line, 0, wx.ALL | wx.EXPAND)
			panel = SizedPanel(self, inner_orientation)
			self.add(panel, 1, wx.ALL | wx.EXPAND, space)
			if border in (wx.BOTH, wx.BOTTOM, wx.RIGHT):
				line = wx.StaticLine(self, style=inner_orientation)
				self.add(line, 0, wx.ALL | wx.EXPAND)
			self.box = panel.box
			self.panel = panel


class HPanel(BorderedPanel):
	def __init__(self, parent, border=None, space=0):
		BorderedPanel.__init__(self, parent, wx.HORIZONTAL, border, space)


class VPanel(BorderedPanel):
	def __init__(self, parent, border=None, space=0):
		BorderedPanel.__init__(self, parent, wx.VERTICAL, border, space)


class LabeledPanel(wx.StaticBox, Widget):

	sizer = None

	def __init__(self, parent, text='', size=DEF_SIZE,
				 orientation=wx.HORIZONTAL):
		wx.StaticBox.__init__(self, parent, wx.ID_ANY, text,
							pos=DEF_SIZE, size=size)
		self.box = wx.StaticBoxSizer(self, orientation)

	def add(self, *args, **kw):
		"""Arguments: object, expandable (0 or 1), flag, border"""
		self.box.Add(*args, **kw)

class Notebook(wx.Notebook, Widget):

	childs = []

	def __init__(self, parent):
		self.childs = []
		wx.Notebook.__init__(self, parent, wx.ID_ANY)

	def add_page(self, page, title):
		self.childs.append(page)
		self.AddPage(page, title)

	def remove_page(self, page):
		index = self.childs.index(page)
		self.childs.remove(page)
		self.RemovePage(index)


class VLine(wx.StaticLine):
	def __init__(self, parent):
		wx.StaticLine.__init__(self, parent, style=wx.VERTICAL)


class HLine(wx.StaticLine):
	def __init__(self, parent):
		wx.StaticLine.__init__(self, parent, style=wx.HORIZONTAL)


class Label(wx.StaticText, Widget):

	def __init__(self, parent, text='', fontbold=False, fontsize=0, fg=()):
		wx.StaticText.__init__(self, parent, wx.ID_ANY, text)
		font = self.GetFont()
		if fontbold:
			font.SetWeight(wx.FONTWEIGHT_BOLD)
		if fontsize:
			if font.IsUsingSizeInPixels():
				sz = font.GetPixelSize()[1] + fontsize
				font.SetPixelSize((0, sz))
			else:
				sz = font.GetPointSize() + fontsize
				font.SetPointSize(sz)
		self.SetFont(font)
		if fg:
			self.SetForegroundColour(wx.Colour(*fg))

	def set_text(self, txt):
		self.SetLabel(txt)


class HtmlLabel(wx.HyperlinkCtrl, Widget):
	def __init__(self, parent, text, url=''):
		if not url:url = text
		wx.HyperlinkCtrl.__init__(self, parent, wx.ID_ANY, text, url)


class Button(wx.Button, Widget):

	def __init__(self, parent, text, size=DEF_SIZE,
				onclick=None, tooltip='', default=False):
		wx.Button.__init__(self, parent, wx.ID_ANY, text, size=size)
		if default: self.SetDefault()
		if onclick: self.Bind(wx.EVT_BUTTON, onclick, self)
		if tooltip: self.SetToolTipString(tooltip)


class Checkbox(wx.CheckBox, DataWidget):

	def __init__(self, parent, text='', value=False, onclick=None, right=False):
		style = 0
		if right:style = wx.ALIGN_RIGHT
		wx.CheckBox.__init__(self, parent, wx.ID_ANY, text, style=style)
		if value: self.SetValue(value)
		if onclick:self.Bind(wx.EVT_CHECKBOX, onclick, self)


class Radiobutton(wx.RadioButton, DataWidget):
	def __init__(self, parent, text='', onclick=None, group=False):
		style = 0
		if group:style = wx.RB_GROUP
		wx.RadioButton.__init__(self, parent, wx.ID_ANY, text, style=style)
		if onclick:self.Bind(wx.wx.EVT_RADIOBUTTON, onclick, self)


class Combolist(wx.Choice, Widget):

	items = []

	def __init__(self, parent, size=DEF_SIZE, width=0, items=[], onchange=None):
		self.items = []
		if items: self.items = items
		size = self._set_width(size, width)
		wx.Choice.__init__(self, parent, wx.ID_ANY, size, choices=self.items)
		if onchange:self.Bind(wx.EVT_CHOICE, onchange, self)

	def set_items(self, items):
		self.SetItems(items)

	def set_selection(self, index):
		if index < self.GetCount(): self.SetSelection(index)

	def get_selection(self):
		return self.GetSelection()


class Combobox(wx.ComboBox, DataWidget):

	items = []

	def __init__(self, parent, value='', pos=(-1, 1), size=DEF_SIZE, width=0,
				items=[], onchange=None):
		self.items = []
		if items: self.items = items
		flags = wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER
		size = self._set_width(size, width)
		wx.ComboBox.__init__(self, parent, wx.ID_ANY, value, pos, size, items, flags)
		if onchange:
			self.Bind(wx.EVT_COMBOBOX, onchange, self)
			self.Bind(wx.EVT_TEXT_ENTER, onchange, self)

	def set_items(self, items):
		self.SetItems(items)

class Entry(wx.TextCtrl, DataWidget):

	def __init__(self, parent, value='', size=DEF_SIZE, width=0, onchange=None,
				multiline=False, richtext=False, onenter=None):
		style = 0
		if multiline: style |= wx.TE_MULTILINE
		if richtext: style |= wx.TE_RICH2
		if onenter: style |= wx.TE_PROCESS_ENTER
		size = self._set_width(size, width)
		wx.TextCtrl.__init__(self, parent, wx.ID_ANY, value, size=size, style=style)
		if onchange: self.Bind(wx.EVT_TEXT, onchange, self)
		if onenter: self.Bind(wx.EVT_TEXT_ENTER, onenter, self)


class Spin(wx.SpinCtrl, RangeDataWidget):

	def __init__(self, parent, value=0, range_val=(0, 1), size=DEF_SIZE, width=0,
				 onchange=None):
		self.range_val = range_val
		size = self._set_width(size, width)
		wx.SpinCtrl.__init__(self, parent, wx.ID_ANY, '', size)
		self.SetRange(*range_val)
		self.SetValue(value)
		if onchange:
			self.Bind(wx.EVT_SPINCTRL, onchange, self)

class SpinButton(wx.SpinButton, RangeDataWidget):

	def __init__(self, parent, value=0, range_val=(0, 10), size=DEF_SIZE,
				 onchange=None, vertical=True):
		self.range_val = range_val
		style = wx.SL_VERTICAL
		if not vertical:style = wx.SL_HORIZONTAL
		wx.SpinButton.__init__(self, parent, wx.ID_ANY, size=size, style=style)
		self.SetValue(value)
		self.SetRange(*range_val)
		if onchange:
			self.Bind(wx.EVT_SPIN, onchange, self)

class FloatSpin(SizedPanel, RangeDataWidget):

	flag = True
	value = 0.0
	range_val = (0.0, 1.0)
	step = 0.01
	digits = 2
	callback = None

	def __init__(self, parent, value=0.0, range_val=(0.0, 1.0), step=0.01,
				digits=2, size=DEF_SIZE, width=0, onchange=None):

		self.callback = onchange

		SizedPanel.__init__(self, parent)
		self.entry = Entry(self.panel, '', size=size, width=width,
						onchange=self._check_entry,
						onenter=self._entry_enter)
		self.add(self.entry, 0, wx.ALL)
		size = (-1, self.entry.GetSize()[1])
		self.sb = SpinButton(self.parent, size=size, onchange=self._check_spin)
		self.add(self.sb, 0, wx.ALL)

		self.set_step(step)
		self.set_range(range_val)
		self._set_digits(digits)
		self._set_value(value)
		self.flag = False

	def _check_spin(self, event):
		if self.flag:return
		coef = pow(10, self.digits)
		dval = float(self.sb.get_value() - int(self.value * coef))
		if not self.value == self._calc_entry():
			self._set_value(self._calc_entry())
		self.SetValue(dval * self.step + self.value)

	def _entry_enter(self, event):
		if self.flag:return
		self.SetValue(self._calc_entry())

	def _check_entry(self, event):
		if self.flag:return
		txt = self.entry.get_value()
		res = ''
		for item in txt:
			if item in '.0123456789-+/*':
				res += item
		if not txt == res:
			self.flag = True
			self.entry.set_value(res)
			self.flag = False

	def _calc_entry(self):
		txt = self.entry.get_value()
		val = 0
		try:
			line = 'val=' + txt
			code = compile(line, '<string>', 'exec')
			exec code
		except:return self.value
		return val

	def _check_in_range(self, val):
		minval, maxval = self.range_val
		if val < minval:val = minval
		if val > maxval:val = maxval
		coef = pow(10, self.digits)
		val = round(val * coef) / coef
		return val

	def _set_value(self, val):
		coef = pow(10, self.digits)
		self.value = self._check_in_range(val)
		self.entry.set_value(str(self.value))
		self.sb.set_value(int(self.value * coef))

	def _set_digits(self, digits):
		self.digits = digits
		self.set_range(self.range_val)

	#----- Native API emulation
	def SetValue(self, val):
		self.flag = True
		self._set_value(val)
		self.flag = False
		self.callback(None)

	def GetValue(self):
		if not self.value == self._calc_entry():
			self._set_value(self._calc_entry())
		return self.value

	def SetRange(self, minval, maxval):
		coef = pow(10, self.digits)
		self.range_val = (minval, maxval)
		self.sb.set_range((int(minval * coef), int(maxval * coef)))

	#----- Control API
	def set_step(self, step):
		self.step = step

	def set_digits(self, digits):
		self._set_digits(digits)
		self.SetValue(self.value)

class Slider(wx.Slider, RangeDataWidget):

	def __init__(self, parent, value=0, range_val=(1, 100),
				size=(100, -1), vertical=False, onchange=None):
		self.range_val = range_val
		style = 0
		if vertical:
			style |= wx.SL_VERTICAL
		else:
			style |= wx.SL_HORIZONTAL
		start, end = range_val
		wx.Slider.__init__(self, parent, wx.ID_ANY, value, start,
						end, size=size, style=style)
		if onchange:
			self.Bind(wx.EVT_SCROLL_CHANGED, onchange, self)

