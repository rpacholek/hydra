from typing import Type
from enum import Enum, auto

from .message import Message

class ConnMaster(Enum):
    SERVER = auto()
    CLIENT = auto()

class Device:
    def __init__(self, rstream, wstream, conn_type):
        self.receiver = Receiver(rstream)
        self.sender = Sender(wstream)
        self.conn_type = conn_type

    def send(self, message: Type[Message]):
        self.sender.send(message)

    async def recv(self):
        return await self.receiver.recv()

    def is_master(self):
        return self.conn_type == ConnMaster.SERVER

    def is_alive(self) -> bool:
        return not self.receiver.is_closed()

class Receiver:
    def __init__(self, rstream):
        self.rstream = rstream

    async def recv(self):
        data = None
        data_len = (await self.rstream.read(5)).decode()
        if data_len and set(data_len).issubset(set(" 0123456789")):
            data_len = int(data_len)
            data = await self.rstream.read(data_len)
        elif not data:
            print("Socket received EOF - closing")
        else:
            print("Package not starting with len")
        return data

    def is_closed(self):
        return self.rstream.at_eof()

class Sender:
    def __init__(self, wstream):
        self.wstream = wstream

    def send(self, message):
        data = message.dumps() 
        # Send stream len
        self.wstream.write("{:<5}".format(len(data)).encode())
        # Send data
        self.wstream.write(data)

    async def close(self):
        self.wstream.close()
        await self.wstream.wait_closed()
