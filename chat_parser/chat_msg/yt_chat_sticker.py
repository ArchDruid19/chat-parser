from chat_parser.chat_msg.yt_chat_msg import YTChatMsg


class YTChatSticker(YTChatMsg):
    def __init__(self, username, message, dt, rel_time, purchase_amt, sticker_type):
        super().__init__(username, message, dt, rel_time)
        self.purchase_amt = purchase_amt
        self.sticker_type = sticker_type
    pass
