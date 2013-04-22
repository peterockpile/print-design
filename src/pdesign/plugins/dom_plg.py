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

from uc2.formats.pdxf import model
from pdesign import _, events, icons, config
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

		doc_model = self.app.current_doc.doc_presenter.model
		self.listmodel = ObjectTreeModel(doc_model)

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

		self.document_icon = self.load_icon('object-document.png')
		self.pages_icon = self.load_icon('object-pages.png')
		self.page_icon = self.load_icon('object-page.png')
		self.layer_icon = self.load_icon('object-layer.png')
		self.grid_layer_icon = self.load_icon('object-grid-layer.png')
		self.guide_layer_icon = self.load_icon('object-guide-layer.png')
		self.master_layers_icon = self.load_icon('object-master-layers.png')
		self.desktop_layers_icon = self.load_icon('object-desktop-layers.png')
		self.guide_icon = self.load_icon('object-guide.png')

		self.group_icon = self.load_icon('object-group.png')
		self.container_icon = self.load_icon('object-container.png')
		self.curve_icon = self.load_icon('object-curve.png')
		self.rect_icon = self.load_icon('object-rect.png')
		self.ellipse_icon = self.load_icon('object-ellipse.png')
		self.polygon_icon = self.load_icon('object-polygon.png')
		self.text_icon = self.load_icon('object-text.png')

		iter = self.append(None)
		self.add_to_dict(self.model, iter)
		self.model_dict[iter] = self.model
		icon_type, name, info = self.model.resolve()
		self.set(iter, 0, self.get_icon(icon_type, self.model),
						1, name,
						2, info,
						3, COLOR)
		for child in self.model.childs:
			self.scan_model(iter, child)

	def load_icon(self, path):
		loader = gtk.gdk.pixbuf_new_from_file
		pixbuf = loader(os.path.join(config.resource_dir, 'icons', 'obj_browser', path))
		return pixbuf

	def scan_model(self, iter, obj):
		child_iter = self.append(iter)
		self.add_to_dict(obj, child_iter)
		icon_type, name, info = obj.resolve()
		self.set(child_iter, 0, self.get_icon(icon_type, obj),
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

	def get_icon(self, type, obj):
		if obj.cid == model.DOCUMENT:return self.document_icon
		if obj.cid == model.PAGES:return self.pages_icon
		if obj.cid == model.PAGE:return self.page_icon
		if obj.cid == model.LAYER:return self.layer_icon
		if obj.cid == model.GRID_LAYER:return self.grid_layer_icon
		if obj.cid == model.GUIDE_LAYER:return self.guide_layer_icon
		if obj.cid == model.MASTER_LAYERS:return self.master_layers_icon
		if obj.cid == model.DESKTOP_LAYERS:return self.desktop_layers_icon
		if obj.cid == model.GUIDE:return self.guide_icon

		if obj.cid == model.GROUP:return self.group_icon
		if obj.cid == model.CONTAINER:return self.container_icon
		if obj.cid == model.RECTANGLE:return self.rect_icon
		if obj.cid == model.CURVE:return self.curve_icon
		if obj.cid == model.CIRCLE:return self.ellipse_icon
		if obj.cid == model.POLYGON:return self.polygon_icon
		if obj.cid == model.TEXT_BLOCK:return self.text_icon

		if type: return LEAF_ICON
		return NODE_ICON
