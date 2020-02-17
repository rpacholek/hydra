from typing import Type

from .node import SupervisorNode
from ..core.node.manager import NodeManager
from ..core.node.base_node import Node
from ..core.action.executor import action_executor, executor_forwarder
from ..core.common.coro import NoneCoroManager


class SupervisorManager(NodeManager):
    def __init__(self, action_queue, config=None, env=None):
        super().__init__(action_queue, config.get("supervisor"), env)

    def get_class(self) -> Type[Node]:
        return SupervisorNode

    @action_executor("event")
    def task_executor(self, action):
        action_type = action.get_type()

    @action_executor(executor_forwarder(SupervisorNode))
    def forward(self, action):
        if len(self.nodes) == 1:
            list(self.nodes.values())[0].exec_action(action)
