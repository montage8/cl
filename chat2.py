import wx
import socket
import threading

class ChatClient(wx.Frame):
    
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Chat Client", pos=wx.DefaultPosition,
                          size=wx.Size(500, 400), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        
        self.panel = wx.Panel(self)
        self.server_address = ('124.53.190.247', 5000)
        self.initUI()
        self.connect_to_server()
        self.start_receiving_messages()

    def initUI(self):
        layout = wx.BoxSizer(wx.VERTICAL)
        
        self.chat_display = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_SIMPLE, size=(-1, 150))
        layout.Add(self.chat_display, 0, wx.EXPAND | wx.ALL, 5)
        
        self.msg_entry = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, size=(-1, -1))
        layout.Add(self.msg_entry, 0, wx.EXPAND | wx.ALL, 5)
        self.msg_entry.Bind(wx.EVT_TEXT_ENTER, self.on_send_message)
        
        self.send_button = wx.Button(self.panel, label="Send")
        layout.Add(self.send_button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send_message)
        
        self.panel.SetSizer(layout)

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)

    def start_receiving_messages(self):
        thread = threading.Thread(target=self.receive_messages)
        thread.daemon = True
        thread.start()

    def on_send_message(self, event):
        msg = self.msg_entry.GetValue()
        if msg:
            self.client_socket.sendall(msg.encode('utf-8'))
            self.display_message("나", msg)  # Display the message in the chat display as "My" message
            self.msg_entry.Clear()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    # Assume all received messages are from "the other"
                    wx.CallAfter(self.display_message, "상대", message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def display_message(self, sender, message):
        formatted_message = f"{sender}: {message}\n"
        self.chat_display.AppendText(formatted_message)

if __name__ == "__main__":
    app = wx.App(False)
    frame = ChatClient(None)
    frame.Show(True)
    app.MainLoop()
