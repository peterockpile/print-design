# -*- coding: utf-8 -*-
#
#	Copyright (C) 2012 by Igor E. Novikov
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
from pdesign import _, appconst

from pdesign.dialogs.prefs.generic import GenericPrefsPlugin

class TestPlugin(GenericPrefsPlugin):

	name = 'TestPlugin'
	title = _('Test Preference Plugin')
	short_title = _('Test Plugin')

	def __init__(self, app, pdxf_config):
		GenericPrefsPlugin.__init__(self, app, pdxf_config)

class Test1Plugin(GenericPrefsPlugin):

	name = 'Test1Plugin'
	title = _('Test1 Preference Plugin')
	short_title = _('Test1 Plugin')

	def __init__(self, app, pdxf_config):
		GenericPrefsPlugin.__init__(self, app, pdxf_config)

class Test2Plugin(GenericPrefsPlugin):

	name = 'Test2Plugin'
	title = _('Test2 Preference Plugin')
	short_title = _('Test2 Plugin')
	cid = appconst.PREFS_DOC_PLUGIN

	def __init__(self, app, pdxf_config):
		GenericPrefsPlugin.__init__(self, app, pdxf_config)

class Test3Plugin(GenericPrefsPlugin):

	name = 'Test3Plugin'
	title = _('Test3 Preference Plugin')
	short_title = _('Test3 Plugin')
	cid = appconst.PREFS_DOC_PLUGIN

	def __init__(self, app, pdxf_config):
		GenericPrefsPlugin.__init__(self, app, pdxf_config)
