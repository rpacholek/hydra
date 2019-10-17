from ..core.node.base_node import Node
from ..core.action.executor import action_executor


class WorkerNode(Node):
    def __init__(self, device, action_queue, config=None, env=None):
        super().__init__(device, action_queue, config, env)

    # Action executor
    @action_executor("job.run")
    def job_executor(self, action):
        # Assume the destination is correct
        self.send(action)

    @action_executor("maintenance")
    def maintenance_executor(self, action):
        pass
