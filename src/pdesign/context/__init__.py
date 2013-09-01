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

from generic import CtxPlugin, PL1, PL2, PL3
from page_format import PagePlugin
from units import UnitsPlugin

PLUGINS = [PagePlugin, UnitsPlugin, PL1, PL2, PL3]

NO_DOC = []
DEFAULT = ['PagePlugin', 'UnitsPlugin', 'Plugin_1', ]
MULTIPLE = ['Plugin_2', 'Plugin_3', ]
GROUP = ['Plugin_3', ]
RECTANGLE = []
CIRCLE = []
POLYGON = []
CURVE = []
TEXT = []
PIXMAP = []
