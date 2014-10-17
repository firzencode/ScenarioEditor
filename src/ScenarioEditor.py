import wx,os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree

class MainWindow(wx.Frame):
	def __init__(self, parent, title):
		wx.Frame.__init__(self, parent, title = title, size=(640,480), style = wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
		self.dirname = ""    # save the current directory path
		self.scenario = ScenarioObject()    # current scenario object
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
		sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.editarea_sizer_list = []
		self.InitWidgets_ActionList(panel, sizer)
		#self.InitWidgets_EditArea(panel, sizer)
		self.InitWidgets_DefActor(panel, sizer)
		self.InitWidgets_Dialog(panel, sizer)
		panel.SetSizer(sizer)
		self.main_sizer = sizer
	def InitWidgets_ActionList(self, panel, parent_sizer):
		self.scenario_listbox = wx.ListBox(panel, -1, (10, 10), (400, 300), self.scenario.action_list,wx.LB_SINGLE | wx.LB_HSCROLL)
		
		# Movement 
		btn_action_moveup = wx.Button(panel, -1, "Up")
		btn_action_movedown = wx.Button(panel,-1, "Down")
		sizer_movement = wx.BoxSizer(wx.HORIZONTAL)
		sizer_movement.Add(btn_action_moveup, flag = wx.ALL, border = 5)
		sizer_movement.Add(btn_action_movedown, flag = wx.ALL, border = 5)
		
		# Add / Remove
		btn_action_addaction = wx.Button(panel,-1,"Add Action")
		btn_action_removeaction = wx.Button(panel,-1, "Remove Action")
		sizer_add_remove = wx.BoxSizer(wx.HORIZONTAL)	
		sizer_add_remove.Add(btn_action_addaction, flag = wx.ALL, border = 5)
		sizer_add_remove.Add(btn_action_removeaction, flag = wx.ALL, border = 5)
		
		# Main
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.scenario_listbox, flag = wx.ALL, border = 5)
		sizer.Add(sizer_movement)
		sizer.Add(sizer_add_remove)
		parent_sizer.Add(sizer)
		
		# Bind
		self.Bind(wx.EVT_BUTTON, self.OnActionMoveUp, btn_action_moveup )
		self.Bind(wx.EVT_BUTTON, self.OnActionMoveDown, btn_action_movedown)
		self.Bind(wx.EVT_BUTTON, self.OnActionAdd, btn_action_addaction)
		self.Bind(wx.EVT_BUTTON, self.OnActionRemove, btn_action_removeaction)
		self.Bind(wx.EVT_LISTBOX, self.OnListboxSelectChanged, self.scenario_listbox)
	#---------- Init Widget DefActor ----------
	def InitWidgets_DefActor(self, panel, parent_sizer):
		#sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
		sizer = wx.BoxSizer(wx.VERTICAL)
		id_label = wx.StaticText(panel, -1, "Actor Id")
		id_text = wx.TextCtrl(panel)
		name_label = wx.StaticText(panel, -1, "Actor Name")
		name_text = wx.TextCtrl(panel)
		
		sizer = self.InitWidgetsUtil([id_label, id_text, name_label, name_text], parent_sizer, ActionDefineActor, self.LoadData_DefActor)
		sizer.custom_textctrl_id = id_text
		sizer.custom_textctrl_name = name_text
		self.Bind(wx.EVT_TEXT, self.SaveData_DefActor, id_text)
		self.Bind(wx.EVT_TEXT, self.SaveData_DefActor, name_text)
	def SaveData_DefActor(self, event):
		action = self.GetCurrentSelectAction()
		if action != None:
			action.actor_id = ActionDefineActor.sizer.custom_textctrl_id.GetValue()
			action.actor_name = ActionDefineActor.sizer.custom_textctrl_name.GetValue()
			self.SaveActionToListbox(action.ToString())
	def LoadData_DefActor(self, action):
		ActionDefineActor.sizer.custom_textctrl_id.ChangeValue(action.actor_id)
		ActionDefineActor.sizer.custom_textctrl_name.ChangeValue(action.actor_name)
	#---------- Init Widget Dialog ----------
	def InitWidgets_Dialog(self, panel, parent_sizer):
		id_label = wx.StaticText(panel, -1, "Actor Id")
		id_text = wx.TextCtrl(panel)
		content_label = wx.StaticText(panel, -1, "Dialog Content")
		content_text = wx.TextCtrl(panel, style = wx.TE_MULTILINE, size = (200,450))
		sizer = self.InitWidgetsUtil([id_label, id_text, content_label, content_text], parent_sizer, ActionDialog, self.LoadData_Dialog)
		sizer.custom_textctrl_id = id_text
		sizer.custom_textctrl_content = content_text
		self.Bind(wx.EVT_TEXT, self.SaveData_Dialog, id_text)
		self.Bind(wx.EVT_TEXT, self.SaveData_Dialog, content_text)
	def SaveData_Dialog(self, event):
		action = self.GetCurrentSelectAction()
		if action != None:
			action.actor_id = ActionDialog.sizer.custom_textctrl_id.GetValue()
			action.text = ActionDialog.sizer.custom_textctrl_content.GetValue()
			self.SaveActionToListbox(action.ToString())
	def LoadData_Dialog(self, action):
		ActionDialog.sizer.custom_textctrl_id.ChangeValue(action.actor_id)
		ActionDialog.sizer.custom_textctrl_content.ChangeValue(action.text)
	#---------- Widget Util ----------
	def InitWidgetsUtil(self, widget_list, parent_sizer, action_class, load_data_method):
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.AddMany(widget_list)
		self.editarea_sizer_list.append(sizer)
		parent_sizer.Add(sizer, flag = wx.ALL, border = 5)
		sizer.ShowItems(False)
		action_class.sizer = sizer
		sizer.LoadActionData = load_data_method
		return sizer
	def GetCurrentSelectAction(self):
		selections = self.scenario_listbox.GetSelections()
		if len(selections) > 0:
			return self.scenario.action_list[selections[0]]
		else:
			print "Current Select is None! That's strange!"
			return None
	def SaveActionToListbox(self, str):
		selections = self.scenario_listbox.GetSelections()
		if len(selections) > 0:
			print selections[0], "  +++  ", str
			self.scenario_listbox.SetString(selections[0],str)
		else:
			print "Current Select is None! That's strange!"
	#---------- Menu & Event ----------
	def OnMenuNew(self, event):
		dlg = wx.MessageDialog(None, "Do you want to save the current file?", "Editor",wx.CANCEL | wx.YES_NO | wx.ICON_WARNING)
		result = dlg.ShowModal()
		if result == wx.ID_YES:
			if self.OnMenuSave(event):
				self.scenario.Reset()
				self.scenario_listbox.Set(self.scenario.GetListboxArray())
		elif result == wx.ID_NO:
			self.scenario.Reset()
			self.scenario_listbox.Set(self.scenario.GetListboxArray())
			pass
		elif result == wx.ID_CANCEL:
			pass
	def OnMenuOpen(self, event):
		dlg = wx.FileDialog(self, "Open scenario file", self.dirname, "", "Scenario files (*.xml)|*.xml", wx.OPEN | wx.FD_CHANGE_DIR)
		if dlg.ShowModal() == wx.ID_OK:
			filename = dlg.GetFilename()
			self.dirname = dlg.GetDirectory()
			self.scenario.Reset()
			if self.scenario.Load(self.dirname + os.path.sep + filename):
				self.OnScenarioLoadSuccess()
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
			return True
		return False
	def OnMenuExit(self,event):
		self.Close(False)
	def OnClose(self, event):
		dlg = wx.MessageDialog(None, "Are you sure to quit the editor?", "Quit", wx.YES_NO | wx.ICON_EXCLAMATION)
		result = dlg.ShowModal()
		if result == wx.ID_YES:
			self.Destroy()
		dlg.Destroy()
	def OnActionMoveUp(self, event):
		pass
	def OnActionMoveDown(self, event):
		pass
	def OnActionAdd(self, event):
		pass
	def OnActionRemove(self, event):
		pass
	def OnScenarioLoadSuccess(self):
		self.scenario_listbox.Set(self.scenario.GetListboxArray())
		pass
	def OnListboxSelectChanged(self, event):
		selections = self.scenario_listbox.GetSelections()
		for sizer in self.editarea_sizer_list:
			sizer.ShowItems(False)
		if len(selections) > 0:
			action = self.scenario.action_list[selections[0]]
			print "select: ", action.ToString()
			action.sizer.ShowItems(True)
			action.sizer.LoadActionData(action)
		else:
			print "no selections"
		self.main_sizer.Layout()
