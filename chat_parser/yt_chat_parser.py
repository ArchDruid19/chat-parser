import json

from chat_parser.chat_msg.yt_chat_msg import YTChatMsg
from chat_parser.chat_msg.yt_chat_reg_msg import YTChatRegMsg
from chat_parser.chat_msg.yt_chat_super_msg import YTChatSuperMsg
from chat_parser.yt_chat import YTChat
from datetime import datetime, timezone, timedelta

# Read and clean a live-chat from a JSON file downloaded from yt-dlp
# We need: usernames, chat messages, moderator status
# This information should be exported to a cleaned, human-readable text file
# This is hell


def runs_list_to_chat_msg(runs_list: list) -> str:
    chat_msg: str = ""
    for runs_item in runs_list:
        if "text" in runs_item:
            chat_msg += runs_item["text"]
        if "emoji" in runs_item:
            # We are going to pray that a shortcut actually exists in the first idx
            if "shortcuts" in runs_item["emoji"]:
                emoji_shortcut: str = runs_item["emoji"]["shortcuts"][0]
                chat_msg += emoji_shortcut
            else:
                chat_msg += ":?:"
    return chat_msg


def add_reg_mesg_to_chat(
    live_chat_text_message_renderer: dict,
    chat_relative_timestamp: timedelta,
    chat: YTChat,
):
    chat_msg: str = ""
    chat_author: str = ""
    is_mod: bool = False
    chat_readable_timestamp: datetime

    # Most of the useful information we need is in the liveChatTextMessageRenderer
    # dictionary
    # the messege may be split into multiple objects
    # within the runs array depending on if emojis are used
    runs: list = live_chat_text_message_renderer.get("message", {}).get("runs")
    if runs:
        chat_msg = runs_list_to_chat_msg(runs)

    # Get the authors name
    author_simple_text: str = live_chat_text_message_renderer.get("authorName", {}).get(
        "simpleText"
    )
    if author_simple_text:
        chat_author = author_simple_text

    # Check if the author has a moderator tooltip
    author_badges: list = live_chat_text_message_renderer.get("authorBadges")
    if author_badges:
        for author_badges_item in author_badges:
            live_chat_author_badge_renderer_tooltip: str = author_badges_item.get(
                "liveChatAuthorBadgeRenderer"
            ).get("tooltip")
            if live_chat_author_badge_renderer_tooltip in "Moderator":
                is_mod = True

    # Get the actual unix millisecond timestamp the message was sent
    # as a datetime object
    chat_timestamp: str = live_chat_text_message_renderer.get("timestampUsec", "0")
    chat_readable_timestamp = datetime.fromtimestamp(
        int(chat_timestamp) / 1_000_000,
        tz=timezone.utc,
    )

    # Add the information we need to the Chat object
    if chat_author:
        yt_chat_msg = YTChatRegMsg(
            chat_author,
            chat_msg,
            chat_readable_timestamp,
            chat_relative_timestamp,
            is_mod,
        )

        chat.add_chat(chat_author, yt_chat_msg)


def add_super_msg_to_chat(
    live_chat_paid_message_renderer: dict,
    chat_relative_timestamp: timedelta,
    chat: YTChat,
):
    author_name: str = ""
    chat_msg: str = ""
    chat_readable_timestamp: datetime
    purchase_amt_text: str = ""

    if "authorName" in live_chat_paid_message_renderer:
        author_name = live_chat_paid_message_renderer.get("authorName").get(
            "simpleText", ""
        )
    if "message" in live_chat_paid_message_renderer:
        chat_msg = runs_list_to_chat_msg(
            live_chat_paid_message_renderer.get("message").get("runs", [])
        )
    if "timestampUsec" in live_chat_paid_message_renderer:
        chat_timestamp: str = live_chat_paid_message_renderer.get("timestampUsec", "0")
        chat_readable_timestamp = datetime.fromtimestamp(
            int(chat_timestamp) / 1_000_000,
            tz=timezone.utc,
        )
    if "purchaseAmountText" in live_chat_paid_message_renderer:
        purchase_amt_text = live_chat_paid_message_renderer.get(
            "purchaseAmountText"
        ).get("simpleText")

    if author_name:
        yt_chat_msg: YTChatMsg = YTChatSuperMsg(
            author_name,
            chat_msg,
            chat_readable_timestamp,
            chat_relative_timestamp,
            purchase_amt_text,
        )

        chat.add_chat(author_name, yt_chat_msg)


def json_to_yt_chat(filepaths: list) -> YTChat:
    tmpcnt = 1
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
                        json_dict.get("replayChatItemAction").get(
                            "videoOffsetTimeMsec", 0
                        )
                    )
                )
                # Check if the action list exists in the replayChatItemAction dict
                actions: list = json_dict.get("replayChatItemAction", []).get("actions")
                if actions:
                    for action_item in actions:
                        if "addChatItemAction" in action_item:
                            item: dict = action_item.get("addChatItemAction", {}).get(
                                "item"
                            )
                            if item:
                                if "liveChatTextMessageRenderer" in item:
                                    live_chat_text_message_renderer: dict = item.get(
                                        "liveChatTextMessageRenderer"
                                    )
                                    add_reg_mesg_to_chat(
                                        live_chat_text_message_renderer,
                                        chat_relative_timestamp,
                                        chat,
                                    )
                                elif "liveChatPaidMessageRenderer" in item:
                                    tmpcnt += 1
                                    live_chat_paid_message_renderer: dict = item.get(
                                        "liveChatPaidMessageRenderer"
                                    )
                                    add_super_msg_to_chat(
                                        live_chat_paid_message_renderer,
                                        chat_relative_timestamp,
                                        chat,
                                    )
                        elif "addLiveChatTickerItemAction" in action_item:
                            tmpcnt += 1
    print(tmpcnt)
    return chat
