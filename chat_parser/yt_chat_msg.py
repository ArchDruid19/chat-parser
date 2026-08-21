class YTChatMsg:
    def __init__(self, username, message, is_mod, dt, rel_time):
        self.username = username
        self.message = message
        self.is_mod = is_mod
        self.dt = dt
        self.rel_time = rel_time
        pass
