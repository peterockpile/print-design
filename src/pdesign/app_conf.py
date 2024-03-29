# -*- coding: utf-8 -*-
#
# 	Copyright (C) 2011-2012 by Igor E. Novikov
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

import os, sys

import cairo, wx
from PIL import Image

from uc2.cms import libcms
from uc2.uc_conf import UCConfig, UCData
from uc2 import uc2const#, libtrace
from uc2.utils import system
from uc2.formats.pdxf.const import DOC_STRUCTURE

from pdesign import events, appconst

class AppData(UCData):

	app_name = 'PrintDesign'
	app_proc = 'print-design'
	app_org = 'sK1 Project'
	app_domain = 'sk1project.org'
	app_icon = None
	doc_icon = None
	version = "1.0"
	revision = 'rev.824'
	app_config_dir = os.path.expanduser(os.path.join('~', '.config', 'pdesign'))
	plugin_dir = os.path.expanduser(os.path.join('~', '.config', 'pdesign', \
												'pd_custom_plugins'))
	components = []

	def __init__(self):

		UCData.__init__(self)

		#----------------Check clipboard directory
		self.app_clipboard_dir = os.path.join(self.app_config_dir, 'clipboard')
		if not os.path.lexists(self.app_clipboard_dir):
			os.makedirs(self.app_clipboard_dir)
		for item in DOC_STRUCTURE:
			path = os.path.join(self.app_clipboard_dir, item)
			if not os.path.lexists(path):
				os.makedirs(path)
		if not os.path.lexists(self.plugin_dir):
			os.makedirs(self.plugin_dir)
		plugin_dir_init = os.path.join(self.plugin_dir, '__init__.py')
		if not os.path.lexists(plugin_dir_init):
			fp = open(plugin_dir_init, 'w')
			fp.close()
		self.check_components()

	def seq_to_str(self, seq):
		ret = ''
		for item in seq: ret += str(item) + '.'
		return ret[:-1]

	def check_components(self):
		comp = self.components
		comp.append(['Python', sys.version])
		comp.append(['wxWidgets', wx.version()])
		comp.append(['UniConvertor', UCData.version + ' ' + UCData.revision])
		comp.append(['Cairo', cairo.cairo_version_string()])
		comp.append(['pycairo', self.seq_to_str(cairo.version_info)])
		comp.append(['PIL', Image.VERSION])
		comp.append(['LittleCMS', libcms.get_version()])
#		comp.append(['Potrace', libtrace.get_version()])


