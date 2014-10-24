from editor import EditorWindow
import wx

app = wx.App(False)
frame = EditorWindow(None, "Ahaworks Scenario Script Editor")
frame.Show()
app.MainLoop()