from typing import Type
import asyncio

from ..action.executor import ActionExecutor, action_executor
from ..action.helper import action_cmp
from ..communication.network.listener import listener, connect
from .base_node import Node
from ..common.coro import *

class NodeManager(ActionExecutor):
    def __init__(self, action_queue, config=None, env=None):
        ActionExecutor.__init__(self)

        self.nodes = {}
        self.action_queue = action_queue
        self.config = config
        self.env = env

    def register(self, node):
        self.nodes[node.id] = node

    def remove(self, node):
        if not isinstance(node, str):
            node = node.id

        if node in self.nodes:
            del self.nodes[node]

    def get_class(self) -> Type[Node]:
        return Node

    def get_best(self) -> Node:
        """
        Get best node from manager.
        By default take the oldest registered.

        It is not specified what best means - implementation detail.
        """
        return next(iter(self.nodes.values()))

    ## Node Factory
    def create_node(self, device):
        print(f"ENV Create {self.env}")
        node = self.get_class()(device, self.action_queue, self.config, self.env)
        self.register(node)
        return node

    ###
    async def server(self, *args, coromanager=NoneCoroManager(), **kargs):
        await listener(self, self.config, coromanager)

    async def connect(self, *args, coromanager=NoneCoroManager(), **kwargs):
        for _try in range(5):
            await connect(self, self.config, coromanager)
            await asyncio.sleep(10)

    ### ActionExecutor
    @action_executor("maintenance.node")
    def maintenance_node_executor(self, action):
        # TODO: Will there be a multinode task action?
        #nodesid = action.get_nodes_id()
        #for nodeid in nodesid:
        
        # Find Node
        nodeid = action.get_node_id()
        node = self.nodes.get(nodeid)
        
        # Validate Node
        if not node or not node.is_alive():
            # TODO: Some event?
            return 
    
        # Exec action
        node.exec_action(action)

    @action_executor("event")
    def event_executor(self, action):
        pass

