from ..core.node.manager import NodeManager


class ClientManager(NodeManager):
    def __init__(self, action_queue, config=None, env=None):
        super().__init__(action_queue, config.get("client"), env)
