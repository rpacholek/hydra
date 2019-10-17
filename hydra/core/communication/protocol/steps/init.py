import random

from ..base import *
from ..exceptions import *
from ....environment import NodeType


class InitProtocol(ProtocolStep):
    def init(self):
        self.send(self.m_init())

    def receive(self, message: Type[Message]):
        info = message.get_info()
        expected_type = self.info.get("expected_type")
        received_type = NodeType.into_type(info["node_type"])
        if expected_type and (expected_type != received_type and expected_type != NodeType.Undefined):
            raise NodeConnectionException(
                f"Not expected type {info['node_type']}, expected {expected_type}")
        self.remote_env.set_node_type(expected_type)

        # TODO: Check the steps, for now there is only one protocol

        self.finish()

    def m_init(self):
        return ProtocolMessage({
            "node_type": self.local_env.get_node_type().value,
            "protocol_steps": [],
            "timeout": 60,
            "version": "0.0.1",
            # if both nodes are the same
            "magic_number": random.randint(1, 10000),
        })
        # TODO: Implement retry if magic_number equal
