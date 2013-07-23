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

from uc2.formats import get_loader, get_saver
from uc2.formats.pdxf.presenter import PDXF_Presenter
from uc2 import uc2const
from uc2.utils.fs import change_file_extension

from pdesign import _
from pdesign.document.eventloop import EventLoop
from pdesign.document.selection import Selection

class PD_Presenter:

	doc_presenter = None
	doc_file = ''
	doc_name = ''


	model = None
	methods = None
	renderer = None
	active_page = None
	active_layer = None

	saved = True

	eventloop = None
	docarea = None
	canvas = None
	selection = None
	traced_objects = None
	snap = None

	def __init__(self, app, doc_file='', silent=True):
		self.app = app

		self.eventloop = EventLoop(self)
		self.selection = Selection(self)

		if doc_file:
			loader = get_loader(doc_file)
			if loader is None:
				raise IOError(_('Unknown file format'), doc_file)

			if silent:
				self.doc_presenter = loader(app.appdata, doc_file)
#			else:
#				pd = ProgressDialog(_('Opening file...'), self.app.mw)
#				ret = pd.run(loader, [app.appdata, doc_file])
#				if ret == gtk.RESPONSE_OK:
#					if pd.result is None:
#						pd.destroy()
#						raise IOError(*pd.error_info)
#
#					self.doc_presenter = pd.result
#					pd.destroy()
#				else:
#					pd.destroy()
#					raise IOError(_('Error while opening'), doc_file)

			self.doc_file = self.doc_presenter.doc_file
			self.doc_name = os.path.basename(self.doc_file)
			self.doc_name = change_file_extension(self.doc_name,
									uc2const.FORMAT_EXTENSION[uc2const.PDXF][0])
		else:
			self.doc_presenter = PDXF_Presenter(app.appdata)
			self.doc_name = self.app.get_new_docname()

		self.methods = self.doc_presenter.methods
		self.model = self.doc_presenter.model
		self.set_active_page()


		self.cms = self.doc_presenter.cms
		self.app.default_cms.registry_cm(self.cms)

		self.docarea = self.app.mdi.create_docarea(self)
		self.canvas = self.docarea.canvas
		self.canvas.set_mode()

	def close(self):
		self.app.mdi.remove_doc(self)
		self.app.default_cms.unregistry_cm(self.cms)
		self.doc_presenter.close()
		self.docarea.destroy()

	def set_active_page(self, page_num=0):
		self.active_page = self.doc_presenter.methods.get_page(page_num)
		self.set_active_layer(self.active_page)

	def set_active_layer(self, page, layer_num=-1):
		self.active_layer = self.doc_presenter.methods.get_layer(page, layer_num)

	def get_editable_layers(self, page=None):
		if page is None: page = self.active_page
		layers = []
		for layer in self.methods.get_desktop_layers():
			if layer.properties[1]:layers.append(layer)
		for layer in page.childs:
			if layer.properties[1]:layers.append(layer)
		for layer in self.methods.get_master_layers():
			if layer.properties[1]:layers.append(layer)
		return layers

	def get_visible_layers(self, page=None):
		if page is None: page = self.active_page
		layers = []
		for layer in self.methods.get_desktop_layers():
			if layer.properties[0]:layers.append(layer)
		for layer in page.childs:
			if layer.properties[0]:layers.append(layer)
		for layer in self.methods.get_master_layers():
			if layer.properties[0]:layers.append(layer)
		return layers

	def get_page_size(self, page=None):
		if page is None:
			page = self.active_page
		w, h = page.page_format[1]
		return w, h
