from typing import Tuple

from ..common.serializer import Serializable
from ..communication.network.message import Message


class Action(Message):
    def __init__(self, action_type=None, attachments={}, content={}, **kwargs):
        self.action_type = action_type
        self.attachments = attachments
        self.dict = content

    def get_type(self):
        return self.action_type

    def add_attachment(self, name, attachment):
        self.attachments[name] = attachment

    def get_attachments(self):
        return self.attachments

    def get_attachment(self, name):
        return self.attachments[name]

    def get_body(self):
        return self.dict

    # ?
    def clone(self):
        pass

    # Message
    @staticmethod
    def get_message_type():
        return "action"

    def loads_message(self, header: dict, body: str, attachments: list):
        self.action_type = header["action_type"]
        self.dict = json.loads(body)
        self.attachments = attachments
        return self

    def dumps_message(self) -> Tuple[dict, str, list]:
        return {"action_type": self.action_type}, json.dumps(self.dict), attachments
