from ScenarioEditor import MainWindow
from editor import EditorWindow
import wx

app = wx.App(False)
#frame = MainWindow(None,"Ahaworks Scenario Script Editor")
frame = EditorWindow(None, "Ahaworks Scenario Script Editor")
frame.Show()
app.MainLoop()