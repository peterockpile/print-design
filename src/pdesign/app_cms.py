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

import os

from uc2 import uc2const
from uc2.uc2const import COLOR_DISPLAY

from uc2.cms import ColorManager, CS, libcms
from uc2.formats.pdxf.pdxf_config import PDXF_Config
from pdesign import config

class AppColorManager(ColorManager):

	color_mngrs = []

	def __init__(self, app):
		self.app = app
		self.color_mngrs = []
		ColorManager.__init__(self)

	def get_profiles(self):
		pdxf_config = PDXF_Config()
		filename = 'pdxf_config.xml'
		config_file = os.path.join(self.app.appdata.app_config_dir, filename)
		pdxf_config.load(config_file)
		profiles = [pdxf_config.default_rgb_profile,
				pdxf_config.default_cmyk_profile,
				pdxf_config.default_lab_profile,
				pdxf_config.default_gray_profile]
		profiles.append(config.cms_display_profile)
		return profiles

	def update(self):
		self.handles = {}
		self.clear_transforms()
		profiles = self.get_profiles()
		profile_dicts = [config.cms_rgb_profiles,
						config.cms_cmyk_profiles,
						config.cms_lab_profiles,
						config.cms_gray_profiles,
						config.cms_display_profiles]
		index = 0
		profile_dir = self.app.appdata.app_color_profile_dir
		for item in CS + [COLOR_DISPLAY, ]:
			path = None
			profile = profiles[index]
			if profile and profile_dicts[index].has_key(profile):
				profile_filename = profile_dicts[index][profile]
				path = os.path.join(profile_dir, profile_filename)
			if path:
				if item == COLOR_DISPLAY:
					self.use_display_profile = True
				self.handles[item] = libcms.cms_open_profile_from_file(path)
			else:
				if item == COLOR_DISPLAY:
					self.use_display_profile = False
				else:
					self.handles[item] = libcms.cms_create_default_profile(item)
			index += 1
		self.intent = config.cms_intent
		self.flags = config.cms_flags
		self.proofing = config.cms_proofing

	def registry_cm(self, cm):
		self.color_mngrs.append(cm)
		self.apply_cm_settings(cm)

	def unregistry_cm(self, cm):
		self.color_mngrs.remove(cm)

	def apply_cm_settings(self, cm):
		if self.use_display_profile:
			cm.use_display_profile = True
			cm.handles[COLOR_DISPLAY] = self.handles[COLOR_DISPLAY]
		else:
			cm.use_display_profile = False
		cm.intent = self.intent
		cm.flags = self.flags
		cm.proofing = self.proofing
		cm.clear_transforms()

	def update_mngrs(self):
		for item in self.color_mngrs:
			self.apply_cm_settings(item)
