from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Tuple, Type
from io import BytesIO


class MessageException(Exception):
    pass


class Message(metaclass=ABCMeta):
    """
    header: information required to e.g. route to correct subsystem
        It is limited to carry only string values.
    body: information that the message is carrying
    attachments: lazy evaluated files that can be transported
    """

    @abstractmethod
    def loads_message(self, header: dict, body: str, attachments: list):
        pass

    @abstractmethod
    def dumps_message(self) -> Tuple[dict, str, list]:
        pass

    @staticmethod
    @abstractmethod
    def get_message_type() -> str:
        return "NoneType"

    def dumps(self) -> bytes:
        header, body, attachments = self.dumps_message()
        header = header.copy()
        header["type"] = self.get_message_type()

        return self._encode(header, body, attachments)

    @staticmethod
    def process(data: bytes) -> Tuple[str, dict, str, list]:
        header, body, attachments = Message._decode(data)
        typename = header.pop("type")

        return typename, header, body, attachments

    def loads(self, data: bytes) -> Type[Message]:
        processed = Message.process(data)
        self.loads_message(*processed[1:])
        return self

    @staticmethod
    def _encode(header, body, attachments):
        buf = BytesIO()
        Message._encode_header(buf, header)
        Message._encode_body(buf, body)
        Message._encode_attachments(buf, attachments)
        buf.seek(0)
        return buf.read()

    @staticmethod
    def _encode_header(buf, header):
        for key, value in header.items():
            buf.write("{}: {}\r\n".format(key, value).encode())
        buf.write(b"\r\n")

    @staticmethod
    def _encode_body(buf, body):
        buf.write(body.encode())
        buf.write(b"\r\n\r\n")

    @staticmethod
    def _encode_attachments(buf, attachments):
        pass

    @staticmethod
    def _decode(data):
        header_data, body, data = data.split(b"\r\n\r\n", 2)

        header = Message._decode_header(header_data)
        body = body.decode()
        attachments = Message._decode_attachments(data)

        return header, body, attachments

    @staticmethod
    def _decode_header(data) -> dict:
        header = {}
        data = data.decode()
        while data:
            if "\r\n" in data:
                value, data = data.split("\r\n", 1)
            else:
                value, data = data, None
            if ": " in value:
                lvalue, rvalue = value.split(": ", 1)
                header[lvalue] = rvalue
            else:
                print(f"Illformated {value.decode()}")
        return header

    @staticmethod
    def _decode_attachments(data) -> list:
        return []


class MessageProcessor:
    def __init__(self, *message_cls):
        self.message_types = {}
        for cls in message_cls:
            self.register(cls)

    def register(self, message_cl):
        self.message_types[message_cl.get_message_type()] = message_cl

    def loads(self, data) -> Type[Message]:
        typename, *content = Message.process(data)

        if typename in self.message_types:
            msg = self.message_types[typename]()
            msg.loads_message(*content)
            return msg
        raise MessageException(f"Unknown message type {typename}")
