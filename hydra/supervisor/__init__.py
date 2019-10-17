import asyncio

from ..core.common.coro import NoneCoroManager
from ..core.node.main import Main
from ..core import *
from ..core.config import get_default_config
from ..core.environment import LocalEnvironment, NodeType
from ..worker.manager import WorkerManager
from ..client.manager import ClientManager


class Supervisor(Main):
    def __init__(self, config, coromanager=NoneCoroManager()):
        super().__init__(config, coromanager)

        self.environment = LocalEnvironment(config, NodeType.Supervisor)

        self.task_container = get_factory(
            TaskContainer, config).create(self.action_queue)
        self.job_container = get_factory(JobContainer, config).create(
            self.action_queue, self.task_container)
        self.scheduler = get_factory(
            Scheduler, config).create(self.action_queue)

        self.worker_manager = WorkerManager(
            self.action_queue, config=config, env=self.environment)
        # TODO: Pass wrapper for action_queue - check permission for action
        self.client_manager = ClientManager(
            self.action_queue, config=config, env=self.environment)

        self.async_objects = [
            (self.scheduler.run, "Scheduler"),
            (self.worker_manager.server, "WorkerListener"),
            (self.client_manager.server, "ClientListener")
        ]

    @staticmethod
    def get_default_config():
        return get_default_config(__file__)
