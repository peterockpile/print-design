import wx


class TabbedFrame(wx.Frame):

    """
    A wx.Frame subclass which uses a toolbar to implement tabbed views and
    invokes the native 'selected' look on OS X when running wxPython version
    2.8.8.0 or higher.
    
    To use:
    - Create an instance.
    - Call CreateTabs with a list of (label, bitmap) pairs for the tabs.
    - Override OnTabChange(tabIndex) to respond to the user switching tabs.
    
    The native selection look on OS X requires that only one toolbar item be
    active at a time (like radio buttons). There is no such requirement with
    the toggle tools in wx, which is why the native look is not used (see
    http://trac.wxwidgets.org/ticket/8789). But this class enforces that
    exactly one tool is toggled at a time, so the native look can be enabled
    by loading the Carbon and CoreFoundation frameworks via ctypes and
    manipulating the toolbar.
    """

    def CreateTabs(self, tabs):
        """
        Create the toolbar and add a tool for each tab.
        
        tabs -- List of (label, bitmap) pairs.
        """

        # Create the toolbar
        self.tabIndex = 0
        self.toolbar = self.CreateToolBar(style=wx.TB_HORIZONTAL | wx.TB_TEXT)
        for i, tab in enumerate(tabs):
            self.toolbar.AddCheckLabelTool(id=i, label=tab[0], bitmap=tab[1])
        self.toolbar.Realize()

        # Determine whether to invoke the special toolbar handling
        macNative = False
        if wx.Platform == '__WXMAC__':
            if hasattr(self, 'MacGetTopLevelWindowRef'):
                try:
                    import ctypes
                    macNative = True
                except ImportError:
                    pass
        if macNative:
            self.PrepareMacNativeToolBar()
            self.Bind(wx.EVT_TOOL, self.OnToolBarMacNative)
        else:
            self.toolbar.ToggleTool(0, True)
            self.Bind(wx.EVT_TOOL, self.OnToolBarDefault)

        self.Show()

    def OnTabChange(self, tabIndex):
        """Respond to the user switching tabs."""

        pass

    def PrepareMacNativeToolBar(self):
        """Extra toolbar setup for OS X native toolbar management."""

        # Load the frameworks
        import ctypes
        carbonLoc = '/System/Library/Carbon.framework/Carbon'
        coreLoc = '/System/Library/CoreFoundation.framework/CoreFoundation'
        self.carbon = ctypes.CDLL(carbonLoc)# Also used in OnToolBarMacNative
        core = ctypes.CDLL(coreLoc)
        # Get a reference to the main window
        frame = self.MacGetTopLevelWindowRef()
        # Allocate a pointer to pass around
        p = ctypes.c_voidp()
        # Get a reference to the toolbar
        self.carbon.GetWindowToolbar(frame, ctypes.byref(p))
        toolbar = p.value
        # Get a reference to the array of toolbar items
        self.carbon.HIToolbarCopyItems(toolbar, ctypes.byref(p))
        # Get references to the toolbar items (note: separators count)
        self.macToolbarItems = [core.CFArrayGetValueAtIndex(p, i)
                                for i in xrange(self.toolbar.GetToolsCount())]
        # Set the native "selected" state on the first tab
        # 128 corresponds to kHIToolbarItemSelected (1 << 7)
        item = self.macToolbarItems[self.tabIndex]
        self.carbon.HIToolbarItemChangeAttributes(item, 128, 0)

    def OnToolBarDefault(self, event):
        """Ensure that there is always one tab selected."""

        i = event.GetId()
        if i in xrange(self.toolbar.GetToolsCount()):
            self.toolbar.ToggleTool(i, True)
            if i != self.tabIndex:
                self.toolbar.ToggleTool(self.tabIndex, False)
                self.OnTabChange(i)
                self.tabIndex = i
        else:
            event.Skip()

    def OnToolBarMacNative(self, event):
        """Manage the toggled state of the tabs manually."""

        i = event.GetId()
        if i in xrange(self.toolbar.GetToolsCount()):
            self.toolbar.ToggleTool(i, False)# Suppress default selection
            if i != self.tabIndex:
                # Set the native selection look via the Carbon APIs
                # 128 corresponds to kHIToolbarItemSelected (1 << 7)
                item = self.macToolbarItems[i]
                self.carbon.HIToolbarItemChangeAttributes(item, 128, 0)
                self.OnTabChange(i)
                self.tabIndex = i
        else:
            event.Skip()


if __name__ == '__main__':
    app = wx.PySimpleApp()
    size = (32, 32)
    tabs = [
        ('List View', wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, size=size)),
        ('Report View', wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW, size=size))
    ]
    frame = TabbedFrame(None)
    frame.CreateTabs(tabs)
    def OnTabChange(tabIndex): print "Switched to tab", tabIndex
    frame.OnTabChange = OnTabChange
    frame.Show()
    app.MainLoop()
