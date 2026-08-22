from chat_parser.yt_user import User
from chat_parser.chat_msg.yt_chat_msg import YTChatMsg


class YTChat:
    def __init__(self):
        self.chat: dict = {}

    def print_all_chatters(self):
        for item in self.chat:
            user_info: str = self.chat[item].get_all_user_messages()
            print(user_info)

    def add_user(self, user):
        self.chat[user.username] = user

    def add_message(self, username: str, yt_chat_msg: YTChatMsg):
        # If the chatter hasnt been added to the dictionary yet, create an entry
        # with a User object as a value, and a username as a key
        if username not in self.chat:
            self.chat[username] = User(username)
        # Add the message to the list of messages per each user object
        self.chat[username].add_message(yt_chat_msg)

    def get_total_unique_mods(self):
        total_mods = 0
        for item in self.chat:
            is_mod = False
            print()

    def write_to_file(self, filename):
        with open(filename, "w") as f:
            for item in self.chat:
                user_info = self.chat[item].get_all_user_messages()
                f.write(user_info)
                f.write("\n\n")
