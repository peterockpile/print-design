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

ICON_SIZES = [16, 22, 24, 32, 48, 64, 128]

PD_NEW = 'gtk-new'
PD_OPEN = 'gtk-open'
PD_FILE_SAVE = 'gtk-save'
PD_FILE_SAVE_AS = 'gtk-save-as'
PD_CLOSE = 'gtk-close'
PD_PRINT_PREVIEW = 'gtk-print-preview'
PD_PRINT = 'gtk-print'
PD_QUIT = 'gtk-quit'
PD_UNDO = 'gtk-undo'
PD_REDO = 'gtk-redo'
PD_CUT = 'gtk-cut'
PD_COPY = 'gtk-copy'
PD_PASTE = 'gtk-paste'
PD_DELETE = 'gtk-delete'
PD_SELECTALL = 'gtk-select-all'
PD_PROPERTIES = 'gtk-properties'
PD_PREFERENCES = 'gtk-preferences'
PD_ZOOM_100 = 'gtk-zoom-100'
PD_ZOOM_IN = 'gtk-zoom-in'
PD_ZOOM_OUT = 'gtk-zoom-out'
PD_ZOOM_PAGE = 'gtk-zoom-page'
PD_ZOOM_FIT = 'gtk-zoom-fit'
PD_REFRESH = 'gtk-refresh'
PD_TO_CURVES = 'pdesign-to-curves'
PD_TOOL_PAGES = 'pdesign-tool-pages'
PD_TOOL_LAYERS = 'pdesign-tool-layers'
PD_TOOL_OBJBROWSER = 'pdesign-tool-objbrowser'
PD_WARNING = 'gtk-dialog-warning'
PD_HOME = 'gtk-home'
PD_FBPAGE = 'pdesign-fb'
PD_ABOUT = 'gtk-about'

ORIGIN_CENTER = 'origin-center'
ORIGIN_LL = 'origin-ll'
ORIGIN_LU = 'origin-lu'

PD_CLOSE_BUTTON = 'pdesign-close-button'
PD_CLOSE_BUTTON_ACTIVE = 'pdesign-close-button-active'
PD_MOUSE_MONITOR = 'mouse-monitor'
PD_APP_STATUS = 'app-status'
PD_PM_ARROW_END = "pager-arrow-end"
PD_PM_ARROW_LEFT = "pager-arrow-left"
PD_PM_ARROW_RIGHT = "pager-arrow-right"
PD_PM_ARROW_START = "pager-arrow-start"

#----- MacOS X specific bitmaps
MAC_TBB_NORMAL = 'tbb-normal'
MAC_TBB_PRESSED = 'tbb-pressed'
MAC_TBNB_LEFT_NORMAL = 'tbnb-left-normal'
MAC_TBNB_LEFT_PRESSED = 'tbnb-left-pressed'
MAC_TBNB_MIDDLE_NORMAL = 'tbnb-middle-normal'
MAC_TBNB_MIDDLE_PRESSED = 'tbnb-middle-pressed'
MAC_TBNB_RIGHT_NORMAL = 'tbnb-right-normal'
MAC_TBNB_RIGHT_PRESSED = 'tbnb-right-pressed'
MAC_TBNB_SPACER_ACTIVE = 'tbnb-spacer-active'
MAC_TBNB_SPACER_NORMAL = 'tbnb-spacer-normal'

ICON_MATCH = {
	wx.ART_NEW:PD_NEW,
	wx.ART_FILE_OPEN:PD_OPEN,
	wx.ART_FILE_SAVE:PD_FILE_SAVE,
	wx.ART_FILE_SAVE_AS:PD_FILE_SAVE_AS,
	wx.ART_PRINT:PD_PRINT,
	wx.ART_QUIT:PD_QUIT,
	wx.ART_UNDO:PD_UNDO,
	wx.ART_REDO:PD_REDO,
	wx.ART_CUT:PD_CUT,
	wx.ART_COPY:PD_COPY,
	wx.ART_PASTE:PD_PASTE,
	wx.ART_DELETE:PD_DELETE,
	wx.ART_WARNING:PD_WARNING,
	}

PDESIGN_ICON16 = 'pdesign-icon-16x16'
PDESIGN_ICON22 = 'pdesign-icon-22x22'
PDESIGN_ICON32 = 'pdesign-icon-32x32'
PDESIGN_ICON48 = 'pdesign-icon-48x48'
PDESIGN_ICON64 = 'pdesign-icon-64x64'
PDESIGN_ICON128 = 'pdesign-icon-128x128'
CAIRO_BANNER = 'cairo-banner'
DOCUMENT_ICON = 'document-icon'
ARROW_LEFT = 'arrow-left'
ARROW_RIGHT = 'arrow-right'
DOUBLE_ARROW_LEFT = 'double-arrow-left'
DOUBLE_ARROW_RIGHT = 'double-arrow-right'
NO_COLOR = 'no-color'

GENERICS = [PDESIGN_ICON16, PDESIGN_ICON22, PDESIGN_ICON32, PDESIGN_ICON48,
		PDESIGN_ICON64, PDESIGN_ICON64,
		CAIRO_BANNER, DOCUMENT_ICON, ARROW_LEFT, ARROW_RIGHT,
		DOUBLE_ARROW_LEFT, DOUBLE_ARROW_RIGHT, NO_COLOR, PD_TO_CURVES,
		PD_TOOL_PAGES, PD_TOOL_LAYERS, PD_TOOL_OBJBROWSER, PD_FBPAGE,
		PD_CLOSE_BUTTON, PD_CLOSE_BUTTON_ACTIVE, ORIGIN_CENTER, ORIGIN_LL,
		ORIGIN_LU, PD_MOUSE_MONITOR, PD_PM_ARROW_END, PD_PM_ARROW_LEFT,
		PD_PM_ARROW_RIGHT, PD_PM_ARROW_START, PD_APP_STATUS]

TOOL_CREATE_CURVE = 'tool-create-curve'
TOOL_CREATE_ELLIPSE = 'tool-create-ellipse'
TOOL_CREATE_POLY = 'tool-create-poly'
TOOL_CREATE_POLYGON = 'tool-create-polygon'
TOOL_CREATE_RECT = 'tool-create-rect'
TOOL_CREATE_TEXT = 'tool-create-text'
TOOL_FILL = 'tool-fill'
TOOL_FLEUR = 'tool-fleur'
TOOL_GRADIENT = 'tool-gradient'
TOOL_SELECT = 'tool-select'
TOOL_SHAPER = 'tool-shaper'
TOOL_STROKE = 'tool-stroke'
TOOL_ZOOM = 'tool-zoom'

TOOLS_ICONS = [TOOL_CREATE_CURVE, TOOL_CREATE_ELLIPSE, TOOL_CREATE_POLY,
	TOOL_CREATE_POLYGON, TOOL_CREATE_RECT, TOOL_CREATE_TEXT, TOOL_FILL,
	TOOL_FLEUR, TOOL_GRADIENT, TOOL_SELECT, TOOL_SHAPER, TOOL_STROKE,
	TOOL_ZOOM, ]

CTX_PAGE_LANDSCAPE = 'ctx-page-landscape'
CTX_PAGE_PORTRAIT = 'ctx-page-portrait'
CTX_UNITS = 'ctx-units'
CTX_OBJECT_JUMP = 'ctx-object-jump'

CTX_ICONS = [CTX_PAGE_LANDSCAPE, CTX_PAGE_PORTRAIT, CTX_UNITS, CTX_OBJECT_JUMP]

GENERIC_ICONS = TOOLS_ICONS + GENERICS + CTX_ICONS



