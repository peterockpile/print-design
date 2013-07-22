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

GENERIC_KEYS = {
#----- File menu
wx.ID_NEW:(wx.ACCEL_CTRL, ord('N'), wx.ID_NEW),
wx.ID_OPEN:(wx.ACCEL_CTRL, ord('O'), wx.ID_OPEN),
wx.ID_SAVE:(wx.ACCEL_CTRL, ord('S'), wx.ID_SAVE),
wx.ID_CLOSE:(wx.ACCEL_CTRL, ord('W'), wx.ID_CLOSE),
wx.ID_PRINT:(wx.ACCEL_CTRL, ord('P'), wx.ID_PRINT),
wx.ID_EXIT:(wx.ACCEL_CTRL, ord('Q'), wx.ID_EXIT),
#----- Edit menu
wx.ID_UNDO:(wx.ACCEL_CTRL, ord('Z'), wx.ID_UNDO),
wx.ID_REDO:(wx.ACCEL_SHIFT | wx.ACCEL_CTRL, ord('Z'), wx.ID_REDO),
wx.ID_CUT:(wx.ACCEL_CTRL, ord('X'), wx.ID_CUT),
wx.ID_COPY:(wx.ACCEL_CTRL, ord('C'), wx.ID_COPY),
wx.ID_PASTE:(wx.ACCEL_CTRL, ord('V'), wx.ID_PASTE),
wx.ID_DELETE:(wx.ACCEL_NORMAL, wx.WXK_DELETE, wx.ID_DELETE),
wx.ID_SELECTALL:(wx.ACCEL_CTRL, ord('A'), wx.ID_SELECTALL),
#----- View menu
pdids.ID_DESELECT:(wx.ACCEL_SHIFT | wx.ACCEL_CTRL, ord('A'), pdids.ID_DESELECT),
pdids.ID_STROKE_VIEW:(wx.ACCEL_SHIFT, wx.WXK_F9, pdids.ID_STROKE_VIEW),
wx.ID_ZOOM_IN:(wx.ACCEL_CTRL, ord('='), wx.ID_ZOOM_IN),
wx.ID_ZOOM_OUT:(wx.ACCEL_CTRL, ord('-'), wx.ID_ZOOM_OUT),
pdids.ID_ZOOM_PAGE:(wx.ACCEL_SHIFT, wx.WXK_F4, pdids.ID_ZOOM_PAGE),
wx.ID_ZOOM_FIT:(wx.ACCEL_NORMAL, wx.WXK_F4, wx.ID_ZOOM_FIT),
wx.ID_REFRESH:(wx.ACCEL_ALT, ord('R'), wx.ID_REFRESH),
#----- Layout menu
pdids.ID_NEXT_PAGE:(wx.ACCEL_NORMAL, wx.WXK_PAGEDOWN, pdids.ID_NEXT_PAGE),
pdids.ID_PREV_PAGE:(wx.ACCEL_NORMAL, wx.WXK_PAGEUP, pdids.ID_PREV_PAGE),
#----- Arrange menu
pdids.ID_COMBINE:(wx.ACCEL_CTRL, ord('L'), pdids.ID_COMBINE),
pdids.ID_BREAK_APART:(wx.ACCEL_CTRL, ord('K'), pdids.ID_BREAK_APART),
pdids.ID_GROUP:(wx.ACCEL_CTRL, ord('G'), pdids.ID_GROUP),
pdids.ID_UNGROUP:(wx.ACCEL_CTRL, ord('U'), pdids.ID_UNGROUP),
pdids.ID_TO_CURVES:(wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('Q'), pdids.ID_TO_CURVES),
#----- Text menu
pdids.ID_EDIT_TEXT:(wx.ACCEL_NORMAL, wx.WXK_F8, pdids.ID_EDIT_TEXT),
#----- Tools menu
pdids.ID_TOOL_PAGES:(wx.ACCEL_SHIFT, wx.WXK_F7, pdids.ID_TOOL_PAGES),
pdids.ID_TOOL_LAYERS:(wx.ACCEL_NORMAL, wx.WXK_F7, pdids.ID_TOOL_LAYERS),
}
