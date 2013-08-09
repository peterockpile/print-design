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

import wx

from pdesign.resources import pdids
from pdesign.pwidgets import AppAction

from pdesign.modes import SELECT_MODE, SHAPER_MODE, ZOOM_MODE, FLEUR_MODE, \
LINE_MODE, CURVE_MODE, RECT_MODE, ELLIPSE_MODE, TEXT_MODE, POLYGON_MODE, \
ZOOM_OUT_MODE
from pdesign.events import CLIPBOARD, DOC_CHANGED, PAGE_CHANGED, \
DOC_CLOSED, DOC_MODIFIED, DOC_SAVED, NO_DOCS, SELECTION_CHANGED, MODE_CHANGED

def create_actions(app):
	# action_id, callback, channels, validator, checker,
	# callable_args, validator_args, checker_args

	doc_chnls = [NO_DOCS, DOC_CHANGED]
	tool_chnls = [NO_DOCS, DOC_CHANGED, MODE_CHANGED]
	doc_save_chnls = [NO_DOCS, DOC_CHANGED, DOC_MODIFIED, DOC_SAVED]
	sel_chnls = [NO_DOCS, DOC_CHANGED, SELECTION_CHANGED]
	insp = app.insp
	proxy = app.proxy
	actions = {}
	entries = [
#----- Canvas modes -----
(pdids.SELECT_MODE, proxy.set_mode, tool_chnls, insp.is_doc, insp.is_mode, [SELECT_MODE], [], [SELECT_MODE]),
(pdids.SHAPER_MODE, proxy.set_mode, tool_chnls, insp.is_doc, insp.is_mode, [SHAPER_MODE], [], [SHAPER_MODE]),
(pdids.ZOOM_MODE, proxy.set_mode, tool_chnls, insp.is_doc, insp.is_mode, [ZOOM_MODE], [], [ZOOM_MODE]),
(pdids.FLEUR_MODE, proxy.set_mode, tool_chnls, insp.is_doc, insp.is_mode, [FLEUR_MODE], [], [FLEUR_MODE]),
(pdids.LINE_MODE, proxy.set_mode, tool_chnls, insp.is_doc, insp.is_mode, [LINE_MODE], [], [LINE_MODE]),
(pdids.CURVE_MODE, proxy.set_mode, tool_chnls, insp.is_doc, insp.is_mode, [CURVE_MODE], [], [CURVE_MODE]),
(pdids.RECT_MODE, proxy.set_mode, tool_chnls, insp.is_doc, insp.is_mode, [RECT_MODE], [], [RECT_MODE]),
(pdids.ELLIPSE_MODE, proxy.set_mode, tool_chnls, insp.is_doc, insp.is_mode, [ELLIPSE_MODE], [], [ELLIPSE_MODE]),
(pdids.TEXT_MODE, proxy.set_mode, tool_chnls, insp.is_doc, insp.is_mode, [TEXT_MODE], [], [TEXT_MODE]),
(pdids.POLYGON_MODE, proxy.set_mode, tool_chnls, insp.is_doc, insp.is_mode, [POLYGON_MODE], [], [POLYGON_MODE]),
(pdids.ZOOM_OUT_MODE, proxy.set_mode, tool_chnls, insp.is_doc, insp.is_mode, [ZOOM_OUT_MODE], [], [ZOOM_OUT_MODE]),

(pdids.FILL_MODE, proxy.stub, doc_chnls, insp.is_doc),
(pdids.STROKE_MODE, proxy.stub, doc_chnls, insp.is_doc),
(pdids.GRADIENT_MODE, proxy.stub, tool_chnls, insp.is_doc),

#------ File menu -------
(wx.ID_NEW, proxy.new),
(wx.ID_OPEN, proxy.open),
(wx.ID_SAVE, proxy.save, doc_save_chnls, insp.is_doc_not_saved),
(wx.ID_SAVEAS, proxy.save_as, doc_chnls, insp.is_doc),
(pdids.ID_SAVEALL, proxy.save_all, doc_save_chnls, insp.is_any_doc_not_saved),
(wx.ID_CLOSE, proxy.close, doc_chnls, insp.is_doc),
(wx.ID_CLOSE_ALL, proxy.close_all, doc_chnls, insp.is_doc),
(wx.ID_PRINT_SETUP, proxy.stub, doc_chnls, insp.is_doc),
(wx.ID_PRINT, proxy.stub, doc_chnls, insp.is_doc),
(wx.ID_EXIT, proxy.exit),
#------ Edit menu -------
(wx.ID_UNDO, proxy.undo, doc_save_chnls, insp.is_undo),
(wx.ID_REDO, proxy.redo, doc_save_chnls, insp.is_redo),
(pdids.ID_CLEAR_UNDO, proxy.clear_history, doc_chnls, insp.is_history),
(wx.ID_CUT, proxy.cut, sel_chnls, insp.is_selection),
(wx.ID_COPY, proxy.copy, sel_chnls, insp.is_selection),
(wx.ID_PASTE, proxy.paste, [NO_DOCS, DOC_CHANGED, CLIPBOARD], insp.is_clipboard),
(wx.ID_DELETE, proxy.delete, sel_chnls, insp.is_selection),
(wx.ID_SELECTALL, proxy.select_all, doc_chnls, insp.is_doc),
(pdids.ID_DESELECT, proxy.deselect, sel_chnls, insp.is_selection),
(wx.ID_PROPERTIES, proxy.stub, doc_chnls, insp.is_doc),
(wx.ID_PREFERENCES, proxy.stub),
#------ View menu -------
(pdids.ID_STROKE_VIEW, proxy.stroke_view, doc_chnls, insp.is_doc, insp.is_stroke_view),
(pdids.ID_DRAFT_VIEW, proxy.draft_view, doc_chnls, insp.is_doc, insp.is_draft_view),
(wx.ID_ZOOM_100, proxy.zoom_100, doc_chnls, insp.is_doc),
(wx.ID_ZOOM_IN, proxy.zoom_in, doc_chnls, insp.is_doc),
(wx.ID_ZOOM_OUT, proxy.zoom_out, doc_chnls, insp.is_doc),
(pdids.ID_ZOOM_PAGE, proxy.fit_zoom_to_page, doc_chnls, insp.is_doc),
(wx.ID_ZOOM_FIT, proxy.zoom_selected, sel_chnls, insp.is_selection),
	(pdids.ID_SHOW_GRID, proxy.show_grid, doc_chnls, insp.is_doc, insp.is_grid_visible),
	(pdids.ID_SHOW_GUIDES, proxy.show_guides, doc_chnls, insp.is_doc, insp.is_guides_visible),
	(pdids.ID_SHOW_SNAP, proxy.show_snapping, doc_chnls, insp.is_doc, insp.is_show_snapping),
	(pdids.ID_SHOW_PAGE_BORDER, proxy.draw_page_border, doc_chnls, insp.is_doc, insp.is_draw_page_border),
	(pdids.ID_SNAP_TO_GRID, proxy.snap_to_grid, doc_chnls, insp.is_doc, insp.is_snap_to_grid),
	(pdids.ID_SNAP_TO_GUIDE, proxy.snap_to_guides, doc_chnls, insp.is_doc, insp.is_snap_to_guides),
	(pdids.ID_SNAP_TO_OBJ, proxy.snap_to_objects, doc_chnls, insp.is_doc, insp.is_snap_to_objects),
	(pdids.ID_SNAP_TO_PAGE, proxy.snap_to_page, doc_chnls, insp.is_doc, insp.is_snap_to_page),
(wx.ID_REFRESH, proxy.force_redraw, doc_chnls, insp.is_doc),
#------ Layout menu -------
(pdids.ID_INSERT_PAGE, proxy.stub),
(pdids.ID_DELETE_PAGE, proxy.stub),
(pdids.ID_GOTO_PAGE, proxy.stub),
(pdids.ID_NEXT_PAGE, proxy.stub),
(pdids.ID_PREV_PAGE, proxy.stub),
#------ Arrange menu -------
(pdids.ID_COMBINE, proxy.combine_selected, sel_chnls, insp.can_be_combined),
(pdids.ID_BREAK_APART, proxy.break_apart_selected, sel_chnls, insp.can_be_breaked),
(pdids.ID_GROUP, proxy.group, sel_chnls, insp.can_be_grouped),
(pdids.ID_UNGROUP, proxy.ungroup, sel_chnls, insp.can_be_ungrouped),
(pdids.ID_UNGROUPALL, proxy.ungroup_all, sel_chnls, insp.can_be_ungrouped_all),
(pdids.ID_TO_CURVES, proxy.convert_to_curve, sel_chnls, insp.can_be_curve),
#------ Effects menu -------
(pdids.ID_TO_CONTAINER, proxy.stub),
(pdids.ID_FROM_CONTAINER, proxy.stub),
#------ Bitmaps menu -------
#------ Text menu -------
(pdids.ID_EDIT_TEXT, proxy.stub),
#------ Tools menu -------
(pdids.ID_TOOL_PAGES, proxy.stub),
(pdids.ID_TOOL_LAYERS, proxy.stub),
(pdids.ID_TOOL_OBJBROWSER, proxy.stub),
#------ Help menu -------
(pdids.ID_REPORT_BUG, proxy.open_url, [], None, None, ('http://sk1project.org/contact.php',)),
(pdids.ID_APP_WEBSITE, proxy.open_url, [], None, None, ('http://sk1project.org',)),
(pdids.ID_APP_FORUM, proxy.open_url, [], None, None, ('http://sk1project.org/forum/index.php',)),
(pdids.ID_APP_FBPAGE, proxy.open_url, [], None, None, ('http://www.facebook.com/pages/sK1-Project/308311182521658',)),
(wx.ID_ABOUT, proxy.stub),
	]
# action_id, callback, channels, validator, checker,
# callable_args, validator_args, checker_args
	for entry in entries:
		actions[entry[0]] = AppAction(*entry)

	return actions
