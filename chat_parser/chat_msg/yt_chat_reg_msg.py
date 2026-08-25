from chat_parser.chat_msg.yt_chat_msg import YTChatMsg

# A regular chat has all properties of a chat but also contains a moderator status


class YTChatRegMsg(YTChatMsg):
    def __init__(self, username, dt, rel_time, is_mod, message):
        super().__init__(username, dt, rel_time)
        self.is_mod: bool = is_mod
        self.message: str = message

    def get_msg(self) -> str:
        mod: str = "[MOD]" if self.is_mod else ""
        return f"{mod}{super().get_timestamps()} {self.message}"
