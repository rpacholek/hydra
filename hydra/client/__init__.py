
import asyncio
from hydra.core.common.coro import NoneCoroManager
from hydra.core.factory import get_factory
from hydra.core.node.main import Main
from hydra.core.config import get_default_config
from hydra.supervisor.manager import SupervisorManager
from hydra.core.common.coro import NoneCoroManager
from ..core.environment import LocalEnvironment, NodeType
from .repl import REPL


class Client(Main):
    def __init__(self, config, coromanager=NoneCoroManager()):
        super().__init__(config, coromanager)

        self.environment = LocalEnvironment(config, NodeType.Client)
        self.supervisor_manager = SupervisorManager(
            self.action_queue, config=config, env=self.environment)

        self.async_objects = [
            (self.supervisor_manager.connect, "SupervisorConnect"),
            (self.action_queue.run, "Queue")
        ]

    async def run(self):
        self.repl = REPL(self.action_queue, self.config)
        await self.repl.run()

    @staticmethod
    def get_default_config():
        return get_default_config(__file__)
