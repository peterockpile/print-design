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


from pdesign import modes
from pdesign.appconst import RENDERING_DELAY

class AbstractController:

	draw = False
	canvas = None
	snap = None
	start = []
	end = []
	start_doc = []
	end_doc = []
	check_snap = False

	counter = 0
	timer = None

	mode = None

	def __init__(self, canvas, presenter):
		self.canvas = canvas
		self.app = presenter.app
		self.presenter = presenter
		self.selection = presenter.selection
		self.eventloop = presenter.eventloop
		self.api = presenter.api
		self.start = []
		self.end = []
		self.start_doc = []
		self.end_doc = []
		self.timer = self.canvas.timer

	def set_cursor(self):
		if self.mode is None:
			self.canvas.set_canvas_cursor(self.canvas.mode)
		else:
			self.canvas.set_canvas_cursor(self.mode)

	def start_(self):pass
	def stop_(self):pass
	def standby(self):pass
	def restore(self):pass
	def do_action(self, event): return True
	def mouse_double_click(self, event): pass
	def mouse_right_down(self, event):
		if event.ControlDown():
			self.canvas.set_temp_mode(modes.TEMP_FLEUR_MODE)
	def mouse_right_up(self, event):pass
	def mouse_middle_down(self, event):
		self.canvas.set_temp_mode(modes.TEMP_FLEUR_MODE)
	def mouse_middle_up(self, event):pass
	def wheel(self, event):pass

	def mouse_down(self, event):
		self.snap = self.presenter.snap
		self.start = []
		self.end = []
		self.start_doc = []
		self.end_doc = []
		self.counter = 0
		if self.timer.IsRunning(): self.timer.Stop()

		self.draw = True
		self.start = list(event.GetPositionTuple())
		self.end = list(event.GetPositionTuple())
		if self.check_snap:
			self.start, self.start_doc = self.snap.snap_point(self.start)[1:]
			self.end, self.end_doc = self.snap.snap_point(self.end)[1:]
		self.counter = 0
		self.timer.Start(RENDERING_DELAY)
		self.canvas.CaptureMouse()

	def mouse_up(self, event):
		self.canvas.ReleaseMouse()
		if self.draw:
			self.timer.Stop()
			self.draw = False
			self.counter = 0
			self.end = list(event.GetPositionTuple())
			if self.check_snap:
				self.end, self.end_doc = self.snap.snap_point(self.end)[1:]
			if self.do_action(event):
				self.start = []
				self.end = []
				self.canvas.selection_redraw()

	def mouse_move(self, event):
		if self.draw:
			self.end = list(event.GetPositionTuple())
			if self.check_snap:
				self.end, self.end_doc = self.snap.snap_point(self.end)[1:]

	def on_timer(self):
		self.canvas.selection_redraw()

	def repaint(self):
		if self.end:
			self.canvas.renderer.draw_frame(self.start, self.end)

class WaitController(AbstractController):

	mode = modes.WAIT_MODE
	move = False
	fleur_timer = None

	def __init__(self, canvas, presenter):
		AbstractController.__init__(self, canvas, presenter)

	def mouse_down(self, event):pass
	def mouse_up(self, event):pass
	def repaint(self, *args):pass
	def mouse_move(self, event):pass
	def on_timer(self):pass
