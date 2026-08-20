# Represents a user in the chat
# Each user has a username and a list of messages that they
# have sent

class User:
    def __init__(self, username):
        self.username = username
        self.messages = []

    def add_message(self, message, is_mod, timestamp, dt, rel_time):
        self.messages.append(
            {
                "message": message,
                "is_mod": is_mod,
                "timestamp": timestamp,
                "readable_time": dt,
                "relative_time": rel_time,
            }
        )

    def get_messages(self):
        lines = []
        lines.append(self.username)
        count = 1
        for item in self.messages:
            mod = "[MOD]" if item["is_mod"] else "[NOR]"
            timestamp = "[" + item["readable_time"].strftime("%Y-%m-%d@%H:%M:%S") + "]"
            rel_timestamp = "[R" + str(item["relative_time"]) + "]"
            lines.append(
                str(count)
                + mod
                + timestamp
                + rel_timestamp
                + " "
                + item["message"]
                + " "
            )
            count += 1
        return "\n".join(lines)
