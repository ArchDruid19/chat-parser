import json

from chat_parser.yt_chat import YTChat
from datetime import datetime, timezone, timedelta


# Read and clean a live-chat from a JSON file downloaded from yt-dlp
# We need: usernames, chat messages, moderator status
# This information should be exported to a cleaned, human-readable text file
# This is hell
def json_to_yt_chat(filepaths: list) -> YTChat:
    chat: YTChat = YTChat()
    for filepath in filepaths:
        with open(filepath) as f:
            # Loop for each line in the json file
            for json_object in f:
                chat_msg: str = ""
                chat_author: str = ""
                is_mod: bool = False
                chat_timestamp: str = ""
                chat_readable_timestamp: str = ""
                chat_relative_timestamp: str = ""
                # Each JSON object is a dictionary
                json_dict: dict = json.loads(json_object)
                # Check if the replayChatItemAction field exists
                replay_chat_item_action = json_dict.get("replayChatItemAction")
                if replay_chat_item_action:
                    # Get the relative timestamp of the message as a timedelta object, which is when
                    # it was sent relative to the livestream duration
                    chat_relative_timestamp = timedelta(
                        milliseconds=int(replay_chat_item_action["videoOffsetTimeMsec"])
                    )
                    # Check if the action list exists in the replayChatItemAction dict
                    actions = replay_chat_item_action.get("actions")
                    if actions:
                        # Each action_item is a dictionary
                        for action_item in actions:
                            add_chat_item_action = action_item.get("addChatItemAction")
                            if add_chat_item_action:
                                item = add_chat_item_action.get("item")
                                if item:
                                    live_chat_text_message_renderer = item.get(
                                        "liveChatTextMessageRenderer"
                                    )
                                    # Most of the useful information we need is in the liveChatTextMessageRenderer
                                    # dictionary
                                    if live_chat_text_message_renderer:
                                        message = live_chat_text_message_renderer.get(
                                            "message"
                                        )
                                        if message:
                                            # Get the user message
                                            # the messege may be split into multiple objects
                                            # within the runs array, so we have to concatenate
                                            # We also have to worry about emojis in the runs array,
                                            # which are broken up in the json between text
                                            runs = message.get("runs")
                                            if runs:
                                                for runs_item in runs:
                                                    tmp_msg = runs_item.get("text")
                                                    if tmp_msg:
                                                        chat_msg += tmp_msg
                                                    if "emoji" in runs_item:
                                                        # We are going to pray that a shortcut actually exists in the first idx
                                                        emoji_shortcut = runs_item["emoji"]["shortcuts"][0]
                                                        chat_msg += emoji_shortcut

                                        # Get the authors name
                                        author_name = (
                                            live_chat_text_message_renderer.get(
                                                "authorName"
                                            )
                                        )
                                        if author_name:
                                            simple_text = author_name.get("simpleText")
                                            if simple_text:
                                                chat_author = simple_text
                                        author_badges = (
                                            live_chat_text_message_renderer.get(
                                                "authorBadges"
                                            )
                                        )
                                        # Check if the author has a moderator tooltip, which will
                                        # indicate if they are a mod or normal user
                                        if author_badges:
                                            for author_badges_item in author_badges:
                                                live_chat_author_badge_renderer_tooltip = author_badges_item.get(
                                                    "liveChatAuthorBadgeRenderer"
                                                ).get(
                                                    "tooltip"
                                                )
                                                if (
                                                    live_chat_author_badge_renderer_tooltip
                                                    in "Moderator"
                                                ):
                                                    is_mod = True
                                        # Get the actual unix millisecond timestamp the message was sent
                                        # (DELETE THIS IN PLACE OF DATETIME OBJECT)
                                        chat_timestamp = (
                                            live_chat_text_message_renderer.get(
                                                "timestampUsec"
                                            )
                                        )

                                        # Get the actual unix millisecond timestamp the message was sent
                                        # as a datetime object
                                        chat_readable_timestamp = (
                                            datetime.fromtimestamp(
                                                int(chat_timestamp) / 1_000_000,
                                                tz=timezone.utc,
                                            )
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
    return chat
