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

import os
import sys
import gtk


from uc2.formats import get_loader, get_saver
from uc2.formats.pdxf.presenter import PDXF_Presenter
from uc2 import uc2const
from uc2.utils.fs import change_file_extension

from pdesign import _, config, events
from pdesign.dialogs import ProgressDialog
from widgets.docarea import DocArea

from eventloop import EventLoop
from api import PresenterAPI
from view.selection import Selection

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



	def __init__(self, app, doc_file='', silent=False):
		self.app = app
		self.eventloop = EventLoop(self)
		self.selection = Selection(self)


		if doc_file:
			loader = get_loader(doc_file)
			if loader is None:
				raise IOError(_('Unknown file format'), doc_file)

			if silent:
				self.doc_presenter = loader(app.appdata, doc_file)
			else:
				pd = ProgressDialog(_('Opening file...'), self.app.mw)
				ret = pd.run(loader, [app.appdata, doc_file])
				if ret == gtk.RESPONSE_OK:
					if pd.result is None:
						pd.destroy()
						raise IOError(*pd.error_info)

					self.doc_presenter = pd.result
					pd.destroy()
				else:
					pd.destroy()
					raise IOError(_('Error while opening'), doc_file)

			self.doc_file = self.doc_presenter.doc_file
			self.doc_name = os.path.basename(self.doc_file)
			self.doc_name = change_file_extension(self.doc_name,
									uc2const.FORMAT_EXTENSION[uc2const.PDXF][0])
		else:
			self.doc_presenter = PDXF_Presenter(app.appdata)
			self.doc_presenter.new()
			self.doc_name = self.app.get_new_docname()

		self.methods = self.doc_presenter.methods
		self.model = self.doc_presenter.model
		self.set_active_page()


		self.cms = self.app.default_cms

		self.api = PresenterAPI(self)
		self.docarea = DocArea(self.app, self)
		self.canvas = self.docarea.canvas
		self.api.view = self.canvas
		self.app.mw.add_tab(self.docarea)
		self.eventloop.connect(self.eventloop.DOC_MODIFIED, self.modified)
		self.traced_objects = [
							self.eventloop,
							self.api,
							self.docarea.hruler,
							self.docarea.vruler,
							self.docarea.corner,
							self.docarea,
							self.canvas.renderer,
							self.canvas,
							self.selection,
							self
							]

	def close(self):
		if not self.docarea is None:
			self.app.mw.remove_tab(self.docarea)
		self.doc_presenter.close()
		for obj in self.traced_objects:
			fields = obj.__dict__
			items = fields.keys()
			for item in items:
				fields[item] = None

	def modified(self, *args):
		self.saved = False
		self.set_title()
		events.emit(events.DOC_MODIFIED, self)

	def reflect_saving(self):
		self.saved = True
		self.set_title()
		self.api.save_mark()
		events.emit(events.DOC_SAVED, self)

	def set_title(self):
		if self.saved:
			title = self.doc_name
		else:
			title = self.doc_name + '*'
		self.app.mw.set_tab_title(self.docarea, title)

	def set_doc_file(self, doc_file, doc_name=''):
		self.doc_file = doc_file
		if doc_name:
			self.doc_name = doc_name
		else:
			self.doc_name = os.path.basename(self.doc_file)
		self.set_title()

	def save(self):
		try:
			if config.make_backup:
				if os.path.lexists(self.doc_file):
					if os.path.lexists(self.doc_file + '~'):
						os.remove(self.doc_file + '~')
					os.rename(self.doc_file, self.doc_file + '~')
			saver = get_saver(self.doc_file)
			if saver is None:
				raise IOError(_('Unknown file format is requested for saving!'),
							 self.doc_file)

			pd = ProgressDialog(_('Saving file...'), self.app.mw)
			ret = pd.run(saver, [self.doc_presenter, self.doc_file])
			if ret == gtk.RESPONSE_OK:
				if not pd.error_info is None:
					pd.destroy()
					raise IOError(*pd.error_info)
				pd.destroy()
			else:
				pd.destroy()
				raise IOError(_('Error while saving'), self.doc_file)

		except IOError:
			raise IOError(*sys.exc_info())
		self.reflect_saving()

	def set_active_page(self, page_num=0):
		self.active_page = self.doc_presenter.methods.get_page(page_num)
		self.set_active_layer(self.active_page)

	def get_pages(self):
		return self.doc_presenter.methods.get_pages()

	def next_page(self):
		pages = self.doc_presenter.methods.get_pages()
		if pages.index(self.active_page) < len(pages) - 1:
			self.set_active_page(pages.index(self.active_page) + 1)
			self.selection.clear()
			self.eventloop.emit(self.eventloop.PAGE_CHANGED)
			events.emit(events.PAGE_CHANGED, self)

	def previous_page(self):
		pages = self.get_pages()
		if pages.index(self.active_page):
			self.set_active_page(pages.index(self.active_page) - 1)
			self.selection.clear()
			self.eventloop.emit(self.eventloop.PAGE_CHANGED)
			events.emit(events.PAGE_CHANGED, self)

	def goto_page(self, index):
		pages = self.get_pages()
		current_index = pages.index(self.active_page)
		if index >= 0 and index <> current_index:
			self.set_active_page(index)
			self.selection.clear()
			self.eventloop.emit(self.eventloop.PAGE_CHANGED)
			events.emit(events.PAGE_CHANGED, self)

	def set_active_layer(self, page, layer_num=0):
		self.active_layer = self.doc_presenter.methods.get_layer(page, layer_num)

	def get_page_size(self, page=None):
		if page is None:
			page = self.active_page
		page_format = page.page_format
		if page_format[2]:
			h, w = page_format[1]
		else:
			w, h = page_format[1]
		return w, h
