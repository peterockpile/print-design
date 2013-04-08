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

import math

from pdesign import dialogs
from pdesign import modes, config
from pdesign.dialogs import prefs

class AppProxy:

	app = None
	mw = None
	stroke_view_flag = False
	draft_view_flag = False

	def __init__(self, app):
		self.app = app
		self.insp = app.inspector

	def stub(self, *args):pass

	def stubd(self, *args):
		dialogs.about_dialog(self.mw)

	def update_references(self):
		self.mw = self.app.mw

	def exit(self, *args):
		self.app.exit()

	def new(self, *args):
		self.app.new()

	def open(self, *args):
		self.app.open()

	def import_image(self, *args):
		self.app.import_image()

	def save(self, *args):
		self.app.save()

	def save_as(self, *args):
		self.app.save_as()

	def save_all(self, *args):
		self.app.save_all()

	def close(self, *args):
		self.app.close()

	def close_all(self, *args):
		self.app.close_all()

	def insert_doc(self, *args):
		self.app.insert_doc()

	def do_print(self, *args):
		pass

	def do_print_setup(self, *args):
		pass

	def undo(self, *args):
		self.app.current_doc.api.do_undo()

	def redo(self, *args):
		self.app.current_doc.api.do_redo()

	def clear_history(self, *args):
		self.app.current_doc.api.clear_history()

	def cut(self, *args):
		self.app.current_doc.api.cut_selected()

	def copy(self, *args):
		self.app.current_doc.api.copy_selected()

	def paste(self, *args):
		self.app.current_doc.api.paste_selected()

	def delete(self, *args):
		self.app.current_doc.api.delete_selected()

	def select_all(self, *args):
		self.app.current_doc.selection.select_all()

	def deselect(self, *args):
		self.app.current_doc.selection.clear()

	def stroke_view(self, action):
		if self.insp.is_doc():
			canvas = self.app.current_doc.canvas
			if canvas.stroke_view and not action.get_active():
				canvas.stroke_view = False
				canvas.force_redraw()
				return
			if not canvas.stroke_view and action.get_active():
				canvas.stroke_view = True
				canvas.force_redraw()
				return

	def draft_view(self, action):
		if self.insp.is_doc():
			canvas = self.app.current_doc.canvas
			if canvas.draft_view and not action.get_active():
				canvas.draft_view = False
				canvas.force_redraw()
				return
			if not canvas.draft_view and action.get_active():
				canvas.draft_view = True
				canvas.force_redraw()
				return

	def snap_to_grid(self, action):
		if self.insp.is_doc():
			snap = self.app.current_doc.snap
			if snap.snap_to_grid and not action.get_active():
				snap.snap_to_grid = False
				return
			if not snap.snap_to_grid and action.get_active():
				snap.snap_to_grid = True
				return

	def snap_to_guides(self, action):
		if self.insp.is_doc():
			snap = self.app.current_doc.snap
			if snap.snap_to_guides and not action.get_active():
				snap.snap_to_guides = False
				return
			if not snap.snap_to_guides and action.get_active():
				snap.snap_to_guides = True
				return

	def snap_to_objects(self, action):
		if self.insp.is_doc():
			snap = self.app.current_doc.snap
			if snap.snap_to_objects and not action.get_active():
				snap.snap_to_objects = False
				return
			if not snap.snap_to_objects and action.get_active():
				snap.snap_to_objects = True
				return

	def snap_to_page(self, action):
		if self.insp.is_doc():
			snap = self.app.current_doc.snap
			if snap.snap_to_page and not action.get_active():
				snap.snap_to_page = False
				return
			if not snap.snap_to_page and action.get_active():
				snap.snap_to_page = True
				return

	def zoom_in(self, *args):
		self.app.current_doc.canvas.zoom_in()

	def zoom_out(self, *args):
		self.app.current_doc.canvas.zoom_out()

	def fit_zoom_to_page(self, *args):
		self.app.current_doc.canvas.zoom_fit_to_page()

	def zoom_100(self, *args):
		self.app.current_doc.canvas.zoom_100()

	def zoom_selected(self, *args):
		self.app.current_doc.canvas.zoom_selected()

	def force_redraw(self, *args):
		self.app.current_doc.canvas.force_redraw()

	def properties(self, *args):
		pass

	def preferences(self, *args):
		prefs.get_prefs_dialog(self.app)

	def report_bug(self, *args):
		self.app.open_url('http://www.sk1project.org/contact.php')

	def project_website(self, *args):
		self.app.open_url('http://www.sk1project.org/')

	def project_forum(self, *args):
		self.app.open_url('http://www.sk1project.org/forum/index.php')

	def about(self, *args):
		dialogs.about_dialog(self.mw)

	#----Canvas modes

	def set_select_mode(self, *args):
		self.app.current_doc.canvas.set_mode(modes.SELECT_MODE)

	def set_shaper_mode(self, *args):
		self.app.current_doc.canvas.set_mode(modes.SHAPER_MODE)

	def set_zoom_mode(self, *args):
		self.app.current_doc.canvas.set_mode(modes.ZOOM_MODE)

	def set_fleur_mode(self, *args):
		self.app.current_doc.canvas.set_mode(modes.FLEUR_MODE)

	def set_line_mode(self, *args):
		self.app.current_doc.canvas.set_mode(modes.LINE_MODE)

	def set_curve_mode(self, *args):
		self.app.current_doc.canvas.set_mode(modes.CURVE_MODE)

	def set_rect_mode(self, *args):
		self.app.current_doc.canvas.set_mode(modes.RECT_MODE)

	def set_ellipse_mode(self, *args):
		self.app.current_doc.canvas.set_mode(modes.ELLIPSE_MODE)

	def set_text_mode(self, *args):
		self.app.current_doc.canvas.set_mode(modes.TEXT_MODE)

	def set_polygon_mode(self, *args):
		self.app.current_doc.canvas.set_mode(modes.POLYGON_MODE)

	def set_zoom_out_mode(self, *args):
		self.app.current_doc.canvas.set_mode(modes.ZOOM_OUT_MODE)

	def set_move_mode(self, *args):
		self.app.current_doc.canvas.set_mode(modes.MOVE_MODE)

	def set_copy_mode(self, *args):
		self.app.current_doc.canvas.set_mode(modes.COPY_MODE)

	#-------

	def fill_selected(self, color):
		if self.app.current_doc is None:
			#FIXME: here should be default style changing
			pass
		else:
			self.app.current_doc.api.fill_selected(color)

	def stroke_selected(self, color):
		if self.app.current_doc is None:
			#FIXME: here should be default style changing
			pass
		else:
			self.app.current_doc.api.stroke_selected(color)

	def convert_to_curve(self, *args):
		self.app.current_doc.api.convert_to_curve_selected()

	def group(self, *args):
		self.app.current_doc.api.group_selected()

	def ungroup(self, *args):
		self.app.current_doc.api.ungroup_selected()

	def ungroup_all(self, *args):
		self.app.current_doc.api.ungroup_all()

	def edit_text(self, *args):
		self.app.current_doc.api.edit_text()

	def set_container(self, *args):
		self.app.current_doc.api.select_container()

	def unpack_container(self, *args):
		self.app.current_doc.api.unpack_container()

	def combine_selected(self, *args):
		self.app.current_doc.api.combine_selected()

	def break_apart_selected(self, *args):
		self.app.current_doc.api.break_apart_selected()

	def rotate_left(self, *args):
		self.app.current_doc.api.rotate_selected(math.pi / 2.0)

	def rotate_right(self, *args):
		self.app.current_doc.api.rotate_selected(-math.pi / 2.0)

	def vertical_mirror(self, *args):
		self.app.current_doc.api.mirror_selected()

	def horizontal_mirror(self, *args):
		self.app.current_doc.api.mirror_selected(False)

	#---Page management
	def next_page(self, *args):
		doc = self.app.current_doc
		pages = doc.get_pages()
		if pages.index(doc.active_page) < len(pages) - 1:
			self.app.current_doc.next_page()
		else:
			self.insert_page()

	def previous_page(self, *args):
		self.app.current_doc.previous_page()

	def delete_page(self, *args):
		index = dialogs.delete_page_dialog(self.mw, self.app.current_doc)
		if index >= 0:
			self.app.current_doc.api.delete_page(index)

	def insert_page(self, *args):
		ret = dialogs.insert_page_dialog(self.mw, self.app.current_doc)
		if ret:
			self.app.current_doc.api.insert_page(*ret)

	def goto_page(self, *args):
		index = dialogs.goto_page_dialog(self.mw, self.app.current_doc)
		if index >= 0:
			self.app.current_doc.goto_page(index)

	#---Canvas actions		

	def move_up(self, *args):
		if self.insp.is_selection():
			self.app.current_doc.api.move_selected(0, config.obj_jump)

	def move_down(self, *args):
		if self.insp.is_selection():
			self.app.current_doc.api.move_selected(0, -1.0 * config.obj_jump)

	def move_left(self, *args):
		if self.insp.is_selection():
			self.app.current_doc.api.move_selected(-1.0 * config.obj_jump, 0)

	def move_right(self, *args):
		if self.insp.is_selection():
			self.app.current_doc.api.move_selected(config.obj_jump, 0)

	#---Tools
	def load_layers_plg(self, *args):
		self.app.mw.plugin_panel.load_plugin('LayersPlugin')
	def load_pages_plg(self, *args):
		self.app.mw.plugin_panel.load_plugin('PagesPlugin')
	def load_dom_plg(self, *args):
		self.app.mw.plugin_panel.load_plugin('DOMPlugin')


