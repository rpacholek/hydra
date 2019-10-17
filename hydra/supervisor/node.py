from ..core.node.base_node import Node
from ..core.action.executor import action_executor


class SupervisorNode(Node):
    def __init__(self, device, action_queue, config=None, env=None):
        super().__init__(device, action_queue, config, env)

    # Action executor
    @action_executor("job.(result|status)")
    def job_result(self, action):
        self.send(action)

    @action_executor("event.node")
    def event_handler(self, action):

        # Propagate
        self.send(action)
