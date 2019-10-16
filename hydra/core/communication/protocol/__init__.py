from .base import *
from .steps.auth import AuthenticationProtocol
from .steps.init import InitProtocol

class AdvancedProtocol(Protocol):
    def __init__(self, info, local_env, remote_env, config):
        Protocol.__init__(self, info, local_env, remote_env, config)
        self.steps = [
            InitProtocol,
            AuthenticationProtocol,
            #ExchangeProtocol,
            #NegotiateProtocol    
        ]

