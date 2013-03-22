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

import os

from uc2.uc_conf import UCConfig
from uc2 import uc2const
from uc2.utils import system
from uc2.utils.fs import expanduser_unicode

from pdesign import events

class AppData:

	app_name = 'PrintDesign'
	app_proc = 'print-design'
	app_org = 'sK1 Project'
	app_domain = 'sk1project.org'
	app_icon = None
	doc_icon = None
	version = "1.0"

#	Check config root directory
	app_config_dir = expanduser_unicode(os.path.join('~', '.config', 'pdesign'))
	if not os.path.lexists(app_config_dir):
		os.makedirs(app_config_dir)

#	Check color profiles directory	
	app_color_profile_dir = os.path.join(app_config_dir, 'profiles')
	if not os.path.lexists(app_color_profile_dir):
		os.makedirs(app_color_profile_dir)

#	Config file path 
	app_config = os.path.join(app_config_dir, 'preferences.cfg')


class AppConfig(UCConfig):

	def __setattr__(self, attr, value):
		if not hasattr(self, attr) or getattr(self, attr) != value:
			self.__dict__[attr] = value
			events.emit(events.CONFIG_MODIFIED, attr, value)

	#============== GENERIC SECTION ===================
	system_encoding = 'utf-8'	# default encoding (GUI uses utf-8 only)
	new_doc_on_start = True
	#============== UI SECTION ===================
	palette_cell_vertical = 18
	palette_cell_horizontal = 40
	palette_orientation = 1

	# 0 - tabbed 
	# 1 - windowed 
	interface_type = 0

	mw_maximized = 0

	mw_width = 1000
	mw_height = 700

	mw_min_width = 1000
	mw_min_height = 700

	show_splash = 1

	set_doc_icon = 1

	ruler_style = 0
	ruler_min_tick_step = 3
	ruler_min_text_step = 50
	ruler_max_text_step = 100

	# 0 - page center
	# 1 - lower-left page corner
	# 2 - upper-left page corner 
	ruler_coordinates = 1

	default_unit = uc2const.UNIT_MM

	obj_jump = 1.0 * uc2const.mm_to_pt

	sel_frame_visible = 1
	sel_frame_offset = 0.0
	sel_frame_color = (0.0, 0.0, 0.0)
	sel_frame_dash = [5, 5]

	sel_marker_size = 9.0
	sel_marker_frame_color = (0.62745, 0.62745, 0.64314)
	sel_marker_frame_bgcolor = (1.0, 1.0, 1.0)
	sel_marker_frame_dash = [5, 5]
	sel_marker_fill = (1.0, 1.0, 1.0)
	sel_marker_stroke = (0.0, 0.3, 1.0)
	sel_object_marker_color = (0.0, 0.0, 0.0)

	rotation_step = 5.0 #in degrees
	stroke_sensitive_size = 5.0 #in pixels

	#============== POLYLINE CREATOR OPTIONS ================
	line_autoclose_flag = 0

	line_stroke_color = (0.0, 0.0, 0.0)
	line_stroke_width = 0.7
	line_trace_color = (1.0, 0.0, 0.0)
	line_sensitivity_size = 9.0

	line_start_point_size = 5.0
	line_start_point_fill = (1.0, 1.0, 1.0)
	line_start_point_stroke = (0.0, 0.3, 1.0)
	line_start_point_stroke_width = 2.0

	line_point_size = 5.0
	line_point_fill = (1.0, 1.0, 1.0)
	line_point_stroke = (0.0, 0.3, 1.0)
	line_point_stroke_width = 1.0

	line_last_point_size = 5.0
	line_last_point_fill = (1.0, 1.0, 1.0)
	line_last_point_stroke = (0.0, 0.3, 1.0)
	line_last_point_stroke_width = 1.0

	line_closing_point_size = 5.0
	line_closing_point_fill = (1.0, 1.0, 1.0)
	line_closing_point_stroke = (0.0, 0.3, 1.0)
	line_closing_point_stroke_width = 2.0

	#============== COLOR PROFILES ================
	display_profiles = {}
	rgb_profiles = {}
	cmyk_profiles = {}
	lab_profiles = {}
	gray_profiles = {}

	display_profile = ''

	#============== I/O SECTION ===================
	open_dir = '~'
	save_dir = '~'
	import_dir = '~'
	export_dir = '~'
	make_backup = 1
	resource_dir = ''

	def __init__(self, path):
		pass
#		self.resource_dir = os.path.join(path, 'share')




class LinuxConfig(AppConfig):
	os = system.LINUX

class MacosxConfig(AppConfig):
	os = system.MACOSX
	mw_maximized = 0
	set_doc_icon = 0
	ruler_style = 0

class WinConfig(AppConfig):
	os = system.WINDOWS
	ruler_style = 0



def get_app_config(path):
	os_family = system.get_os_family()
	if os_family == system.MACOSX:
		return MacosxConfig(path)
	elif os_family == system.WINDOWS:
		return WinConfig(path)
	else:
		return LinuxConfig(path)