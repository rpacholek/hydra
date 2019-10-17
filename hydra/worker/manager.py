from typing import Type

from .node import WorkerNode
from ..core.node.manager import NodeManager
from ..core.node.base_node import Node
from ..core.action.executor import action_executor


class WorkerManager(NodeManager):
    def __init__(self, action_queue, config=None, env=None):
        super().__init__(action_queue, config.get("worker"), env)

    def get_class(self) -> Type[Node]:
        return WorkerNode

    @action_executor("job")
    def task_executor(self, action):
        action_type = action.get_type()
