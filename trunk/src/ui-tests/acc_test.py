# -*- coding: utf-8 -*-
import wx
from wx._core import StaticBoxSizer

class MyForm(wx.Frame):

	#----------------------------------------------------------------------
	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "Tutorial")

		panel = wx.Panel(self, wx.ID_ANY)

		# Create an accelerator table
		exit_id = wx.NewId()
		xit_id = wx.NewId()
		yit_id = wx.NewId()
# 		self.Bind(wx.EVT_MENU, self.onAltX, id=xit_id)
# 		self.Bind(wx.EVT_MENU, self.onShiftAltY, id=yit_id)
		self.Bind(wx.EVT_KEY_UP, self.onExit2)



# 		self.accel_tbl = wx.AcceleratorTable([(wx.ACCEL_ALT, ord('X'), xit_id),
# 											  (wx.ACCEL_SHIFT | wx.ACCEL_ALT, ord('Y'), yit_id),
# 											  (wx.ACCEL_SHIFT | wx.ACCEL_CTRL, ord('Z'), exit_id),
# 											 ])
# 		self.SetAcceleratorTable(self.accel_tbl)

		# Create a menu
		menuBar = wx.MenuBar()
		fileMenu = wx.Menu()

		refreshMenuItem = fileMenu.Append(yit_id, "Refresh", "Refresh app")
		self.Bind(wx.EVT_MENU, self.onRefresh, refreshMenuItem)
		acc = wx.AcceleratorEntry(wx.ACCEL_SHIFT | wx.ACCEL_CMD, wx.WXK_DELETE, yit_id)
		print acc.ToString()
		refreshMenuItem.SetAccel(acc)

		exitMenuItem = fileMenu.Append(xit_id, "E&xit\tCtrl+X", "Exit the program")
		self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem)

		self.hMenu = wx.Menu()

		exitMenuItem2 = self.hMenu.Append(wx.ID_EXIT, "&Выход", "Exit the program")
		self.Bind(wx.EVT_MENU, self.onExit, exitMenuItem2)

		menuBar.Append(fileMenu, "File")
		item = menuBar.Append(self.hMenu, "Hidden")
		self.SetMenuBar(menuBar)

		t1 = wx.TextCtrl(self, -1, "Test it out and see", size=(125, -1))
		box = wx.BoxSizer()
		self.SetSizer(box)
		box.Add(t1)

# 		accel_tbl = wx.AcceleratorTable([
# 						 (wx.ACCEL_ALT, ord('Z'), exitMenuItem.GetId()),
# 						])
# 		self.SetAcceleratorTable(accel_tbl)



	#----------------------------------------------------------------------
	def onRefresh(self, event):
		print "refreshed!"

	#----------------------------------------------------------------------
	def onAltX(self, event):
		""""""
		print "You pressed ALT+X!"

	#----------------------------------------------------------------------
	def onShiftAltY(self, event):
		""""""
		print "You pressed SHIFT+ALT+Y!"

	#----------------------------------------------------------------------
	def onExit(self, event):
		""""""
		self.Close()

	#----------------------------------------------------------------------
	def onExit2(self, event):
		""""""
		print event

#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
	app = wx.PySimpleApp()
	frame = MyForm().Show()
	app.MainLoop()
