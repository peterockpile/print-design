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

class AppInspector:

	def __init__(self, app):
		self.app = app

	def update(self):
		self.mw = self.app.mw

	def stub(self, *args):return False

	def is_doc(self): return not self.app.docs == []
	def is_not_doc(self): return self.app.docs == []

	def is_doc_saved(self, doc=None):
		if doc: return doc.saved
		elif self.app.current_doc: return self.app.current_doc.saved
		else: return True

	def is_doc_not_saved(self, doc=None):
		return self.is_doc_saved(doc) != True

	def is_any_doc_not_saved(self):
		ret = False
		if self.app.docs:
			for doc in self.app.docs:
				if not doc.saved: ret = True
		return ret

	def is_mode(self, mode):
		if self.is_not_doc(): return False
		if mode == self.app.current_doc.canvas.mode: return True
		return False

	def is_undo(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		if doc.api.undo:
			return True
		else:
			return False

	def is_redo(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		if doc.api.redo:
			return True
		else:
			return False

	def is_history(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		if self.is_undo(doc) or self.is_redo(doc):
			return True
		else:
			return False

	def is_selection(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		elif doc.selection is None:
			return False
		elif doc.selection.objs:
			return True
		else:
			return False

	def is_clipboard(self):
		if self.app.clipboard.contents:
			return True
		else:
			return False

	def is_draft_view(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		return self.app.current_doc.canvas.draft_view

	def is_stroke_view(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		print 'is_stroke_view', self.app.current_doc.canvas.stroke_view
		return self.app.current_doc.canvas.stroke_view

	def is_guides_visible(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		methods = self.app.current_doc.methods
		guide_layer = methods.get_guide_layer()
		if guide_layer.properties[0]: return True
		return False

	def is_grid_visible(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		methods = self.app.current_doc.methods
		grid_layer = methods.get_gird_layer()
		if grid_layer.properties[0]: return True
		return False

	def is_draw_page_border(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		return self.app.current_doc.canvas.draw_page_border

	def is_show_snapping(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		return self.app.current_doc.canvas.show_snapping

	def is_snap_to_grid(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		return self.app.current_doc.snap.snap_to_grid

	def is_snap_to_guides(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		return self.app.current_doc.snap.snap_to_guides

	def is_snap_to_objects(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		return self.app.current_doc.snap.snap_to_objects

	def is_snap_to_page(self, doc=None):
		if doc is None: doc = self.app.current_doc
		if doc is None: return False
		return self.app.current_doc.snap.snap_to_page
