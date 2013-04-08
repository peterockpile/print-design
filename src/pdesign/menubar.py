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

import types
import gtk

from pdesign import _

class AppMenubar(gtk.MenuBar):

	def __init__(self, mw):
		gtk.MenuBar.__init__(self)
		self.mw = mw
		self.app = mw.app
		self.actions = self.app.actions

		#----FILE MENU
		self.file_item, self.file_menu = self.create_menu(_("_File"))
		items = ['NEW',
				 None,
				 'OPEN',
				 'SAVE',
				 'SAVE_AS',
				 'SAVE_ALL',
				 None,
				 'CLOSE',
				 'CLOSE_ALL',
				 None,
				 'IMPORT_IMAGE',
				 None,
				 'PRINT_SETUP',
				 'PRINT',
				 None,
				 'QUIT'
		]
		self.add_items(self.file_menu, items)

		#----EDIT MENU
		self.edit_item, self.edit_menu = self.create_menu(_("_Edit"))
		items = ['UNDO',
				 'REDO',
				 'CLEAR_HISTORY',
				 None,
				 'CUT',
				 'COPY',
				 'PASTE',
				 'DELETE',
				 None,
				 'SELECT_ALL',
				 'DESELECT',
				 None,
				 'PROPERTIES',
				 'PREFERENCES',
		]
		self.add_items(self.edit_menu, items)

		#----VIEW MENU
		self.view_item, self.view_menu = self.create_menu(_("_View"))
		items = ['STROKE_VIEW',
				'DRAFT_VIEW',
				 None,
				 'ZOOM_100',
				 'ZOOM_IN',
				 'ZOOM_OUT',
				 None,
				 'ZOOM_PAGE',
				 'ZOOM_SELECTED',
#				 None,
#				 ('SHOW_GRID',),
#				 ('SHOW_GUIDES',),
				 None,
				 'SNAP_TO_GRID',
				 'SNAP_TO_GUIDES',
				 'SNAP_TO_OBJECTS',
				 'SNAP_TO_PAGE',
				 None,
				 'FORCE_REDRAW',
		]
		self.add_items(self.view_menu, items)

		#----LAYOUT MENU
		self.layout_item, self.layout_menu = self.create_menu(_("_Layout"))
		items = ['INSERT_PG',
				 'DELETE_PG',
				 'GOTO_PG',
				 None,
				 'NEXT_PG',
				 'PREV_PG',
		]
		self.add_items(self.layout_menu, items)

		#----ARRANGE MENU
		self.arrange_item, self.arrange_menu = self.create_menu(_("_Arrange"))
		items = ['COMBINE',
				'BREAK_APART',
				None,
				'GROUP',
				'UNGROUP',
				'UNGROUP_ALL',
				None,
				'CONVERT_TO_CURVES',
		]
		self.add_items(self.arrange_menu, items)

		#----EFFETCS MENU
		self.effects_item, self.effects_menu = self.create_menu(_("Effe_cts"))
		items = ['SET_CONTAINER',
				'UNPACK_CONTAINER',
		]
		self.add_items(self.effects_menu, items)

		#----BITMAPS MENU
		self.bitmaps_item, self.curve_menu = self.create_menu(_("_Bitmaps"))

		#----TEXT MENU
		self.text_item, self.text_menu = self.create_menu(_("_Text"))
		items = ['EDIT_TEXT',
		]
		self.add_items(self.text_menu, items)

		#----TOOLS MENU
		self.tools_item, self.tools_menu = self.create_menu(_("T_ools"))
		items = ['PAGES',
				'LAYERS',
				'DOM_VIEWER',
		]
		self.add_items(self.tools_menu, items)

		#----HELP MENU
		self.help_item, self.help_menu = self.create_menu(_("_Help"))
		items = ['REPORT_BUG',
				None,
				'PROJECT_WEBSITE',
				'PROJECT_FORUM',
				None,
				'ABOUT',
		]
		self.add_items(self.help_menu, items)

		#----HIDDEN MENU
		self.hidden_item, self.hidden_menu = self.create_menu("hidden")
		items = ['PREV_PG_KP',
				'NEXT_PG_KP',
				'CUT2',
				'CUT3',
				'PASTE2',
				'PASTE3',
				'DELETE2',
		]
		self.add_items(self.hidden_menu, items)

		self.append(self.file_item)
		self.append(self.edit_item)
		self.append(self.view_item)
		self.append(self.layout_item)
		self.append(self.arrange_item)
		self.append(self.effects_item)
		self.append(self.bitmaps_item)
		self.append(self.text_item)
		self.append(self.tools_item)
		self.append(self.help_item)
#		self.append(self.hidden_item)

	def create_menu(self, text):
		menu = gtk.Menu()
		item = gtk.MenuItem(text)
		item.set_submenu(menu)
		return item, menu

	def add_items(self, parent, items):
		for item in items:
			if item is None:
				parent.append(gtk.SeparatorMenuItem())
			else:
				action = self.actions[item]
				menuitem = action.create_menu_item()
				action.menuitem = menuitem
				parent.append(menuitem)
