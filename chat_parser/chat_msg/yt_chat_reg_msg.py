from chat_parser.chat_msg.yt_chat_msg import YTChatMsg

# A regular chat has all properties of a chat but also contains a moderator status


class YTChatRegMsg(YTChatMsg):
    def __init__(self, username, message, dt, rel_time, is_mod):
        super().__init__(username, message, dt, rel_time)
        self.is_mod: bool = is_mod

    def get_msg(self):
        mod: str = "[MOD]" if self.is_mod else "[NOR]"
        return f"{mod}{super().get_msg()}"
