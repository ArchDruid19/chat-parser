from datetime import datetime, timedelta

# Parent class that will be inherited by YTRegChat and YTSuperChat
# All chat messages chat a username, message, and times linked to them, regardless
# if they are super chats or not


class YTChatMsg:
    def __init__(self, username, dt, rel_time):
        self.username: str = username
        self.dt: datetime = dt
        self.rel_time: timedelta = rel_time

    def get_timestamps(self) -> str:
        timestamp: str = f"[{self.dt.strftime("%Y-%m-%d@%H:%M:%S")}]"
        rel_timestamp: str = f"[R{str(self.rel_time).rstrip("0").rstrip(".")}]"
        return f"{timestamp}{rel_timestamp}"
