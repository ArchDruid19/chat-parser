import json

from chat_parser.yt_chat import YTChat
from datetime import datetime, timezone, timedelta

# Read and clean a live-chat from a JSON file downloaded from yt-dlp
# We need: usernames, chat messages, moderator status
# This information should be exported to a cleaned, human-readable text file
# This is hell


def add_reg_mesg_to_chat(
    live_chat_text_message_renderer: dict,
    chat_relative_timestamp: timedelta,
    chat: YTChat,
):
    chat_msg: str = ""
    chat_author: str = ""
    is_mod: bool = False
    chat_timestamp: str = ""
    chat_readable_timestamp: datetime
    # Most of the useful information we need is in the liveChatTextMessageRenderer
    # dictionary
    if live_chat_text_message_renderer:
        # the messege may be split into multiple objects
        # within the runs array depending on if emojis are used
        runs: list = live_chat_text_message_renderer.get("message", {}).get("runs")
        if runs:
            for runs_item in runs:
                if "text" in runs_item:
                    chat_msg += runs_item["text"]
                if "emoji" in runs_item:
                    # We are going to pray that a shortcut actually exists in the first idx
                    if "shortcuts" in runs_item["emoji"]:
                        emoji_shortcut: str = runs_item["emoji"]["shortcuts"][0]
                        chat_msg += emoji_shortcut
                    else:
                        chat_msg += ":?:"

        # Get the authors name
        author_simple_text: str = live_chat_text_message_renderer.get("authorName", {}).get(
            "simpleText"
        )
        if author_simple_text:
            chat_author = author_simple_text
        author_badges: list = live_chat_text_message_renderer.get("authorBadges")
        # Check if the author has a moderator tooltip
        if author_badges:
            for author_badges_item in author_badges:
                live_chat_author_badge_renderer_tooltip: str = author_badges_item.get(
                    "liveChatAuthorBadgeRenderer"
                ).get("tooltip")
                if live_chat_author_badge_renderer_tooltip in "Moderator":
                    is_mod = True
        # Get the actual unix millisecond timestamp the message was sent
        # (DELETE THIS IN PLACE OF DATETIME OBJECT)
        chat_timestamp = live_chat_text_message_renderer.get("timestampUsec")

        # Get the actual unix millisecond timestamp the message was sent
        # as a datetime object
        chat_readable_timestamp = datetime.fromtimestamp(
            int(chat_timestamp) / 1_000_000,
            tz=timezone.utc,
        )
    # Add the information we need to the Chat object
    if chat_author:
        chat.add_message(
            chat_author,
            chat_msg,
            is_mod,
            chat_timestamp,
            chat_readable_timestamp,
            chat_relative_timestamp,
        )


def json_to_yt_chat(filepaths: list) -> YTChat:
    chat: YTChat = YTChat()
    for filepath in filepaths:
        with open(filepath) as f:
            # Loop for each line in the json file
            for json_object in f:
                # Each JSON object is a dictionary
                json_dict: dict = json.loads(json_object)
                # Get when the message was sent relative to the livestream duration
                chat_relative_timestamp: timedelta = timedelta(
                    milliseconds=int(
                        json_dict.get("replayChatItemAction").get("videoOffsetTimeMsec")
                    )
                )
                # Check if the action list exists in the replayChatItemAction dict
                actions: list = json_dict.get("replayChatItemAction").get("actions")
                if actions:
                    for action_item in actions:
                        item: dict = action_item.get("addChatItemAction", {}).get(
                            "item"
                        )
                        if item:
                            live_chat_text_message_renderer: dict = item.get(
                                "liveChatTextMessageRenderer"
                            )
                            add_reg_mesg_to_chat(
                                live_chat_text_message_renderer,
                                chat_relative_timestamp,
                                chat,
                            )

    return chat
