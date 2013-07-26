#
# -*- coding: utf-8 -*-
#
# 	Copyright (C) 2013 by Igor E. Novikov
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU General Public License as published by
# 	the Free Software Foundation, either version 3 of the License, or
# 	(at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU General Public License for more details.
#
# 	You should have received a copy of the GNU General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, sys

from uc2 import uc2const
from uc2.application import UCApplication

from pdesign import _, config, events, app_actions, modes, dialogs
from pdesign.app_conf import AppData
from pdesign.app_insp import AppInspector
from pdesign.app_proxy import AppProxy
from pdesign.parts.mw import AppMainWindow
from pdesign.parts.artprovider import create_artprovider
from pdesign.widgets import Application
from pdesign.app_cms import AppColorManager
from pdesign.document import PD_Presenter

class pdApplication(Application, UCApplication):

	appdata = None

	actions = {}
	docs = []
	current_doc = None
	doc_counter = 0

	proxy = None
	inspector = None
	cursors = None

	def __init__(self, path):

		self.path = path

		Application.__init__(self)
		UCApplication.__init__(self, path)

		self.appdata = AppData()
		config.load(self.appdata.app_config)
		config.resource_dir = os.path.join(self.path, 'share')

		create_artprovider()
		self.cursors = modes.get_cursors()

		self.proxy = AppProxy(self)
		self.insp = AppInspector(self)
		self.mw = AppMainWindow(self)
		self.default_cms = AppColorManager(self)

		self.actions = app_actions.create_actions(self)

		self.proxy.update()
		self.insp.update()

	def call_after(self, *args):
		if not self.docs: events.emit(events.NO_DOCS)
		txt = _('To start create new document or open existing')
		events.emit(events.APP_STATUS, txt)

	def stub(self, *args):pass

	def get_new_docname(self):
		self.doc_counter += 1
		return _('Untitled') + ' ' + str(self.doc_counter)

	def set_current_doc(self, doc):
		self.current_doc = doc
		events.emit(events.DOC_CHANGED, doc)

	def new(self):
		doc = PD_Presenter(self)
		self.docs.append(doc)
		self.set_current_doc(doc)
		events.emit(events.APP_STATUS, _('New document created'))

	def close(self, doc=None):
		if not doc: doc = self.current_doc
		if not doc: return
		doc.close()
		self.docs.remove(doc)
		if doc == self.current_doc:
			if self.docs:
				self.set_current_doc(self.docs[-1])
			else:
				self.current_doc = None
				events.emit(events.NO_DOCS)
				msg = _('To start create new or open existing document')
				events.emit(events.APP_STATUS, msg)

	def close_all(self):
		result = True
		if self.docs:
			while self.docs:
				result = self.close(self.docs[0])
				if not result:
					break
		return result

	def open(self, doc_file='', silent=True):
		if not doc_file:
			doc_file = dialogs.get_open_file_name(self.mw, self, config.open_dir)
		if os.path.lexists(doc_file) and os.path.isfile(doc_file):
			try:
				doc = PD_Presenter(self, doc_file, silent)
			except:
				msg = _('Cannot open file')
				msg = "%s '%s'" % (msg, doc_file) + '\n'
				msg += _('The file may be corrupted or not supported format')
				dialogs.msg_dialog(self.mw, self.appdata.app_name, msg)
				if config.print_stacktrace:
					print sys.exc_info()[1].__str__()
					print sys.exc_info()[2].__str__()
				return
			self.docs.append(doc)
			self.set_current_doc(doc)
			config.open_dir = os.path.dirname(doc_file)
			events.emit(events.APP_STATUS, _('Document opened'))

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
			msg = _('Cannot save file')
			msg = "%s '%s'" % (msg, self.current_doc.doc_file) + '\n'
			msg += _('Please check file write permissions')
			dialogs.msg_dialog(self.mw, self.appdata.app_name, msg)
			if config.print_stacktrace:
				print sys.exc_info()[1].__str__()
				print sys.exc_info()[2].__str__()
			return False
		events.emit(events.APP_STATUS, _('Document saved'))
		return True

	def exit(self):
		if self.close_all():
			self.update_config()
			config.save(self.appdata.app_config)
			self.mw.Destroy()
			self.Exit()
			return True
		return False

	def update_config(self):
		config.resource_dir = ''
		w, h = self.mw.GetSize()
		config.mw_width = w
		config.mw_height = h

	def open_url(self, url):
		import webbrowser
		webbrowser.open_new(url)
