import enum
from typing import Type

from ...environment import *
from ..network.message import Message
from .message import ProtocolMessage

class ProtocolStatus(enum.Enum):
    Success = 0
    Failed = 1
    Waiting = 2

class Protocol:
    def __init__(self, info, local_env, remote_env, config):
        print(f"ENV: {local_env}")
        self.local_env = local_env
        self.remote_env = remote_env
        self.info = info
        self.config = config
        self.stage = None
        self.steps = [
            NoConnectionProtocol
        ]
        self.__step_iter = None
        self.status = ProtocolStatus.Waiting

        self.send_buffer = []

    def init(self):
        print("Init protocol")
        self.__step_iter = iter(self.steps)
        self.__next_step()

    def has_failed(self):
        return self.status == ProtocolStatus.Failed

    def error(self):
        self.status = ProtocolStatus.Failed

    def receive(self, data):
        if self.stage:
            print(data)
            self.stage.receive(ProtocolMessage().loads(data))
            
            if self.stage.status == ProtocolStatus.Failed:
                self.error()
            elif self.stage.status == ProtocolStatus.Success:
                self.__next_step()
        else:
            self.error()

    def get_send_content(self):
        buf = self.send_buffer[:]
        self.send_buffer.clear()
        return buf

    def set_steps(self, steps):
        self.steps = steps
        self.__step_iter = iter(steps)

    def is_ready(self):
        return self.status == ProtocolStatus.Success
    
    def __next_step(self):
        print("Next step")
        step = next(self.__step_iter, None)
        if step:
            print(step)
            self.stage = step(self.send_buffer, self.info, self.local_env, self.remote_env, self.config)
            self.stage.init()
        else:
            print("Protocol ended successfuly")
            self.status = ProtocolStatus.Success

class ProtocolStep:
    def __init__(self, send_buffer, info, local_env, remote_env, config):
        self.send_buffer = send_buffer
        self.info = info
        self.local_env = local_env
        self.remote_env = remote_env
        self.config = config
        self.status = ProtocolStatus.Waiting

    def send(self, data: Type[Message]):
        print(data)
        self.send_buffer.append(data)

    def receive(self, message):
        return None

    def finish(self):
        self.status = ProtocolStatus.Success

    def failed(self):
        self.status = ProtocolStatus.Failed

class NoConnectionProtocol(ProtocolStep):
    def init(self):
        self.failed()

