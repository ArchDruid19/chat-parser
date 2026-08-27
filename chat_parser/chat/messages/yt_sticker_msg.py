from chat_parser.chat.messages.yt_msg import YTChatMsg


class YTChatSticker(YTChatMsg):
    def __init__(self, username, dt, rel_time, purchase_amt, sticker_type):
        super().__init__(username, dt, rel_time)
        self.purchase_amt: str = purchase_amt
        self.sticker_type: str = sticker_type

    def get_msg(self) -> str:
        return f"{super().get_timestamps()}({self.purchase_amt}) [(STICKER){self.sticker_type}]"
