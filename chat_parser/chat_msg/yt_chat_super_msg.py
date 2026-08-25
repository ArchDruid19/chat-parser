from chat_parser.chat_msg.yt_chat_msg import YTChatMsg

# A super chat has all properties of a chat but also contains a purchase ammount


class YTChatSuperMsg(YTChatMsg):
    def __init__(self, username, dt, rel_time, purchase_amt, message):
        super().__init__(username, dt, rel_time)
        self.purchase_amt: str = purchase_amt
        self.message: str = message

    def get_msg(self) -> str:
        return f"{super().get_timestamps()}({self.purchase_amt}) {self.message}"
