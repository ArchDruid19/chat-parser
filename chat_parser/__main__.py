from chat_parser.qt6_gui.main_window import MainWindow
from chat_parser.yt_chat import YTChat
import chat_parser.yt_chat_parser as yt
from PyQt6.QtWidgets import QApplication, QMainWindow


def main():
    chatters: YTChat = yt.json_to_yt_chat(
       [
           "chat-data/raw_data/FORTNITE-ZONE-WARS-GONE-WRONG-live_chat.json"
       ]
    )
    app = QApplication([])
    window = MainWindow(chatters)
    window.show()
    app.exec()
    # chatters.print_all_chatters()
    # print(chatters.chat["@connorsommer2114"].get_all_user_chats())
    # chatters.write_to_file("chat-data/cleaned_data/fortniteugh.txt")


if __name__ == "__main__":
    main()
