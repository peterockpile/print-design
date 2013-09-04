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

from generic import CtxPlugin
from page_format import PagePlugin
from units import UnitsPlugin
from jump import JumpPlugin
from resize import ResizePlugin
from transform import RotatePlugin, MirrorPlugin
from combine import GroupPlugin, CombinePlugin, ToCurvePlugin

PLUGINS = [PagePlugin, UnitsPlugin, JumpPlugin, ResizePlugin, RotatePlugin,
		 MirrorPlugin, GroupPlugin, CombinePlugin, ToCurvePlugin]

NO_DOC = []
DEFAULT = ['PagePlugin', 'UnitsPlugin', 'JumpPlugin', ]
MULTIPLE = ['ResizePlugin', 'CombinePlugin', 'GroupPlugin', 'RotatePlugin',
		'MirrorPlugin', 'ToCurvePlugin']
GROUP = ['ResizePlugin', 'GroupPlugin', 'RotatePlugin', 'MirrorPlugin',
		'ToCurvePlugin']
RECTANGLE = ['ResizePlugin', 'RotatePlugin', 'MirrorPlugin', 'ToCurvePlugin']
CIRCLE = ['ResizePlugin', 'RotatePlugin', 'MirrorPlugin', 'ToCurvePlugin' ]
POLYGON = ['ResizePlugin', 'RotatePlugin', 'MirrorPlugin', 'ToCurvePlugin' ]
CURVE = ['ResizePlugin', 'CombinePlugin', 'RotatePlugin', 'MirrorPlugin', ]
TEXT = ['ResizePlugin', 'RotatePlugin', 'MirrorPlugin', 'ToCurvePlugin' ]
PIXMAP = ['ResizePlugin', 'RotatePlugin', 'MirrorPlugin', ]
