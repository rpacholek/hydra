import enum

class NodeType(enum.Enum):
    Supervisor = "supervisor"
    Worker = "worker"
    Client = "client"

    Undefined = "undefined"

    def into_type(name):
        return { t.value: t for t in NodeType }.get(name, NodeType.Undefined)

class Environment:
    """
    Protocol in use and available
    Name

    Information from basic module will be passed every time.
    Other information is abailable throught a plugin.
    """

    def __init__(self):
        self.node_type = NodeType.Undefined
        self.static_env = {}
        self.dynamic_env = {}

    class EnvValue:
        def __init__(self, value):
            self.value = value
        def __call__(self):
            return self.value

    def set_denv(self, path, handler):
        pass

    def set_senv(self, path, value):
        pass

    def get(self, path):
        pass

    def get_node_type(self):
        return self.node_type

    def set_node_type(self, value):
        self.node_type = value

class LocalEnvironment(Environment):
    """
    Local node environment
    """
    def __init__(self, config, node_type=NodeType.Undefined):
        super().__init__()
        self.node_type = node_type

class RemoteEnvironment(Environment):
    """
    Remote node environment - data gathered from exchange protocol
    """
    pass

