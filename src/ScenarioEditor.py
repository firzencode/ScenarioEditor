import wx,os
import xml.etree.ElementTree as ET

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title, size=(640,480))
		self.dirname = "" 					# save the current directory path
		self.scenario = ScenarioObject()	# current scenario object
		self.InitMenu()
		self.InitWidgets()
		self.Show()
	def InitMenu(self):
		# Status Bar
		self.CreateStatusBar()
		# Menu
		filemenu = wx.Menu()
		filemenu_new = filemenu.Append(wx.ID_ANY, "&New", "Create a new scenario file")
		filemenu_open = filemenu.Append(wx.ID_ANY, "&Open", "Open a scenario file")
		filemenu_save = filemenu.Append(wx.ID_ANY, "&Save", "Save the scenario file")
		filemenu_exit = filemenu.Append(wx.ID_EXIT, "E&xit", "Quit the editor")
		# Menu Bar
		menubar = wx.MenuBar()
		menubar.Append(filemenu, "&File")
		self.SetMenuBar(menubar)
		# Bind Menu Event
		self.Bind(wx.EVT_MENU, self.OnMenuNew, filemenu_new)
		self.Bind(wx.EVT_MENU, self.OnMenuOpen, filemenu_open)
		self.Bind(wx.EVT_MENU, self.OnMenuSave, filemenu_save)
		self.Bind(wx.EVT_MENU, self.OnMenuExit, filemenu_exit)
		self.Bind(wx.EVT_CLOSE, self.OnClose)
	def InitWidgets(self):
		panel = wx.Panel(self)
		self.scenario_list = wx.ListBox(panel, -1, (10, 10), (200, 300), self.scenario.action_list,wx.LB_SINGLE)
		
		self.Bind(wx.EVT_BUTTON, self.OnTest, wx.Button(panel, -1, "Button", (300,300)))
	def OnMenuNew(self, event):
		pass
	def OnMenuOpen(self, event):
		dlg = wx.FileDialog(self, "Open scenario file", self.dirname, "", "Scenario files (*.xml)|*.xml", wx.OPEN | wx.FD_CHANGE_DIR)
		if dlg.ShowModal() == wx.ID_OK:
			filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			if self.scenario.Load(self.dirname + os.path.sep + filename):
				pass
			else:
				dlg = wx.MessageDialog(None, "Load failed with " + self.dirname + os.path.sep + filename + "\nThe format is invalidate or the data may be broken.", "Load Failed", wx.OK | wx.ICON_ERROR)
				dlg.ShowModal()
				dlg.Destroy()
	def OnMenuSave(self, event):
		dlg = wx.FileDialog(self, "Save scenario file", self.dirname, "", "Scenario files (*.xml)|*.xml", wx.SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR)
		if dlg.ShowModal() == wx.ID_OK:
			filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			self.scenario.Save(self.dirname + os.path.sep + filename)
	def OnMenuExit(self,event):
		self.Close(False)
	def OnClose(self, event):
		dlg = wx.MessageDialog(None, "Are you sure to quit the editor?", "Quit", wx.YES_NO | wx.ICON_EXCLAMATION)
		result = dlg.ShowModal()
		if result == wx.ID_YES:
			self.Destroy()
		dlg.Destroy()
	def OnTest(self, event):
		self.scenario.action_list.append("ya")
		print self.scenario.action_list
		self.scenario_list.Set(self.scenario.action_list)
class ScenarioObject:
	def __init__(self):
		self.action_list = []
	def Load(self, path):
		print "load file path:",path
		tree = ET.parse(path) 
		return False
	def Save(self, path):
		print "save file path:", path
		return False
	def Reset(self):
		pass

app = wx.App(False)
frame = MainWindow(None,"Ahaworks Scenario Script Editor")
app.MainLoop()