from pprint import pprint
from typing import Final, Optional

import requests

from Modules.make_logger import make_logger

HOST: Final[str] = "https://misskey.io/api/"


class MisskeyIO:
    def __init__(self, token: str):
        self.token = token
        self.logger = make_logger("MisskeyIO")

    def note(self, text: str, reply_to: Optional[str] = None) -> dict:
        try:
            url = HOST + "notes/create"
            payload = {"i": self.token, "text": text}

            if reply_to:
                payload["replyId"] = reply_to

            response = requests.post(url, json=payload)

            return response.json()
        except Exception:
            self.logger.error("An error occurred", exc_info=True)
            return {}
