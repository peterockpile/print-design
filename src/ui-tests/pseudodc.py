
import wx
#import images
import random

import cairo

from pdesign.widgets import const, copy_surface_to_bitmap
from pdesign.widgets import BOTTOM, CENTER, LEFT, ALL, EXPAND, TOP
from pdesign.widgets import Application, MainWindow, VPanel, HPanel, Button, Label

#---------------------------------------------------------------------------

W = 1500
H = 1000
SW = 150
SH = 150
SHAPE_COUNT = 20
hitradius = 5

#---------------------------------------------------------------------------

colours = [
	wx.Colour(0, 0, 255, 150),
	wx.Colour(0, 255, 255, 150),
	wx.Colour(255, 0, 255, 150),
	wx.Colour(0, 0, 150, 150),
	wx.Colour(0, 150, 150, 150),
	wx.Colour(150, 150, 150, 150),
	wx.Colour(150, 0, 0, 150),
	wx.Colour(150, 150, 0, 150),
	wx.Colour(150, 0, 255, 150),
	]



class MyCanvas(wx.ScrolledWindow):
	start = []
	end = []
	draw = False
	frame = None

	def __init__(self, parent, id, size=wx.DefaultSize):
		wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)

		self.lines = []
		self.maxWidth = W
		self.maxHeight = H
		self.x = self.y = 0
		self.curLine = []
		self.drawing = False

		self.SetBackgroundColour("WHITE")
#		bmp = images.Test2.GetBitmap()
#		mask = wx.Mask(bmp, wx.BLUE)
#		bmp.SetMask(mask)
#		self.bmp = bmp

		self.SetVirtualSize((self.maxWidth, self.maxHeight))
		self.SetScrollRate(20, 20)

		# create a PseudoDC to record our drawing
		self.pdc = wx.PseudoDC()
		self.pen_cache = {}
		self.brush_cache = {}
		#self.DoDrawing(self.pdc)

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_ERASE_BACKGROUND, lambda x:None)
		self.Bind(wx.EVT_MOUSE_EVENTS, self.OnMouse)

		# vars for handling mouse clicks
		self.dragid = -1
		self.lastpos = (0, 0)

	def ConvertEventCoords(self, event):
		xView, yView = self.GetViewStart()
		xDelta, yDelta = self.GetScrollPixelsPerUnit()
		return (event.GetX() + (xView * xDelta),
			event.GetY() + (yView * yDelta))

	def convert_coords(self, x, y):
		xView, yView = self.GetViewStart()
		xDelta, yDelta = self.GetScrollPixelsPerUnit()
		return [x + (xView * xDelta), y + (yView * yDelta)]

	def OffsetRect(self, r):
		xView, yView = self.GetViewStart()
		xDelta, yDelta = self.GetScrollPixelsPerUnit()
		r.OffsetXY(-(xView * xDelta), -(yView * yDelta))

	def draw_frame(self, start, end):pass

	def hide_frame(self):pass


	def OnMouse(self, event):
		if event.LeftDown():
			self.start = list(event.GetPositionTuple())
			self.draw = True
		elif event.Dragging() and self.draw:
			end = list(event.GetPositionTuple())
			self.draw_frame(self.start, end)
			self.end = end
		elif event.LeftUp() and self.draw:
			self.draw = False
			self.hide_frame()


