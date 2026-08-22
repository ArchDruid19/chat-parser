from chat_parser.chat_msg.yt_chat_msg import YTChatMsg

# A super chat has all properties of a chat but also contains a purchase ammount


class YTChatSuperMsg(YTChatMsg):
    def __init__(self, username, message, dt, rel_time, purchase_amt):
        super().__init__(username, message, dt, rel_time)
        self.purchase_amt = purchase_amt

    def get_msg(self):
        return f"({self.purchase_amt}){super().get_msg()}"