class AppConfig(UCConfig):

	def __setattr__(self, attr, value):
		if attr == 'filename': return
		if not hasattr(self, attr) or getattr(self, attr) != value:
			self.__dict__[attr] = value
			events.emit(events.CONFIG_MODIFIED, attr, value)


	def get_defaults(self):
		defaults = AppConfig.__dict__
		defaults.update(UCConfig.get_defaults())
		return defaults

	#============== GENERIC SECTION ===================
	os = system.LINUX
	system_encoding = 'utf-8'# default encoding (GUI uses utf-8 only)
	new_doc_on_start = True
	print_stacktrace = True

	#============== I/O SECTION ===================
	open_dir = '~'
	save_dir = '~'
	import_dir = '~'
	export_dir = '~'
	make_backup = True
	resource_dir = ''
	plugin_dirs = []
	profile_import_dir = '~'

	history_size = 100

	#============== UI SECTION ===================
	mw_maximized = 0
	mw_width = 1000
	mw_height = 700
	mw_min_width = 1000
	mw_min_height = 700
	spin_overlay = True
	statusbar_fontsize = 0
	tabs_fontsize = 0
	tabs_use_bold = True
	palette = ''
	show_splash = False
	menu_size = (16, 16)
	toolbar_size = (24, 24)
	toolbar_icon_size = (24, 24)
	set_doc_icon = True
	history_list_size = 10

	default_polygon_num = 5

	#============== MOUSE OPTIONS ================
	mouse_scroll_sensitivity = 3.0

	#============== RULER OPTIONS ================
	ruler_size = 20
	ruler_style = 0
	ruler_min_tick_step = 3
	ruler_min_text_step = 50
	ruler_max_text_step = 100

	#============== PALETTE OPTIONS ================
	palette_cell_vertical = 18
	palette_cell_horizontal = 40
	palette_orientation = uc2const.HORIZONTAL

	#============== CANVAS OPTIONS ================
	default_unit = uc2const.UNIT_MM

	obj_jump = 1.0 * uc2const.mm_to_pt

	sel_frame_visible = 1
	sel_frame_offset = 10.0
	sel_frame_color = (0.0, 0.0, 0.0)
	sel_frame_dash = [5, 5]

	sel_bbox_visible = 0
	sel_bbox_color = (0.0, 0.0, 0.0)
	sel_bbox_bgcolor = (1.0, 1.0, 1.0)
	sel_bbox_dash = [5, 5]

	sel_marker_size = 9.0
	sel_marker_frame_color = (0.62745, 0.62745, 0.64314)
	sel_marker_frame_bgcolor = (1.0, 1.0, 1.0)
	sel_marker_frame_dash = [5, 5]
	sel_marker_fill = (1.0, 1.0, 1.0)
	sel_marker_stroke = (0.0, 0.3, 1.0)
	sel_object_marker_color = (0.0, 0.0, 0.0)

	rotation_step = 5.0# in degrees
	stroke_sensitive_size = 5.0# in pixels

	#============== SNAPPING OPTIONS ================
	snap_distance = 10.0# in pixels
	snap_order = [appconst.SNAP_TO_GUIDES,
				appconst.SNAP_TO_GRID,
				appconst.SNAP_TO_OBJECTS,
				appconst.SNAP_TO_PAGE]
	snap_to_grid = False
	snap_to_guides = True
	snap_to_objects = False
	snap_to_page = False

	show_snap = True
	snap_line_dash = [5, 5]
	snap_line_color = (1.0, 0.0, 0.0, 1.0)

	guide_line_dash = [5, 5]
	guide_line_dragging_color = (0.0, 0.0, 0.0, 0.25)

	#============== BEZIER CURVE OPTIONS ================
	curve_autoclose_flag = 0

	curve_stroke_color = (0.0, 0.0, 0.0)
	curve_stroke_width = 0.7
	curve_trace_color = (1.0, 0.0, 0.0)
	curve_point_sensitivity_size = 9.0

	curve_start_point_size = 5.0
	curve_start_point_fill = (1.0, 1.0, 1.0)
	curve_start_point_stroke = (0.0, 0.0, 0.0)
	curve_start_point_stroke_width = 2.0

	curve_point_size = 5.0
	curve_point_fill = (1.0, 1.0, 1.0)
	curve_point_stroke = (0.0, 0.3, 1.0)
	curve_point_stroke_width = 1.0

	curve_last_point_size = 5.0
	curve_last_point_fill = (1.0, 1.0, 1.0)
	curve_last_point_stroke = (0.0, 0.3, 1.0)
	curve_last_point_stroke_width = 2.0

	control_point_size = 5.0
	control_point_fill = (1.0, 1.0, 1.0)
	control_point_stroke = (0.0, 0.0, 0.0)
	control_point_stroke_width = 1.0

	control_line_stroke_color = (0.0, 0.5, 0.0)
	control_line_stroke_width = 0.7
	control_line_stroke_dash = [5, 5]

	def is_linux(self):
		if self.os == system.LINUX: return True
		return False

	def is_mac(self):
		if self.os == system.MACOSX: return True
		return False

	def is_win(self):
		if self.os == system.WINDOWS: return True
		return False




class LinuxConfig(AppConfig):
	os = system.LINUX
	statusbar_fontsize = 9
	tabs_fontsize = 9
	tabs_use_bold = False

class MacosxConfig(AppConfig):
	os = system.MACOSX
	toolbar_size = (16, 16)
	toolbar_icon_size = (16, 16)
	spin_overlay = False

class WinConfig(AppConfig):
	os = system.WINDOWS
	toolbar_size = (24, 24)
	toolbar_icon_size = (16, 16)
	statusbar_fontsize = 0



def get_app_config():
	os_family = system.get_os_family()
	if os_family == system.MACOSX:
		return MacosxConfig()
	elif os_family == system.WINDOWS:
		return WinConfig()
	else:
		return LinuxConfig()