#		global hitradius
#		if event.LeftDown():
#			x, y = self.ConvertEventCoords(event)
#			#l = self.pdc.FindObjectsByBBox(x, y)
#			l = self.pdc.FindObjects(x, y, hitradius)
#			for id in l:
#				if not self.pdc.GetIdGreyedOut(id):
#					self.dragid = id
#					self.lastpos = (event.GetX(), event.GetY())
#					break
#		elif event.RightDown():
#			x, y = self.ConvertEventCoords(event)
#			#l = self.pdc.FindObjectsByBBox(x, y)
#			l = self.pdc.FindObjects(x, y, hitradius)
#			if l:
#				self.pdc.SetIdGreyedOut(l[0], not self.pdc.GetIdGreyedOut(l[0]))
#				r = self.pdc.GetIdBounds(l[0])
#				r.Inflate(4, 4)
#				self.OffsetRect(r)
#				self.RefreshRect(r, False)
#		elif event.Dragging() or event.LeftUp():
#			if self.dragid != -1:
#				x, y = self.lastpos
#				dx = event.GetX() - x
#				dy = event.GetY() - y
#				r = self.pdc.GetIdBounds(self.dragid)
#				self.pdc.TranslateId(self.dragid, dx, dy)
#				r2 = self.pdc.GetIdBounds(self.dragid)
#				r = r.Union(r2)
#				r.Inflate(4, 4)
#				self.OffsetRect(r)
#				self.RefreshRect(r, False)
#				self.lastpos = (event.GetX(), event.GetY())
#			if event.LeftUp():
#				self.dragid = -1

	def RandomPen(self):
		c = random.choice(colours)
		t = random.randint(1, 4)
		if not self.pen_cache.has_key((c, t)):
			self.pen_cache[(c, t)] = wx.Pen(c, t)
		return self.pen_cache[(c, t)]


	def RandomBrush(self):
		c = random.choice(colours)
		if not self.brush_cache.has_key(c):
			self.brush_cache[c] = wx.Brush(c)

		return self.brush_cache[c]

	def RandomColor(self):
		return random.choice(colours)


	def OnPaint(self, event):
		# Create a buffered paint DC.  It will create the real
		# wx.PaintDC and then blit the bitmap to it when dc is
		# deleted.
		dc = wx.BufferedPaintDC(self)
		# use PrepateDC to set position correctly
		self.PrepareDC(dc)
		# we need to clear the dc BEFORE calling PrepareDC
		bg = wx.Brush(self.GetBackgroundColour())
		dc.SetBackground(bg)
		dc.Clear()
		# create a clipping rect from our position and size
		# and the Update Region
		xv, yv = self.GetViewStart()
		dx, dy = self.GetScrollPixelsPerUnit()
		x, y = (xv * dx, yv * dy)
		rgn = self.GetUpdateRegion()
		rgn.Offset(x, y)
		r = rgn.GetBox()
		# draw to the dc using the calculated clipping rect
		self.pdc.DrawToDCClipped(dc, r)

	def DoDrawing(self):
		self.pdc = wx.PseudoDC()
		dc = self.pdc
		random.seed()
		self.objids = []
		self.boundsdict = {}
		dc.BeginDrawing()
		dc.Clear()
		for i in range(SHAPE_COUNT):
			id = wx.NewId()
			dc.SetId(id)
			bmp = self.create_bmp()
			w, h = bmp.GetSize()
			x = random.randint(0, W - w)
			y = random.randint(0, H - h)
			dc.DrawBitmap(bmp, x, y, True)
			dc.SetIdBounds(id, wx.Rect(x, y, w, h))
			self.objids.append(id)
		dc.EndDrawing()
		self.refresh()

	def refresh(self, x=0, y=0, w=0, h=0):
		if not w: w, h = self.GetSize()
		self.Refresh(rect=wx.Rect(x, y, w, h))

	def create_bmp(self):
		surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 500, 500)
		ctx = cairo.Context(surface)
		ctx.set_line_width(15)
		ctx.move_to(250, 50)
		ctx.line_to(450, 450)
		ctx.rel_line_to(-400, 0)
		ctx.close_path()
		ctx.set_source_rgba(random.random(),
						random.random(),
						random.random(),
						random.random())
		ctx.stroke()
		return copy_surface_to_bitmap(surface)

class ControlPanel(HPanel):

	canvas = None

	def __init__(self, parent):
		HPanel.__init__(self, parent)
		self.add((25, 5))
		but = Button(self, 'Draw', onclick=self.redraw)
		self.add(but)

	def set_canvas(self, canvas):
		self.canvas = canvas

	def redraw(self, event):
		self.canvas.DoDrawing()




app = Application('PseudoDC test')
mw = MainWindow(app.app_name, (700, 500))
panel = ControlPanel(mw)
mw.add(panel, 0, ALL | EXPAND)
canvas = MyCanvas(mw, wx.ID_ANY)
panel.set_canvas(canvas)
mw.add(canvas, 1, ALL | EXPAND)
app.mw = mw
app.run()
