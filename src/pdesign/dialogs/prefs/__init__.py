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

from uc2.formats.pdxf.pdxf_config import PDXF_Config
from pdesign import _, config, appconst
from pdesign.dialogs.prefs import test
from pdesign.dialogs.prefs.cms_prefs import CmsPrefsPlugin

PLUGINS = [CmsPrefsPlugin, test.TestPlugin, test.Test1Plugin, test.Test2Plugin,
		 test.Test3Plugin]

def get_prefs_dialog(app):
	parent = app.mw
	title = _('%s Preferences') % (app.appdata.app_name)

	dialog = gtk.Dialog(title, parent,
	                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
	                   (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
	                    gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))


	vbox = gtk.VBox()
	content = PrefsContainer(app)
	vbox.pack_start(content)
	vbox.set_border_width(5)
	vbox.show_all()
	dialog.vbox.pack_start(vbox)

	ret = dialog.run()
	if ret == gtk.RESPONSE_ACCEPT:
		content.apply_changes()
		app.proxy.force_redraw()
	dialog.destroy()

class PrefsContainer(gtk.HPaned):

	model = None
	plugins = []
	current_plg = None

	def __init__(self, app):
		self.app = app
		self.pdxf_config = PDXF_Config()
		gtk.HPaned.__init__(self)
		self.set_size_request(700, 400)
		self.build_model()
		self.viewer = PluginViewer(self)
		self.add1(self.viewer)
		self.load_plugin(self.plugins[0])
		self.show_all()

	def build_model(self):
		self.model = PrefsNode(_('Preferences'), gtk.STOCK_PREFERENCES)
		self.app_prefs = PrefsNode(_('Application'), gtk.STOCK_PROPERTIES)
		self.model.childs.append(self.app_prefs)
		self.doc_prefs = PrefsNode(_('New document'), gtk.STOCK_NEW)
		self.model.childs.append(self.doc_prefs)
		for item in PLUGINS:
			plg = item(self.app, self.pdxf_config)
			if plg.cid == appconst.PREFS_APP_PLUGIN:
				self.app_prefs.childs.append(plg)
			else:
				self.doc_prefs.childs.append(plg)
			self.plugins.append(plg)

	def load_plugin(self, plg):
		if not plg.leaf: return
		if not self.current_plg is None: self.remove(self.current_plg)
		if not plg.built:
			plg.build()
		self.add2(plg)
		plg.show_all()
		self.current_plg = plg

	def apply_changes(self):
		for item in self.plugins:
			item.apply_changes()


class PrefsNode:

	short_title = ''
	icon_stock = gtk.STOCK_DIRECTORY
	icon = None
	childs = []
	leaf = False

	def __init__(self, title, icon=None):
		self.childs = []
		self.short_title = title
		if not icon is None:
			self.icon_stock = icon

class PluginViewer(gtk.VBox):

	def __init__(self, owner):
		gtk.VBox.__init__(self)
		self.owner = owner
		spacer = gtk.VBox()
		self.add(spacer)
		self.set_border_width(5)
		self.set_size_request(200, -1)

		self.listmodel = ObjectTreeModel(self.owner.model)

		self.treeview = gtk.TreeView()

		self.column = gtk.TreeViewColumn()
		render_pixbuf = gtk.CellRendererPixbuf()
		self.column.pack_start(render_pixbuf, expand=False)
		self.column.add_attribute(render_pixbuf, 'pixbuf', 0)
		render_text = gtk.CellRendererText()
		self.column.pack_start(render_text, expand=True)
		self.column.add_attribute(render_text, 'text', 1)
		self.treeview.append_column(self.column)

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

	def update_view(self, *args):
		if self.active:
			self.listmodel = ObjectTreeModel(self.owner.model)
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

	def view_object(self, *args):
		path = self.treeview.get_cursor()[0]
		obj = self.listmodel.get_obj_by_path(path)
		self.owner.load_plugin(obj)

class ObjectTreeModel(gtk.TreeStore):

	def __init__(self, model):
		gtk.TreeStore.__init__(self, gtk.gdk.Pixbuf, str)

		self.model = model
		self.model_dict = {}
		for child in self.model.childs:
			self.scan_model(None, child)

	def scan_model(self, iter, obj):
		child_iter = self.append(iter)
		self.add_to_dict(obj, child_iter)
		self.set(child_iter, 0, self.get_icon(obj),
							1, obj.short_title)
		for item in obj.childs:
			self.scan_model(child_iter, item)

	def add_to_dict(self, obj, iter):
		path_str = self.get_path(iter).__str__()
		self.model_dict[path_str] = obj

	def get_obj_by_path(self, path):
		return self.model_dict[path.__str__()]

	def get_icon(self, obj):
		if obj.icon is None:
			return gtk.Image().render_icon(obj.icon_stock, gtk.ICON_SIZE_MENU)
		return obj.icon

