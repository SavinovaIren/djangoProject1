import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse, GET_UPDATES_RESPONSE_SCHEMA, SEND_MESSAGE_RESPONSE_SCHEMA


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url("getUpdates")
        response = requests.get(url, params={"offset": offset, "timeout": timeout,
                                             "allowed_updates": ["update_id", "message"]})
        print(response.json())
        return GET_UPDATES_RESPONSE_SCHEMA.load(response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url("sendMessage")
        response = requests.post(url, params={"chat_id": chat_id, "text": text})
        print(response.json())
        return SEND_MESSAGE_RESPONSE_SCHEMA.load(response.json())