class ScenarioObject:
	def __init__(self):
		self.action_list = []
		self.uid = ""
		self.type_map = {
		"def_actor":ActionDefineActor,
		"dialog":ActionDialog
		}
	def Load(self, path):
		print "load file path:",path
		tree = ET.parse(path)
		root = tree.getroot()
		
		# check root element
		if root.tag != "scenario":
			return False
		
		# load root attrs
		self.uid = root.attrib["uid"]
		
		# load elements
		for element in root:
			print "LoadElement:=====>", element.tag
			if element.tag in self.type_map:
				tempObject = self.type_map[element.tag]()
				loadResult = tempObject.LoadElement(element)
				if loadResult == True:
					self.action_list.append(tempObject)
				else:
					print "Load element failed: ", element.tag
			else:
				print "Can't decode element: ", element.tag
		
		self.Print()
		return True
	def Save(self, path):
		print "save file path:", path
		root = Element("scenario")
		tree = ElementTree(root)
		
		root.attrib["uid"] = self.uid
		for action in self.action_list:
			action.SaveElement(root)
		self.indent(root)
		tree.write(path, 'utf-8')
	# used to format xml file
	def indent(self, elem, level=0):
		i = "\n" + level*"\t"
		if len(elem):
			if not elem.text or not elem.text.strip():
				elem.text = i + "\t"
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
			for elem in elem:
				self.indent(elem, level+1)
			if not elem.tail or not elem.tail.strip():
				elem.tail = i
		else:
			if level and (not elem.tail or not elem.tail.strip()):
				elem.tail = i
	def Reset(self):
		del self.action_list[:]
		self.uid = ""
	def Print(self):
		print "ScenarioObjectData:"
		print "uid = ", self.uid
		for action in self.action_list:
			action.Print()
	def GetListboxArray(self):
		array = []
		for action in self.action_list:
			action.PutDataIntoListbox(array)
		return array
