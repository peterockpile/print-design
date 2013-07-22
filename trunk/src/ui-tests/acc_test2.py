# -*- coding: utf-8 -*-
import wx, os

class TestKey(wx.Frame):
	def __init__(self, parent, id, title, position, size):
		wx.Frame.__init__(self, parent, id, title, position, size)
		menuBar = wx.MenuBar()
		fileMenu = wx.Menu()
		menuBar.Append(fileMenu, "File")
		self.SetMenuBar(menuBar)
		#-----------------------
		ID = wx.NewId()
		ID2 = wx.NewId()
		self.SetAcceleratorTable(
			wx.AcceleratorTable([(wx.ACCEL_ALT, ord('P'), ID),
								(wx.ACCEL_ALT, ord('R'), ID2)
								]))
		wx.EVT_MENU(self, ID, self.OnAccelKey)
		wx.EVT_MENU(self, ID2, self.OnAccelKey)
		#-----------------------

  		d = wx.Button(self, -1, "Press Me")
  		wx.EVT_BUTTON(self, d.GetId(), self.OnButton)
 		wx.EVT_KEY_DOWN(self, self.OnKeyDown)

 		t1 = wx.TextCtrl(self, -1, "Test it out and see", size=(125, -1))
 		t1.SetFocus()

	def set_focus(self):
		self.SetFocus()


	def OnKeyDown(self, event):
		key = event.KeyCode()
		if key == wx.WXK_UP:
			print "Up Key Pressed"
		event.Skip()


	def OnAccelKey(self, evt):
		print "Got accelerator"

	def OnButton(self, evt):
		print "Button pressed"


class App(wx.App):
	def OnInit(self):
		self.frame = TestKey(None, -1, "Key Press  Test",
						wx.DefaultPosition, (200, 200))
		self.SetTopWindow(self.frame)
		wx.CallAfter(self.frame.SetFocus)
		self.frame.Show(True)
		return True

if __name__ == "__main__":
		app = App(0)
		app.MainLoop()
