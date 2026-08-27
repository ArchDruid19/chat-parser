from chat_parser.chat.yt_chat import YTChat
import chat_parser.chat.yt_chat_parser as yt
from PyQt6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QListWidget,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # YTChat
        self.yt_chat: YTChat = YTChat()

        # Widgets
        self.lst_chat: QListWidget = QListWidget()
        self.btn_open_chat: QPushButton = QPushButton("Open File")

        # Event handlers
        self.btn_open_chat.clicked.connect(self.open_json_file)

        # Main layout
        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.addWidget(self.lst_chat)
        main_layout.addWidget(self.btn_open_chat)

        main_widget: QWidget = QWidget()
        main_widget.setLayout(main_layout)

        # Main window
        self.setWindowTitle("Chat Viewer")
        self.setFixedSize(800, 600)
        self.setCentralWidget(main_widget)

    def open_json_file(self) -> str:
        file_path: tuple = QFileDialog.getOpenFileName(
            self,
            "Open Chat",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            self.yt_chat = yt.json_to_yt_chat([file_path[0]])
            self.fill_lst_chat()

    def fill_lst_chat(self):
        self.lst_chat.clear()
        for username in self.yt_chat.chat:
            self.lst_chat.addItem(username)
            for msg in self.yt_chat.chat[username].messages:
                self.lst_chat.addItem(msg.get_msg())
            self.lst_chat.addItem("\n")
