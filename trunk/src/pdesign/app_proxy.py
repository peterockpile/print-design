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

from pdesign.dialogs import msg_dialog

class AppProxy:

	def __init__(self, app):
		self.app = app

	def update(self):
		self.insp = self.app.insp
		self.mw = self.app.mw

	def stub(self, *args):
		msg_dialog(self.mw, self.app.appdata.app_name,
				'Sorry, but this feature is not implemented yet!\n' +
				'Be patient and watch project development of regularly updating the source code!')

	def new(self): self.app.new()
	def open(self): self.app.open()
	def save(self): self.app.save()
	def save_as(self): self.app.save_as()
	def save_all(self): self.app.save_all()
	def close(self): self.app.close()
	def close_all(self): self.app.close_all()
	def exit(self): self.app.exit()

	def set_mode(self, mode): self.app.current_doc.canvas.set_mode(mode)
	def open_url(self, url): self.app.open_url(url)

	def undo(self): self.app.current_doc.api.do_undo()
	def redo(self): self.app.current_doc.api.do_redo()
	def clear_history(self): self.app.current_doc.api.clear_history()
	def cut(self): self.app.current_doc.api.cut_selected()
	def copy(self): self.app.current_doc.api.copy_selected()
	def paste(self): self.app.current_doc.api.paste_selected()
	def delete(self): self.app.current_doc.api.delete_selected()
	def select_all(self): self.app.current_doc.selection.select_all()
	def deselect(self, *args): self.app.current_doc.selection.clear()

	def zoom_in(self): self.app.current_doc.canvas.zoom_in()
	def zoom_out(self): self.app.current_doc.canvas.zoom_out()
	def fit_zoom_to_page(self): self.app.current_doc.canvas.zoom_fit_to_page()
	def zoom_100(self): self.app.current_doc.canvas.zoom_100()
	def zoom_selected(self): self.app.current_doc.canvas.zoom_selected()
	def force_redraw(self): self.app.current_doc.canvas.force_redraw()

	def stroke_view(self):
		if self.insp.is_doc():
			canvas = self.app.current_doc.canvas
			if canvas.stroke_view:
				canvas.stroke_view = False
			else:
				canvas.stroke_view = True
			canvas.force_redraw()

	def draft_view(self):
		if self.insp.is_doc():
			canvas = self.app.current_doc.canvas
			if canvas.draft_view:
				canvas.draft_view = False
				canvas.force_redraw()
			else:
				canvas.draft_view = True
			canvas.force_redraw()

	def show_snapping(self):
		if self.insp.is_doc():
			canvas = self.app.current_doc.canvas
			if canvas.show_snapping:
				canvas.show_snapping = False
			else:
				canvas.show_snapping = True
				self.app.current_doc.snap.active_snap = [None, None]

	def show_grid(self):
		if self.insp.is_doc():
			methods = self.app.current_doc.methods
			api = self.app.current_doc.api
			grid_layer = methods.get_gird_layer()
			if grid_layer.properties[0]:
				prop = [] + grid_layer.properties
				prop[0] = 0
			else:
				prop = [] + grid_layer.properties
				prop[0] = 1
			api.set_layer_properties(grid_layer, prop)

	def show_guides(self):
		if self.insp.is_doc():
			methods = self.app.current_doc.methods
			api = self.app.current_doc.api
			guide_layer = methods.get_guide_layer()
			if guide_layer.properties[0]:
				prop = [] + guide_layer.properties
				prop[0] = 0
			else:
				prop = [] + guide_layer.properties
				prop[0] = 1
			api.set_layer_properties(guide_layer, prop)
			self.app.current_doc.snap.update_guides_grid()

	def snap_to_grid(self):
		if self.insp.is_doc():
			snap = self.app.current_doc.snap
			if snap.snap_to_grid:
				snap.snap_to_grid = False
			else:
				snap.snap_to_grid = True
				snap.update_grid()

	def snap_to_guides(self):
		if self.insp.is_doc():
			snap = self.app.current_doc.snap
			if snap.snap_to_guides:
				snap.snap_to_guides = False
			else:
				snap.snap_to_guides = True
				snap.update_guides_grid()

	def snap_to_objects(self):
		if self.insp.is_doc():
			snap = self.app.current_doc.snap
			if snap.snap_to_objects:
				snap.snap_to_objects = False
			else:
				snap.snap_to_objects = True
				snap.update_objects_grid()

	def snap_to_page(self):
		if self.insp.is_doc():
			snap = self.app.current_doc.snap
			if snap.snap_to_page:
				snap.snap_to_page = False
			else:
				snap.snap_to_page = True
				snap.update_page_grid()

	def draw_page_border(self):
		if self.insp.is_doc():
			canvas = self.app.current_doc.canvas
			if canvas.draw_page_border:
				canvas.draw_page_border = False
			else:
				canvas.draw_page_border = True
			canvas.force_redraw()
