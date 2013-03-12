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


from pdesign import _, events, icons
from pdesign.plugins.plg_caption import PluginTabCaption

class DOMPlugin(gtk.VBox):

	name = 'DOMPlugin'
	title = _('Object browser')
	icon = icons.STOCK_PLUGIN_DOM_VIEWER
	loaded = False
	active = False

	def __init__(self, master):
		gtk.VBox.__init__(self)
		self.master = master
		self.mw = master.mw
		self.app = master.app
		self.caption = PluginTabCaption(self, self.icon, self.title)

	def build(self):
		spacer = gtk.VBox()
		self.add(spacer)
		self.set_border_width(5)

		model = self.app.current_doc.doc_presenter.model
		self.listmodel = ObjectTreeModel(model)

		self.treeview = gtk.TreeView()

		self.column = gtk.TreeViewColumn()
		self.column.set_title(_('Document Object Model'))
		render_pixbuf = gtk.CellRendererPixbuf()
		self.column.pack_start(render_pixbuf, expand=False)
		self.column.add_attribute(render_pixbuf, 'pixbuf', 0)
		render_text = gtk.CellRendererText()
		self.column.pack_start(render_text, expand=True)
		self.column.add_attribute(render_text, 'text', 1)
		self.treeview.append_column(self.column)

		self.column1 = gtk.TreeViewColumn()
		render_text = gtk.CellRendererText()
		self.column1.pack_start(render_text, expand=False)
		self.column1.add_attribute(render_text, 'text', 2)
		self.column1.add_attribute(render_text, 'foreground', 3)
		self.treeview.append_column(self.column1)

		self.treeview.connect('cursor-changed', self.view_object)

		self.scrolledwindow = gtk.ScrolledWindow()
		self.scrolledwindow.add(self.treeview)
		self.scrolledwindow.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		self.scrolledwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		spacer.pack_end(self.scrolledwindow, True)

		self.treeview.set_model(self.listmodel)
		self.treeview.set_rules_hint(True)
		self.treeview.set_enable_tree_lines(True)

		self.expand_all()

		self.loaded = True
		events.connect(events.DOC_CHANGED, self.update_view)
		events.connect(events.DOC_MODIFIED, self.update_view)

	def update_view(self, *args):
		if self.active:
			model = self.app.current_doc.doc_presenter.model
			self.listmodel = ObjectTreeModel(model)
			self.treeview.set_model(self.listmodel)
			self.expand_all()

	def activate(self):
		self.active = True
		self.update_view()

	def deactivate(self):
		self.active = False

	def collapse_all(self, *args):
		self.treeview.collapse_all()

	def expand_all(self, *args):
		self.treeview.expand_all()

	def view_object(self, *args):pass



NODE_ICON = gtk.Image().render_icon(gtk.STOCK_DIRECTORY, gtk.ICON_SIZE_MENU)
LEAF_ICON = gtk.Image().render_icon(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU)
COLOR = '#A7A7A7'

class ObjectTreeModel(gtk.TreeStore):

	def __init__(self, model):
		gtk.TreeStore.__init__(self, gtk.gdk.Pixbuf, str, str, str)

		self.model = model
		self.model_dict = {}

		iter = self.append(None)
		self.add_to_dict(self.model, iter)
		self.model_dict[iter] = self.model
		icon_type, name, info = self.model.resolve()
		self.set(iter, 0, self.get_icon(icon_type),
						1, name,
						2, info,
						3, COLOR)
		for child in self.model.childs:
			self.scan_model(iter, child)

	def scan_model(self, iter, obj):
		child_iter = self.append(iter)
		self.add_to_dict(obj, child_iter)
		icon_type, name, info = obj.resolve()
		self.set(child_iter, 0, self.get_icon(icon_type),
							1, name,
							2, info,
							3, COLOR)
		for item in obj.childs:
			self.scan_model(child_iter, item)

	def add_to_dict(self, obj, iter):
		path_str = self.get_path(iter).__str__()
		self.model_dict[path_str] = obj

	def get_obj_by_path(self, path):
		return self.model_dict[path.__str__()]

	def get_icon(self, type):
		if type: return LEAF_ICON
		return NODE_ICON
