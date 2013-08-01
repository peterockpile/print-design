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

	def new(self, *args): self.app.new()
	def open(self, *args): self.app.open()
	def save(self, *args): self.app.save()
	def save_as(self, *args): self.app.save_as()
	def save_all(self, *args): self.app.save_all()
	def close(self, *args): self.app.close()
	def close_all(self, *args): self.app.close_all()
	def exit(self, *args): self.app.exit()

	def set_mode(self, mode): self.app.current_doc.canvas.set_mode(mode)
	def open_url(self, url): self.app.open_url(url)

	def undo(self, *args): self.app.current_doc.api.do_undo()
	def redo(self, *args): self.app.current_doc.api.do_redo()
	def clear_history(self, *args): self.app.current_doc.api.clear_history()
	def cut(self, *args): self.app.current_doc.api.cut_selected()
	def copy(self, *args): self.app.current_doc.api.copy_selected()
	def paste(self, *args): self.app.current_doc.api.paste_selected()
	def delete(self, *args): self.app.current_doc.api.delete_selected()
	def select_all(self, *args): self.app.current_doc.selection.select_all()
	def deselect(self, *args): self.app.current_doc.selection.clear()

	def zoom_in(self, *args): self.app.current_doc.canvas.zoom_in()
	def zoom_out(self, *args): self.app.current_doc.canvas.zoom_out()
	def fit_zoom_to_page(self, *args): self.app.current_doc.canvas.zoom_fit_to_page()
	def zoom_100(self, *args): self.app.current_doc.canvas.zoom_100()
	def zoom_selected(self, *args): self.app.current_doc.canvas.zoom_selected()
	def force_redraw(self, *args): self.app.current_doc.canvas.force_redraw()

	def stroke_view(self, *args):
		if self.insp.is_doc():
			canvas = self.app.current_doc.canvas
			if canvas.stroke_view:
				canvas.stroke_view = False
			else:
				canvas.stroke_view = True
			canvas.force_redraw()
