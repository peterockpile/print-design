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

from pdesign import events
from pdesign.plugins.layers_plg import LayersPlugin
from pdesign.plugins.dom_plg import DOMPlugin
from pdesign.plugins.pages_plg import PagesPlugin

PLUGINS = {}
INTERNAL = [LayersPlugin, DOMPlugin, PagesPlugin, ]

class PluginPanel(gtk.VBox):

	plugin_stack = []
	active_plg = ''
	active = False
	visible = True

	def __init__(self, mw):

		gtk.VBox.__init__(self)

		self.mw = mw
		self.app = mw.app

		self.nb = gtk.Notebook()
		self.nb.connect('switch-page', self.change_plugin)
		self.nb.set_property('scrollable', True)
		self.nb.set_tab_pos(gtk.POS_RIGHT)
		self.pack_start(self.nb, True, True, 0)

		self.set_size_request(200, -1)
		self.build_dict()
		events.connect(events.NO_DOCS, self.no_docs)
		events.connect(events.DOC_CHANGED, self.doc_changed)

	def build_dict(self):
		for item in INTERNAL:
			plg_item = item(self)
			PLUGINS[plg_item.name] = plg_item

	def load_plugin(self, name):
		if self.check_loaded(name):
			self.set_active_by_name(name)
		else:
			if not self.nb.get_n_pages():
				self.show_panel()
			plg = PLUGINS[name]
			if not plg.loaded:
				plg.build()
			self.plugin_stack.append(plg)
			self.nb.append_page(plg, plg.caption)
			self.nb.show_all()
			self.set_active_by_name(plg.name)
			self.active = True
			self.visible = True

	def close_panel(self):
		for item in self.plugin_stack:
			self.remove_plugin(item)

	def no_docs(self, *args):
		if self.active and self.visible:
			self.hide_panel()
			self.visible = False

	def doc_changed(self, *args):
		if self.active and not self.visible:
			self.show_panel()
			self.visible = True

	def check_loaded(self, name):
		result = False
		for item in self.plugin_stack:
			if item.name == name:
				result = True
				break
		return result

	def set_active_by_name(self, name):
		for item in self.plugin_stack:
			if item.name == name:
				index = self.nb.page_num(item)
				self.nb.set_current_page(index)
				self.deactivate_all()
				item.activate()
				self.active_plg = name

	def deactivate_all(self):
		for item in self.plugin_stack:
			item.deactivate()

	def remove_plugin(self, plg):
		self.nb.remove_page(self.nb.page_num(plg))
		self.plugin_stack.remove(plg)
		plg.deactivate()
		if not self.nb.get_n_pages():
			self.hide_panel()
			self.active = False
			self.visible = False

	def show_panel(self):
		self.mw.inner_hpaned.pack2(self, False, False)
		self.show_all()
		if self.active_plg:
			self.set_active_by_name(self.active_plg)

	def hide_panel(self):
		self.deactivate_all()
		self.mw.inner_hpaned.remove(self)

	def change_plugin(self, *args):
		plg = self.nb.get_nth_page(args[2])
		self.deactivate_all()
		plg.activate()
		self.active_plg = plg.name


