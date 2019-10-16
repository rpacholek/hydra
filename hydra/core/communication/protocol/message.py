import json
from typing import Tuple

from ..network.message import Message 

class ProtocolMessage(Message):
    def __init__(self, payload={}, attachments=[]):
        self.payload = payload
        self.attachments = attachments

    #Message
    def loads_message(self, header: dict, body: str, attachments: list):
        self.payload = json.loads(body)
        self.attachments = attachments
        return self

    def dumps_message(self) -> Tuple[dict, str, list]:
        return {}, json.dumps(self.payload), self.attachments

    @staticmethod
    def get_message_type():
        return "protocol"
    #End Message 

    def get_info(self):
        return self.payload

    def get_attachments(self):
        return self.attachments


