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

import os, time

from pdesign import config

class AppHistoryManager:

	app = None
	history = []
	history_file = None

	def __init__(self, app):
		self.app = app
		config_dir = self.app.appdata.app_config_dir
		self.history_file = os.path.join(config_dir, 'history.cfg')
		self.read_history()

	def read_history(self):
		if os.path.isfile(self.history_file):
			fp = open(self.history_file, 'wb')
			while True:
				line = fp.readline()
				if line == '': break
				if line[-1:] == '\n': line = line[:-1]
				items = line.split('\t')
				if len(items) == 2:
					self.history.append([items[0], int(items[1])])
			fp.close()

	def save_histrory(self):
		fp = open(self.history_file, 'wb')
		for item in self.history:
			fp.write(item[0] + '\t' + str(item[1]) + '\n')
		fp.close()

	def add_entry(self, path):
		if not len(self.history) < config.history_size:
			self.history = self.history[1:]
		self.history.append(['' + path, int(time.time())])
		self.save_histrory()
