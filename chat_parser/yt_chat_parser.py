import json

from chat_parser.chat_msg.yt_chat_msg import YTChatMsg
from chat_parser.chat_msg.yt_chat_reg_msg import YTChatRegMsg
from chat_parser.chat_msg.yt_chat_sticker import YTChatSticker
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
                # It seems like some (or perhaps all) IOS
                # emojis don't have a shortcut field, and there is
                # no other metadata on the emoji available in the JSON
                chat_msg += ":?:"
    return chat_msg


def get_renderer_info(renderer_type: dict) -> dict:
    chat_author: str = ""
    chat_msg: str = ""
    chat_readable_timestamp: datetime

    # Get the chat authors name
    if "authorName" in renderer_type:
        chat_author = renderer_type.get("authorName").get("simpleText", "")

    # The messege may be split into multiple objects
    # within the runs array, depending on if emojis are used
    if "message" in renderer_type:
        chat_msg = runs_list_to_chat_msg(renderer_type.get("message").get("runs", []))

    # Get the actual unix millisecond timestamp the message was sent
    # as a datetime object
    if "timestampUsec" in renderer_type:
        chat_timestamp: str = renderer_type.get("timestampUsec", "0")
        chat_readable_timestamp = datetime.fromtimestamp(
            int(chat_timestamp) / 1_000_000,
            tz=timezone.utc,
        )
    return {"author": chat_author, "msg": chat_msg, "usec": chat_readable_timestamp}


def add_reg_mesg_to_chat(
    live_chat_text_message_renderer: dict,
    chat_relative_timestamp: timedelta,
    chat: YTChat,
):
    is_mod: bool = False
    renderer_info: dict = get_renderer_info(live_chat_text_message_renderer)

    # Check if the author has a moderator tooltip/badge
    if "authorBadges" in live_chat_text_message_renderer:
        author_badges: list = live_chat_text_message_renderer.get("authorBadges", [])
        for author_badges_item in author_badges:
            live_chat_author_badge_renderer_tooltip: str = author_badges_item.get(
                "liveChatAuthorBadgeRenderer"
            ).get("tooltip")
            if live_chat_author_badge_renderer_tooltip in "Moderator":
                is_mod = True

    # Add the information we need to the Chat object
    if renderer_info["author"]:
        yt_chat_msg = YTChatRegMsg(
            renderer_info["author"],
            renderer_info["usec"],
            chat_relative_timestamp,
            is_mod,
            renderer_info["msg"],
        )
        chat.add_chat(renderer_info["author"], yt_chat_msg)


def add_super_msg_to_chat(
    live_chat_paid_message_renderer: dict,
    chat_relative_timestamp: timedelta,
    chat: YTChat,
):
    purchase_amt_text: str = ""
    renderer_info: dict = get_renderer_info(live_chat_paid_message_renderer)

    if "purchaseAmountText" in live_chat_paid_message_renderer:
        purchase_amt_text = live_chat_paid_message_renderer.get(
            "purchaseAmountText"
        ).get("simpleText")

    if renderer_info["author"]:
        yt_chat_msg: YTChatMsg = YTChatSuperMsg(
            renderer_info["author"],
            renderer_info["usec"],
            chat_relative_timestamp,
            purchase_amt_text,
            renderer_info["msg"],
        )

        chat.add_chat(renderer_info["author"], yt_chat_msg)


def add_sticker_msg_to_chat(
    live_chat_paid_sticker_renderer: dict,
    chat_relative_timestamp: timedelta,
    chat: YTChat,
):
    purchase_amt_text: str = ""
    # There is no message for a sticker, so we will have to get
    # the type of sticker through a differant dictionary item
    renderer_info: dict = get_renderer_info(live_chat_paid_sticker_renderer)
    sticker_type: str = ""

    if "purchaseAmountText" in live_chat_paid_sticker_renderer:
        purchase_amt_text = live_chat_paid_sticker_renderer.get(
            "purchaseAmountText"
        ).get("simpleText")

    if "sticker" in live_chat_paid_sticker_renderer:
        sticker_type = (
            live_chat_paid_sticker_renderer.get("sticker")
            .get("accessibility")
            .get("accessibilityData")
            .get("label")
        )
    if renderer_info["author"]:
        yt_chat_sticker = YTChatSticker(
            renderer_info["author"],
            renderer_info["usec"],
            chat_relative_timestamp,
            purchase_amt_text,
            sticker_type,
        )

        chat.add_chat(renderer_info["author"], yt_chat_sticker)


def json_to_yt_chat(filepaths: list) -> YTChat:
    tmpcnt = 0
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
                                    # tmpcnt += 1
                                elif "liveChatPaidMessageRenderer" in item:
                                    live_chat_paid_message_renderer: dict = item.get(
                                        "liveChatPaidMessageRenderer"
                                    )
                                    add_super_msg_to_chat(
                                        live_chat_paid_message_renderer,
                                        chat_relative_timestamp,
                                        chat,
                                    )
                                    # tmpcnt += 1
                                elif "liveChatPaidStickerRenderer":
                                    live_chat_paid_sticker_renderer: dict = item.get(
                                        "liveChatPaidStickerRenderer"
                                    )
                                    if live_chat_paid_sticker_renderer:
                                        add_sticker_msg_to_chat(
                                            live_chat_paid_sticker_renderer,
                                            chat_relative_timestamp,
                                            chat,
                                        )
                                        tmpcnt += 1

    print(tmpcnt)
    return chat
