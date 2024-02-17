import wx
from chat import ChatClient

class MainMenu(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Main Menu", pos=wx.DefaultPosition,
                          size=wx.Size(300, 200), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.panel = wx.Panel(self)
        self.initUI()

    def initUI(self):
        layout = wx.BoxSizer(wx.VERTICAL)
        
        self.btn_message = wx.Button(self.panel, label="메시지")
        layout.Add(self.btn_message, 0, wx.ALL | wx.CENTER, 10)
        
        self.btn_message.Bind(wx.EVT_BUTTON, self.onMessageClicked)
        
        self.panel.SetSizer(layout)

    def onMessageClicked(self, event):
        chat_client = ChatClient(None)
        chat_client.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainMenu(None)
    frame.Show(True)
    app.MainLoop()
