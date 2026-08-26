from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QListWidget,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self, yt_chat):
        super().__init__()
        # YTChat we have to pass in so we can display the information
        self.yt_chat = yt_chat

        # Widgets
        self.lst_chat = QListWidget()

        # Event handlers
        # main_btn.clicked.connect(self.do_somthing)
        self.fill_lst_chat()

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.lst_chat)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        # Main window
        self.setWindowTitle("Chat Viewer")
        self.setFixedSize(800, 600)
        self.setCentralWidget(main_widget)

    def fill_lst_chat(self):
        for username in self.yt_chat.chat:
            self.lst_chat.addItem(username)
            for msg in self.yt_chat.chat[username].messages:
                self.lst_chat.addItem(msg.get_msg())
            self.lst_chat.addItem("\n")
