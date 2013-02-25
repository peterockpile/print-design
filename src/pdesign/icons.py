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

import os
import gtk

from pdesign import _, config


STOCK_DONT_SAVE = 'action-dont-save'

def load_icons():

	iconfactory = gtk.IconFactory()

	#Creating aliased icons
	items = [(STOCK_DONT_SAVE, _("_Don't save"), 0, 0, None), ]

	aliases = [(STOCK_DONT_SAVE, gtk.STOCK_NO), ]

	gtk.stock_add(items)

	for item, alias in aliases:
		iconset = gtk.icon_factory_lookup_default(alias)
		iconfactory.add(item, iconset)

	iconfactory.add_default()
