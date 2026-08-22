# Represents a user in the chat
# Each user has a username and a list of messages that they
# have sent


from chat_parser.chat_msg.yt_chat_msg import YTChatMsg


class User:
    def __init__(self, username):
        self.username: str = username
        self.messages: list = []

    def add_message(self, yt_chat_msg):
        self.messages.append(yt_chat_msg)

    def get_all_user_messages(self):
        lines: list = []
        lines.append(self.username)
        count: int = 1
        item: YTChatMsg
        for item in self.messages:
            lines.append(str(count) + ":" + item.get_msg())
            count += 1
        return "\n".join(lines)
