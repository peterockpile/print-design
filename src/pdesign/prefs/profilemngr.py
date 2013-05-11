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
import gtk

from uc2.utils.fs import expanduser_unicode
from uc2.uc2const import COLOR_RGB, COLOR_CMYK, COLOR_LAB, COLOR_GRAY, COLOR_DISPLAY
from pdesign import _, config
from pdesign.widgets import ImageStockButton

def get_profiles_dialog(app, parent, colorspace):
	title = _('%s profiles') % (colorspace)

	dialog = gtk.Dialog(title, parent,
	                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
	                   (gtk.STOCK_CLOSE, gtk.RESPONSE_ACCEPT))


	vbox = gtk.VBox()
	content = ProfileManager(app, dialog, colorspace)
	vbox.pack_start(content)
	vbox.set_border_width(5)
	vbox.show_all()
	dialog.vbox.pack_start(vbox)

	dialog.run()
	dialog.destroy()

def _get_import_fiters():
	result = []

	ext_list = ['icc', 'icm']
	filter = gtk.FileFilter()
	filter.set_name(_('ICC color profiles'))
	for extension in ext_list:
		filter.add_pattern('*.' + extension)
		filter.add_pattern('*.' + extension.upper())
	result.append(filter)

	filter = gtk.FileFilter()
	filter.set_name(_('All files'))
	filter.add_pattern('*')
	result.append(filter)

	return result

def get_profile_import_dialog(parent, app, start_dir):
	result = ''
	caption = _('Import color profile')
	dialog = gtk.FileChooserDialog(caption,
				parent,
				gtk.FILE_CHOOSER_ACTION_OPEN,
				(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
					gtk.STOCK_OPEN, gtk.RESPONSE_OK))

	dialog.set_default_response(gtk.RESPONSE_OK)
	start_dir = expanduser_unicode(start_dir)
	dialog.set_current_folder(start_dir)

	for filter in _get_import_fiters():
		dialog.add_filter(filter)

	ret = dialog.run()
	if not ret == gtk.RESPONSE_CANCEL:
		result = dialog.get_filename()
	dialog.destroy()
	if result is None: result = ''
	return result

class ProfileManager(gtk.HBox):

	profiles = {}
	pf_list = []

	def __init__(self, app, dialog, colorspace):
		self.app = app
		self.dlg = dialog
		self.colorspace = colorspace
		gtk.HBox.__init__(self)
		self.build()

	def set_profiles(self):
		if self.colorspace == COLOR_RGB:self.profiles = config.rgb_profiles
		elif self.colorspace == COLOR_CMYK:self.profiles = config.cmyk_profiles
		elif self.colorspace == COLOR_LAB:self.profiles = config.lab_profiles
		elif self.colorspace == COLOR_GRAY:self.profiles = config.gray_profiles
		else:self.profiles = config.display_profiles

	def update_list(self):
		keys = self.profiles.keys()
		keys.sort()
		default = _('Built-in %s profile') % (self.colorspace)
		self.pf_list = [default, ] + keys

	def build(self):
		self.set_profiles()
		self.update_list()
		self.viewer = ProfileList(self, self.pf_list)
		self.pack_start(self.viewer, False, True, 5)

		box = gtk.VBox()
		self.add_button = ImageStockButton('Import profile', gtk.STOCK_ADD, False)
		self.add_button.connect('clicked', self.import_profile)
		box.pack_start(self.add_button, False, False, 5)

		self.remove_button = ImageStockButton('Remove profile', gtk.STOCK_REMOVE, False)
		self.remove_button.connect('clicked', self.remove_profile)
		box.pack_start(self.remove_button, False, False, 5)
		self.remove_button.set_sensitive(False)
		self.pack_start(box, False, False, 0)

	def import_profile(self, *args):
		print get_profile_import_dialog(self.dlg, self.app, '~')

	def remove_profile(self, *args):
		pass

	def check_selection(self, index):
		if index:
			self.remove_button.set_sensitive(True)
		else:
			self.remove_button.set_sensitive(False)


class ProfileList(gtk.VBox):

	def __init__(self, owner, objs):

		self.owner = owner

		gtk.VBox.__init__(self)
		self.set_size_request(300, 200)

		self.listmodel = ProfileListModel(objs)
		self.treeview = gtk.TreeView()

		self.column = gtk.TreeViewColumn()
		self.column.set_title(_('Profile names'))
		render_pixbuf = gtk.CellRendererPixbuf()
		self.column.pack_start(render_pixbuf, expand=False)
		self.column.add_attribute(render_pixbuf, 'pixbuf', 0)
		render_text = gtk.CellRendererText()
		self.column.pack_start(render_text, expand=True)
		self.column.add_attribute(render_text, 'text', 1)
		self.treeview.append_column(self.column)

		self.treeview.connect('cursor-changed', self.select_profile)
		self.treeview.connect('row-activated', self.inspect_file)

		self.scrolledwindow = gtk.ScrolledWindow()
		self.scrolledwindow.add(self.treeview)
		self.scrolledwindow.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		self.scrolledwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		self.pack_end(self.scrolledwindow, True)

		self.treeview.set_model(self.listmodel)
		self.treeview.set_rules_hint(True)
		self.update_view()

	def update_view(self):pass

	def select_profile(self, *args):
		index = self.treeview.get_cursor()[0][0]
		self.owner.check_selection(index)

	def inspect_file(self, treeview, path, column):
		pass

class ProfileListModel(gtk.ListStore):

	def __init__(self, objs):
		gtk.ListStore.__init__(self, gtk.gdk.Pixbuf, str)
		ICON = gtk.gdk.pixbuf_new_from_file(os.path.join(config.resource_dir,
							'icons', 'preferences', 'prefs-cms.png'))
		for item in objs:
			self.append((ICON, item))
