import wx
import socket
import threading
import pygame
import logging
import os
import sys

# 커맨드라인 인자를 기반으로 로깅 활성화 결정
if "log" in sys.argv:
    logging.basicConfig(filename='chat.log', level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s')
else:
    logging.basicConfig(level=logging.CRITICAL)  # 로그를 비활성화하거나, CRITICAL 메시지만 기록

def resource_path(relative_path):
    """리소스 파일의 경로를 얻습니다. PyInstaller 실행 시 필요합니다."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ChatClient(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Chat Client", pos=wx.DefaultPosition,
                          size=wx.Size(500, 400), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        if "log" in sys.argv:
            logging.info('Chat client initialized.')
        self.panel = wx.Panel(self)
        self.server_address = ('124.53.190.247', 5000)
        self.initUI()
        self.connect_to_server()
        self.start_receiving_messages()
        self.initialize_pygame()
        self.load_sounds()

    def initUI(self):
        if "log" in sys.argv:
            logging.info('Initializing UI: Starting.')
        layout = wx.BoxSizer(wx.VERTICAL)
        
        if "log" in sys.argv:
            logging.info('Initializing UI: Adding chat_display.')
        self.chat_display = wx.TextCtrl(self.panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.BORDER_SIMPLE, size=(-1, 150))
        layout.Add(self.chat_display, 0, wx.EXPAND | wx.ALL, 5)
        
        if "log" in sys.argv:
            logging.info('Initializing UI: Adding msg_entry.')
        self.msg_entry = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER, size=(-1, -1))
        layout.Add(self.msg_entry, 0, wx.EXPAND | wx.ALL, 5)
        self.msg_entry.Bind(wx.EVT_TEXT_ENTER, self.on_send_message)
        
        if "log" in sys.argv:
            logging.info('Initializing UI: Adding send_button.')
        self.send_button = wx.Button(self.panel, label="Send")
        layout.Add(self.send_button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.send_button.Bind(wx.EVT_BUTTON, self.on_send_message)
        
        self.panel.SetSizer(layout)
        if "log" in sys.argv:
            logging.info('Initializing UI: Completed.')

    def initialize_pygame(self):
        try:
            pygame.mixer.init()
            if "log" in sys.argv:
                logging.info('Pygame mixer initialized successfully.')
        except Exception as e:
            if "log" in sys.argv:
                logging.error(f'Failed to initialize pygame mixer: {e}')

    def load_sounds(self):
        try:
            self.sound_message_sent = pygame.mixer.Sound(resource_path("ms.ogg"))
            self.sound_message_received = pygame.mixer.Sound(resource_path("mr.ogg"))
            if "log" in sys.argv:
                logging.info('Sounds loaded successfully.')
        except Exception as e:
            if "log" in sys.argv:
                logging.error(f'Failed to load sounds: {e}')

    def connect_to_server(self):
        try:
            if "log" in sys.argv:
                logging.info(f'Attempting to connect to server at {self.server_address}.')
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(self.server_address)
            if "log" in sys.argv:
                logging.info('Successfully connected to server.')
        except Exception as e:
            if "log" in sys.argv:
                logging.error(f'Failed to connect to server: {e}')

    def start_receiving_messages(self):
        if "log" in sys.argv:
            logging.info('Starting thread for receiving messages.')
        thread = threading.Thread(target=self.receive_messages)
        thread.daemon = True
        thread.start()

    def on_send_message(self, event):
        msg = self.msg_entry.GetValue()
        if msg:
            try:
                self.client_socket.sendall(msg.encode('utf-8'))
                self.display_message("나", msg)
                self.msg_entry.Clear()
                self.play_sound(self.sound_message_sent)
                if "log" in sys.argv:
                    logging.info('Message sent.')
            except Exception as e:
                if "log" in sys.argv:
                    logging.error(f'Failed to send message: {e}')

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    wx.CallAfter(self.display_message, "상대", message)
                    wx.CallAfter(lambda: self.play_sound(self.sound_message_received))
                    if "log" in sys.argv:
                        logging.info('Message received.')
            except Exception as e:
                if "log" in sys.argv:
                    logging.error(f'Error receiving message: {e}')
                break

    def play_sound(self, sound):
        try:
            sound.play()
            if "log" in sys.argv:
                logging.info('Sound played successfully.')
        except Exception as e:
            if "log" in sys.argv:
                logging.error(f'Failed to play sound: {e}')

    def display_message(self, sender, message):
        formatted_message = f"{sender}: {message}\n"
        self.chat_display.AppendText(formatted_message)

if __name__ == "__main__":
    app = wx.App(False)
    frame = ChatClient(None)
    frame.Show(True)
    app.MainLoop()
