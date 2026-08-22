from datetime import datetime, timedelta

# Parent class that will be inherited by YTRegChat and YTSuperChat
# All chat messages chat a username, message, and times linked to them, regardless
# if they are super chats or not


class YTChatMsg:
    def __init__(self, username, message, dt, rel_time):
        self.username: str = username
        self.message: str = message
        self.dt: datetime = dt
        self.rel_time: timedelta = rel_time

    def get_msg(self):
        timestamp: str = "[" + self.dt.strftime("%Y-%m-%d@%H:%M:%S") + "]"
        rel_timestamp: str = "[R" + str(self.rel_time) + "]"
        line: str = timestamp + rel_timestamp + " " + self.message + " "
        return line
