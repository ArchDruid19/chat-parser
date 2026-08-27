from chat_parser.chat.messages.yt_msg import YTChatMsg

# Represents a user in the chat
# Each user has a username and a list of messages that they
# have sent


class User:
    def __init__(self, username):
        self.username: str = username
        self.messages: list = []

    def add_chat(self, yt_chat_msg):
        self.messages.append(yt_chat_msg)

    def get_all_user_chats(self):
        lines: list = []
        lines.append(self.username)
        count: int = 1
        item: YTChatMsg
        for item in self.messages:
            lines.append(str(count) + ":" + item.get_msg())
            count += 1
        return "\n".join(lines)