class ScenarioAction:
	def __init__(self):
		pass
	def Print(self):
		print self.ToString()
	def ToString(self):
		return "Action"
	def LoadElement(self, element):
		return True
	def SaveElement(self, parent_element):
		pass
	def PutDataIntoListbox(self, array):
		array.append(self.ToString())
class ActionDefineActor(ScenarioAction):
	def LoadElement(self, element):
		if ("actor_id" in element.attrib) & ("actor_name" in element.attrib):
			self.actor_id = element.attrib["actor_id"]
			self.actor_name = element.attrib["actor_name"]
			return True
		else:
			return False
	def ToString(self):
		return "[def_actor] actor_id: {0}, actor_name: {1}".format(self.actor_id, self.actor_name)
	def SaveElement(self, parent_element):
		element = Element("def_actor", {"actor_id":self.actor_id, "actor_name":self.actor_name})
		parent_element.append(element)
class ActionDialog(ScenarioAction):
	def LoadElement(self, element):
		if "actor_id" in element.attrib:
			self.actor_id = element.attrib["actor_id"]
			self.text = element.text
			return True
		else:
			return False
	def ToString(self):
		return "[dialog] actor_id: {0}, text: {1}:".format(self.actor_id, self.text)
	def SaveElement(self, parent_element):
		element = Element("dialog", {"actor_id":self.actor_id})
		element.text = self.text
		parent_element.append(element)
class ActionSet(ScenarioAction):
	def __init__(self):
		pass
	
app = wx.App(False)
frame = MainWindow(None,"Ahaworks Scenario Script Editor")
app.MainLoop()