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
import gtk
import sys

from uc2.application import UCApplication
from uc2.utils import system
from uc2 import cms, uc2const

from pdesign import _, config, events, icons
from pdesign import dialogs
from pdesign import modes
from pdesign.app_conf import AppData
from pdesign.app_cms import AppColorManager
from pdesign.proxy import AppProxy
from pdesign.inspector import DocumentInspector
from pdesign.mainwindow import MainWindow
from pdesign.actions import create_actions
from pdesign.presenter import PD_Presenter
from pdesign.clipboard import AppClipboard


class Application(UCApplication):

	appdata = None

	actions = {}
	docs = []
	current_doc = None
	doc_counter = 0

	proxy = None
	inspector = None
	cursors = None


	def __init__(self, path):

		UCApplication.__init__(self, path)

		self.path = path

		self.appdata = AppData()
		config.load(self.appdata.app_config)
		config.resource_dir = os.path.join(self.path, 'share')

		self.default_cms = AppColorManager(self)

		icons.load_icons()

		self.cursors = modes.get_cursors()
		self.inspector = DocumentInspector(self)
		self.proxy = AppProxy(self)
		self.clipboard = AppClipboard(self)


		self.accelgroup = gtk.AccelGroup()
		self.actiongroup = gtk.ActionGroup('BasicAction')

		self.actions = create_actions(self)
		self.mw = MainWindow(self)
		self.proxy.update_references()

	def run(self):
		events.emit(events.NO_DOCS)
		events.emit(events.APP_STATUS,
				_('To start create new or open existing document'))
		self.process_args()
		gtk.main()

	def process_args(self):
		args = sys.argv[1:]
		if args:
			for arg in args:
				self.open(arg, True)
		elif config.new_doc_on_start:
			self.new()

	def stub(self, *args):
		pass

	def get_new_docname(self):
		self.doc_counter += 1
		return _('Untitled') + ' ' + str(self.doc_counter)

	def set_current_doc(self, doc):
		self.current_doc = doc
		events.emit(events.DOC_CHANGED, doc)

	def exit(self):
		if self.close_all():
			self.update_config()
			config.save(self.appdata.app_config)
			gtk.main_quit()
			return True
		return False

	def new(self):
		doc = PD_Presenter(self)
		self.docs.append(doc)
		self.set_current_doc(doc)
		events.emit(events.APP_STATUS, _('New document created'))

	def close(self, doc=None):
		if not self.docs:
			return
		if doc is None:
			doc = self.current_doc

		if not self.mw.nb.page_num(doc.docarea) == self.mw.nb.get_current_page():
			self.mw.set_active_tab(doc.docarea)

		if self.inspector.is_doc_not_saved(doc):
			first = _("Document '%s' has been modified.") % (doc.doc_name)
			second = _('Do you want to save your changes?')
			ret = dialogs.warning_dialog(self.mw, self.appdata.app_name,
					first, second,
					[(icons.STOCK_DONT_SAVE , gtk.RESPONSE_NO,),
					(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL),
					(gtk.STOCK_SAVE, gtk.RESPONSE_OK)])

			if ret == gtk.RESPONSE_OK:
				if not self.save(): return False
			elif ret == gtk.RESPONSE_NO: pass
			else: return False

		if doc in self.docs:
			self.docs.remove(doc)
			doc.close()
			events.emit(events.DOC_CLOSED)
			if not len(self.docs):
				self.current_doc = None
				events.emit(events.NO_DOCS)
				msg = _('To start create new or open existing document')
				events.emit(events.APP_STATUS, msg)
		return True

	def close_all(self):
		result = True
		if self.docs:
			while self.docs:
				result = self.close(self.docs[0])
				if not result:
					break
		return result

	def open(self, doc_file='', silent=False):
		if not doc_file:
			doc_file = dialogs.get_open_file_name(self.mw, self,
												config.open_dir)
		if os.path.lexists(doc_file) and os.path.isfile(doc_file):
			try:
				doc = PD_Presenter(self, doc_file, silent)
			except:
				details = sys.exc_info()[1].__str__() + sys.exc_info()[2].__str__()
				msg = _('Cannot open file')
				msg = "%s '%s'" % (msg, doc_file)
				sec = _('The file may be corrupted or not supported format')
				dialogs.msg_dialog(self.mw, self.appdata.app_name, msg, sec, details)
				return
			self.docs.append(doc)
			self.set_current_doc(doc)
			config.open_dir = os.path.dirname(doc_file)
			events.emit(events.APP_STATUS, _('Document opened'))

	def import_image(self, image_file=''):
		if not image_file:
			image_file = dialogs.get_open_file_name(self.mw, self,
												config.import_dir, True)
		if os.path.lexists(image_file) and os.path.isfile(image_file):
			try:
				print image_file
			except:
				details = sys.exc_info()[1].__str__() + sys.exc_info()[2].__str__()
				msg = _('Cannot import image')
				msg = "%s '%s'" % (msg, image_file)
				sec = _('The file may be corrupted or not supported format')
				dialogs.msg_dialog(self.mw, self.appdata.app_name, msg, sec, details)
				return
			config.import_dir = os.path.dirname(image_file)
			events.emit(events.APP_STATUS, _('Image is imported'))

	def save(self, doc=''):
		if not doc:
			doc = self.current_doc
		if not doc.doc_file:
			return self.save_as()
		ext = os.path.splitext(self.current_doc.doc_file)[1]
		if not ext == "." + uc2const.FORMAT_EXTENSION[uc2const.PDXF][0]:
			return self.save_as()
		if not os.path.lexists(os.path.dirname(self.current_doc.doc_file)):
			return self.save_as()

		try:
			doc.save()
			events.emit(events.DOC_SAVED, doc)
		except:
			details = sys.exc_info()[1].__str__() + sys.exc_info()[2].__str__()
			msg = _('Cannot save file')
			msg = "%s '%s'" % (msg, self.current_doc.doc_file)
			sec = _('Please check file write permissions')
			dialogs.msg_dialog(self.mw, self.appdata.app_name, msg, sec, details)
			return False
		events.emit(events.APP_STATUS, _('Document saved'))
		return True

	def save_as(self):
		doc_file = '' + self.current_doc.doc_file
		if not doc_file:
			doc_file = '' + self.current_doc.doc_name
		if not os.path.splitext(doc_file)[1] == "." + \
					uc2const.FORMAT_EXTENSION[uc2const.PDXF][0]:
			doc_file = os.path.splitext(doc_file)[0] + "." + \
					uc2const.FORMAT_EXTENSION[uc2const.PDXF][0]
		if not os.path.lexists(os.path.dirname(doc_file)):
			doc_file = os.path.join(config.save_dir,
								os.path.basename(doc_file))
		doc_file = dialogs.get_save_file_name(self.mw, self, doc_file)
		if doc_file:
			old_file = self.current_doc.doc_file
			old_name = self.current_doc.doc_name
			self.current_doc.set_doc_file(doc_file)
			try:
				self.current_doc.save()
			except IOError:
				self.current_doc.set_doc_file(old_file, old_name)
				details = sys.exc_info()[1].__str__() + sys.exc_info()[2].__str__()
				first = _('Cannot save document')
				sec = _('Please check file name and write permissions')
				msg = ("%s '%s'.") % (first, self.current_doc.doc_name)

				dialogs.msg_dialog(self.mw, self.appdata.app_name, msg, sec, details)

				return False
			config.save_dir = os.path.dirname(doc_file)
			events.emit(events.APP_STATUS, _('Document saved'))
			return True
		else:
			return False

	def save_all(self):
		for doc in [] + self.docs:
			self.save(doc)

	def insert_doc(self):
		pass

	def update_config(self):
		config.resource_dir = ''
		w, h = self.mw.get_size()
		state = self.mw.window.get_state()
		if state == gtk.gdk.WINDOW_STATE_MAXIMIZED:
			if config.os != system.MACOSX:
				config.mw_maximized = 1
		else:
			config.mw_maximized = 0

			config.mw_width = w
			config.mw_height = h

	def open_url(self, url):
		import webbrowser
		webbrowser.open_new(url)
