from chat_parser.yt_chat import YTChat
import chat_parser.yt_chat_parser as yt


def main():
    chatters: YTChat = yt.json_to_yt_chat(
        [
            "chat-data/raw_data/FORTNITE-ZONE-WARS-GONE-WRONG-live_chat.json"
        ]
    )
    #chatters.print_all_chatters()
    chatters.write_to_file("chat-data/cleaned_data/fortnite2.txt")


if __name__ == "__main__":
    main()
