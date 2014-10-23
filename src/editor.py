import wx, os
from scenario import *
from scenario import ScenarioObject

class EditorWindow(wx.Frame):
    def __init__(self, parent, title):
            wx.Frame.__init__(self, parent, title = title, size=(640,480), style = wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
            # key: action class, value: sizer holding widgets
            self.editarea_sizer_map = {}
            # key: action class, value: method to load data from action to widget
            self.editarea_load_func_map = {}
            self.controller = EditorController(self)
            self.InitMenu()
            self.InitWidgets()
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
            self.Bind(wx.EVT_MENU, self.controller.OnMenuNew, filemenu_new)
            self.Bind(wx.EVT_MENU, self.controller.OnMenuOpen, filemenu_open)
            self.Bind(wx.EVT_MENU, self.controller.OnMenuSave, filemenu_save)
            self.Bind(wx.EVT_MENU, self.controller.OnMenuExit, filemenu_exit)
            self.Bind(wx.EVT_CLOSE, self.controller.OnClose)
    def InitWidgets(self):
            # main panel
            panel = wx.Panel(self)
            # main sizer
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            # init
            self.InitWidgets_ActionList(panel, sizer)
            self.InitWidgets_DefActor(panel, sizer)
            self.InitWidgets_Dialog(panel, sizer)
            panel.SetSizer(sizer)
            self.main_panel = panel
    def InitWidgets_ActionList(self, panel, parent_sizer):
            self.widget_listbox = wx.ListBox(panel, -1, (10, 10), (400, 300),style = wx.LB_SINGLE | wx.LB_HSCROLL)
            
            # Movement 
            btn_action_moveup = wx.Button(panel, -1, "Up")
            btn_action_movedown = wx.Button(panel,-1, "Down")
            text_scenario_uid = wx.StaticText(panel,label = "UID")
            self.widget_textctrl_scenario_uid = wx.TextCtrl(panel)
            
            sizer_movement = wx.BoxSizer(wx.HORIZONTAL)
            sizer_movement.Add(btn_action_moveup, flag = wx.ALL, border = 5)
            sizer_movement.Add(btn_action_movedown, flag = wx.ALL, border = 5)
            sizer_movement.Add(text_scenario_uid, flag = wx.ALL | wx.CENTER, border = 5)
            sizer_movement.Add(self.widget_textctrl_scenario_uid, flag = wx.ALL, border = 5)
            
            # Add / Remove
            btn_action_addaction = wx.Button(panel,-1,"Add Action")
            btn_action_removeaction = wx.Button(panel,-1, "Remove Action")
            
            sizer_add_remove = wx.BoxSizer(wx.HORIZONTAL)	
            sizer_add_remove.Add(btn_action_addaction, flag = wx.ALL, border = 5)
            sizer_add_remove.Add(btn_action_removeaction, flag = wx.ALL, border = 5)
            
            # Add to sizer
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(self.widget_listbox, flag = wx.ALL, border = 5)
            sizer.Add(sizer_movement)
            sizer.Add(sizer_add_remove)
            parent_sizer.Add(sizer)
            
            # Bind
            self.Bind(wx.EVT_BUTTON, self.controller.OnBtnActionMoveUp, btn_action_moveup )
            self.Bind(wx.EVT_BUTTON, self.controller.OnBtnActionMoveDown, btn_action_movedown)
            self.Bind(wx.EVT_BUTTON, self.controller.OnBtnActionAdd, btn_action_addaction)
            self.Bind(wx.EVT_BUTTON, self.controller.OnBtnActionRemove, btn_action_removeaction)
            self.Bind(wx.EVT_LISTBOX, self.controller.OnListboxSelectChanged, self.widget_listbox)
            self.Bind(wx.EVT_TEXT, self.controller.OnTextCtrlUidChanged, self.widget_textctrl_scenario_uid)
    def InitWidgets_DefActor(self, panel, parent_sizer):
            sizer = wx.BoxSizer(wx.VERTICAL)
            # Widgets
            id_label = wx.StaticText(panel, -1, "Actor Id")
            id_text = wx.TextCtrl(panel)
            name_label = wx.StaticText(panel, -1, "Actor Name")
            name_text = wx.TextCtrl(panel)
            # Add to sizer
            sizer.AddMany([id_label, id_text, name_label, name_text])
            parent_sizer.Add(sizer, flag = wx.ALL, border = 5)
            sizer.ShowItems(False)
            # Bind 
            self.editarea_sizer_map[ActionDefineActor] = sizer
            self.editarea_load_func_map[ActionDefineActor] = self.controller.ActionLoad_DefActor
            self.Bind(wx.EVT_TEXT, self.controller.ActionSave_DefActor, id_text)
            self.Bind(wx.EVT_TEXT, self.controller.ActionSave_DefActor, name_text)
            # Save widget
            self.widget_defactor_textctrl_id = id_text
            self.widget_defactor_textctrl_name = name_text
    def InitWidgets_Dialog(self, panel, parent_sizer):
            sizer = wx.BoxSizer(wx.VERTICAL)
            # Widgets
            id_label = wx.StaticText(panel, -1, "Actor Id")
            id_text = wx.TextCtrl(panel)
            content_label = wx.StaticText(panel, -1, "Dialog Content")
            content_text = wx.TextCtrl(panel, style = wx.TE_MULTILINE, size = (200,450))
            # Add to sizer
            sizer.AddMany([id_label,id_text,content_label,content_text])
            parent_sizer.Add(sizer, flag = wx.ALL, border = 5)
            sizer.ShowItems(False)
            # Bind
            self.editarea_sizer_map[ActionDialog] = sizer
            self.editarea_load_func_map[ActionDialog] = self.controller.ActionLoad_Dialogue
            self.Bind(wx.EVT_TEXT, self.controller.ActionSave_Dialogue, id_text)
            self.Bind(wx.EVT_TEXT, self.controller.ActionSave_Dialogue, content_text)
            # Save widget
            self.widget_dialogue_textctrl_id = id_text
            self.widget_dialogue_textctrl_text = content_text
class EditorController:
    def __init__(self, window):
        # scenario object. save all data
        self.scenario = ScenarioObject()
        # main window
        self.window = window
        # save the current directory path
        self.dirname = ""
    def OnMenuNew(self, event):
        """Handle event while file->new clicked"""
        dlg = wx.MessageDialog(None, "Do you want to save the current file?", "Editor",wx.CANCEL | wx.YES_NO | wx.ICON_WARNING)
        result = dlg.ShowModal()
        if (result == wx.ID_YES):
            if self.OnMenuSave(event):
                self.scenario.Reset()
                self.RefreshListbox()
                self.HideAllEditArea()
        elif result == wx.ID_NO:
            self.scenario.Reset()
            self.RefreshListbox()
            self.HideAllEditArea()
    def OnMenuOpen(self, event):
        """Handle event while file->open clicked"""
        dlg = wx.FileDialog(self.window, "Open scenario file", self.dirname, "", "Scenario files (*.xml)|*.xml", wx.OPEN | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.scenario.Reset()
            self.HideAllEditArea()
            if self.scenario.Load(self.dirname + os.path.sep + filename):
                self.RefreshListbox()    
            else:
                dlg = wx.MessageDialog(None, "Load failed with " + self.dirname + os.path.sep + filename + "\nThe format is invalidate or the data may be broken.", "Load Failed", wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
        pass
    def OnMenuSave(self, event):
        """Handle event while file->save clicked"""
        dlg = wx.FileDialog(self.window, "Save scenario file", self.dirname, "", "Scenario files (*.xml)|*.xml", wx.SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            self.scenario.Save(self.dirname + os.path.sep + filename)
            return True
        return False
    def OnMenuExit(self, event):
        """Handle event while file->exit clicked"""
        self.window.Close(False)
    def OnClose(self, event):
        """Handle event while main window close"""
        dlg = wx.MessageDialog(None, "Are you sure to quit the editor?", "Quit", wx.YES_NO | wx.ICON_EXCLAMATION)
        result = dlg.ShowModal()
        if result == wx.ID_YES:
            self.window.Destroy()
        dlg.Destroy()
    def OnBtnActionMoveUp(self, event):
        """Handle event while button action move up clicked"""
        selections = self.window.widget_listbox.GetSelections()
        if len(selections) > 0:
            index = selections[0]
            if index > 0:
                # swap action
                self.scenario.action_list[index-1], self.scenario.action_list[index] \
                = self.scenario.action_list[index], self.scenario.action_list[index - 1]
                
                # swap list item
                item_list = self.window.widget_listbox.GetItems()
                item_list[index - 1], item_list[index] = item_list[index], item_list[index - 1]
                self.window.widget_listbox.SetItems(item_list)
                
                # change selected item
                self.window.widget_listbox.Select(index - 1)
    def OnBtnActionMoveDown(self, event):
        """Handle event while button action move down clicked"""
        selections = self.window.widget_listbox.GetSelections()
        if len(selections) > 0:
            index = selections[0]
            if index < self.window.widget_listbox.GetCount() - 1:
                # swap action
                self.scenario.action_list[index + 1], self.scenario.action_list[index] \
                = self.scenario.action_list[index], self.scenario.action_list[index + 1]
                
                #swap list item
                item_list = self.window.widget_listbox.GetItems()
                item_list[index + 1], item_list[index] = item_list[index], item_list[index + 1]
                self.window.widget_listbox.SetItems(item_list)
                
                # change selected item
                self.window.widget_listbox.Select(index + 1)
        pass
    def OnBtnActionAdd(self, event):
        """Handle event while button action add clicked"""
        win = NewActionWindow(self.window);
        win.ShowModal()
        if win.result != None:
            self.scenario.action_list.append(win.result)
            self.window.widget_listbox.Append(win.result.ToString())
        pass
    def OnBtnActionRemove(self, event):
        """Handle event while button action remove clicked"""
        selections = self.widget_listbox.GetSelections()
        if len(selections) > 0:
            self.HideAllEditArea()
            action = self.scenario.action_list[selections[0]]
            self.scenario.action_list.pop(selections[0])
            self.window.widget_listbox.Delete(selections[0])
            if selections[0] > 0:
                self.window.widget_listbox.Select(selections[0] - 1)
    def OnListboxSelectChanged(self, event):
        """Handle event while the selected item in listbox has been changed"""
        self.HideAllEditArea()
        selections = self.window.widget_listbox.GetSelections()
        if len(selections) > 0:
            action = self.scenario.action_list[selections[0]]
            print "select: ", action.ToString()
            self.ShowEditArea(action)
            self.LoadEditAreaData(action)
        else:
            print "no selections"
    def OnTextCtrlUidChanged(self, event):
        """Handle event while the uid in the textctrl has been changed"""
        self.scenario.uid = self.window.widget_textctrl_scenario_uid.GetValue();
    # ----- List box -----
    def RefreshListbox(self):
        """Clear the data in listbox and put all data from scenario object into listbox"""
        self.HideAllEditArea()
        self.window.widget_listbox.Set(self.scenario.GetListboxArray())
        self.window.widget_textctrl_scenario_uid.SetValue(self.scenario.uid)
    def GetCurrentSelectAction(self):
        """Get the selected action. If no selection, return None."""
        selections = self.window.widget_listbox.GetSelections()
        if len(selections) > 0:
            return self.scenario.action_list[selections[0]]
        else:
            print "Current Select is None! That's strange!"
            return None
    def SaveActionToListbox(self, str):
        """Set the text to listbox's selected item"""
        selections = self.window.widget_listbox.GetSelections()
        if len(selections) > 0:
            print selections[0], "  +++  ", str
            self.window.widget_listbox.SetString(selections[0],str)
        else:
            print "Current Select is None! That's strange!"
    # ----- Edit Area -----
    def ShowEditArea(self, target):
        """Show edit area for specific type of action"""
        t = target.__class__
        if t in self.window.editarea_sizer_map:
            self.window.editarea_sizer_map[t].ShowItems(True)
        self.window.main_panel.Layout()
    def HideAllEditArea(self):
        """Hide all edit area"""
        for area in self.window.editarea_sizer_map:
            self.window.editarea_sizer_map[area].ShowItems(False)
        self.window.main_panel.Layout()
    def LoadEditAreaData(self, target):
        """Load data from selected action to edit area"""
        t = target.__class__
        if t in self.window.editarea_load_func_map:
            self.window.editarea_load_func_map[t](target)
    # ---------- Action Load & Save method ----------
    def ActionLoad_DefActor(self, action):
        self.window.widget_defactor_textctrl_id.ChangeValue(action.actor_id)
        self.window.widget_defactor_textctrl_name.ChangeValue(action.actor_name)
    def ActionSave_DefActor(self, event):
        action = self.GetCurrentSelectAction()
        if action != None:
            action.actor_id = self.window.widget_defactor_textctrl_id.GetValue()
            action.actor_name = self.window.widget_defactor_textctrl_name.GetValue()
            self.SaveActionToListbox(action.ToString())
    def ActionLoad_Dialogue(self, action):
        self.window.widget_dialogue_textctrl_id.ChangeValue(action.actor_id)
        self.window.widget_dialogue_textctrl_text.ChangeValue(action.text)
    def ActionSave_Dialogue(self, event):
        action = self.GetCurrentSelectAction()
        if action != None:
            action.actor_id = self.window.widget_dialogue_textctrl_id.GetValue()
            action.text = self.window.widget_dialogue_textctrl_text.GetValue()
            self.SaveActionToListbox(action.ToString())
class NewActionWindow(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, size = (320,420), title = "Add New Action")
        panel = wx.Panel(self)
        sizer = wx.GridSizer(rows = 5, cols = 3, vgap = 5, hgap = 5)
        
        btn_actordef = wx.Button(panel, label = "Actor Define")
        btn_dialogue = wx.Button(panel, label = "Dialogue")
        btn_set = wx.Button(panel, label = "Action Set")
        
        sizer.Add(btn_actordef)
        sizer.Add(btn_dialogue)
        sizer.Add(btn_set)
        
        panel.SetSizer(sizer)
        
        self.Bind(wx.EVT_BUTTON, self.OnBtnActorDef, btn_actordef )
        self.Bind(wx.EVT_BUTTON, self.OnBtnDialogue, btn_dialogue )
        self.Bind(wx.EVT_BUTTON, self.OnBtnSet, btn_set )
    def OnBtnActorDef(self, event):
        self.result = ActionDefineActor()
        self.result.CreateNew("-1","noname")
        self.Close()
    def OnBtnDialogue(self, event):
        self.result = ActionDialog()
        self.result.CreateNew("-1","no text")
        self.Close()
    def OnBtnSet(self, event):
        self.Close()