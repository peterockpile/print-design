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

import os
import wx

from uc2 import uc2const
from uc2.formats import data

from pdesign import _
from pdesign.utils.fs import expanduser_unicode

def _get_open_filters():
	wildcard = ''
	descr = uc2const.FORMAT_DESCRIPTION
	ext = uc2const.FORMAT_EXTENSION
	items = [] + data.LOADER_FORMATS
	wildcard += _('All supported formats') + '|'
	for item in items:
		for extension in ext[item]:
			wildcard += '*.' + extension + ';'
			wildcard += '*.' + extension.upper() + ';'
	wildcard += '|'

	wildcard += _('All files (*.*)') + '|'
	wildcard += '*;*.*|'

	for item in items:
		wildcard += descr[item] + '|'
		for extension in ext[item]:
			wildcard += '*.' + extension + ';'
			wildcard += '*.' + extension.upper() + ';'
		wildcard += '|'

	return wildcard

def get_open_file_name(parent, app, start_dir):
	ret = ''
	msg = _('Open document')

	start_dir = expanduser_unicode(start_dir)

	dlg = wx.FileDialog(
		parent, message=msg,
		defaultDir=start_dir,
		defaultFile="",
		wildcard=_get_open_filters(),
		style=wx.OPEN | wx.CHANGE_DIR | wx.FILE_MUST_EXIST
		)
	dlg.CenterOnParent()
	if dlg.ShowModal() == wx.ID_OK:
		ret = dlg.GetPath()
	dlg.Destroy()
	return ret

def _get_save_fiters():
	wildcard = ''
	descr = uc2const.FORMAT_DESCRIPTION
	ext = uc2const.FORMAT_EXTENSION
	items = [] + data.SAVER_FORMATS
	for item in items:
		wildcard += descr[item] + '|'
		for extension in ext[item]:
			wildcard += '*.' + extension + ';'
			wildcard += '*.' + extension.upper() + ';'
		wildcard += '|'
	return wildcard

def get_save_file_name(parent, app, path):
	ret = ''
	msg = _('Save document As...')

	path = expanduser_unicode(path)
	doc_folder = os.path.dirname(path)

	dlg = wx.FileDialog(
		parent, message=msg,
		defaultDir=doc_folder,
		defaultFile=path,
		wildcard=_get_save_fiters(),
		style=wx.SAVE | wx.CHANGE_DIR | wx.FD_OVERWRITE_PROMPT
	)
	dlg.CenterOnParent()
	if dlg.ShowModal() == wx.ID_OK:
		ret = dlg.GetPath()
	dlg.Destroy()
	return ret
