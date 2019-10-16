from enum import Enum
import asyncio

from ..action.executor import ActionExecutor
from ..environment import RemoteEnvironment, NodeType

from ..communication.protocol import AdvancedProtocol

NodeStatus = Enum("NodeStatus", "Init Running Paused Stoped Failed Unknown")

class Node(ActionExecutor):
    def __init__(self, device, action_queue, config=None, env=None):
        ActionExecutor.__init__(self)

        self.id = id(self)

        self.action_queue = action_queue
        self.config = config
        self.device = device
        print(f"ENV NODE: {env}")
        self.local_env = env
        self.remote_env = RemoteEnvironment()

        #TODO: Protocol should be passed via factory 
        self.protocol = AdvancedProtocol(
                {"expected_type": self.node_type()}, 
                self.local_env, 
                self.remote_env, 
                self.config)

        self.status = NodeStatus.Init

    async def init(self):
        await self.run_protocol()

    async def run_protocol(self):
        if self.protocol:
            print("Init")
            self.protocol.init()
            for s in self.protocol.get_send_content():
                await self.device.send(s)

            while not self.protocol.is_ready() and not self.protocol.has_failed():
                print("Recv")
                data = await self.device.recv()
                if data:
                    self.protocol.receive(data)
                for s in self.protocol.get_send_content():
                    await self.device.send(s)
                if not self.device.is_alive():
                    raise Exception("Connection closed")

        else:
            raise Exception("Unknown protocol")

    async def run(self, *args, **kwargs):
        await self.init()
        if self.protocol and self.protocol.has_failed():
            self.status = NodeStatus.Failed
            self.device.close()
            return

        self.status = NodeStatus.Running

        print("Start")
        while True:
            message = await self.device.recv()
            # TODO: Process

    def process(self, message):
        pass

    def close(self):
        self.device.close()
        self.action_queue.push(
            Action(
                "event.node.closed",
                nodeid=self.id
            )
        )

    def is_alive(self):
        return self.device.is_alive() 

    def node_type(self):
        return NodeType.Undefined

    ## Private functions
    
    ### Action helper
    def send(self, action):
        self.device.send(action)

"""
Example impl:

class Worker(Node):
    ...
    @action_executor("job.execute")
    def execute(self, action):
        self.send(action)
    ...
"""
