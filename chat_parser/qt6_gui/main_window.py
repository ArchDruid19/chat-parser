from chat_parser.chat.yt_chat import YTChat
import chat_parser.chat.yt_chat_parser as yt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
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

        # Top menu bar (from QMainWindow)
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        file_open_action = QAction("Open", self)
        file_menu.addAction(file_open_action)

        # Search layout
        self.btn_search_user: QPushButton = QPushButton("Search")
        self.txt_search_user: QLineEdit = QLineEdit()

        search_layout_hbox = QHBoxLayout()
        search_layout_hbox.addWidget(self.btn_search_user)
        search_layout_hbox.addWidget(self.txt_search_user)

        search_layout_widget = QWidget()
        search_layout_widget.setLayout(search_layout_hbox)

        # Main layout
        main_layout: QVBoxLayout = QVBoxLayout()
        main_layout.addWidget(self.lst_chat)
        main_layout.addWidget(search_layout_widget)

        main_widget: QWidget = QWidget()
        main_widget.setLayout(main_layout)

        # Main window
        self.setWindowTitle("Chat Viewer")
        self.setFixedSize(600, 400)
        self.setCentralWidget(main_widget)

        # Event handlers
        self.btn_search_user.clicked.connect(self.search_user)
        file_open_action.triggered.connect(self.open_json_file)

    def open_json_file(self) -> str:
        file_path: tuple = QFileDialog.getOpenFileName(
            self, "Open Chat", "", "JSON Files (*.json);;All Files (*)"
        )

        if file_path[0]:
            self.yt_chat = yt.json_to_yt_chat([file_path[0]])
            self.fill_lst_chat()

    def fill_lst_chat(self):
        self.lst_chat.clear()
        for username in self.yt_chat.chat:
            self.lst_chat.addItem(username)
            for msg in self.yt_chat.chat[username].messages:
                self.lst_chat.addItem(msg.get_msg())
            self.lst_chat.addItem("\n")

    def search_user(self):
        print(self.lst_chat.item(0))
        pass
