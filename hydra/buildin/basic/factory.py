from .scheduler import BasicScheduler, Scheduler
from .action_queue import BasicActionQueue, ActionQueue
from hydra.core.factory.register_class import SubFactory

class BasicSchedulerFactory(SubFactory, generate=Scheduler):
    def __init__(self, config):
        super().__init__(config)
        self.config = config

    @staticmethod
    def get_name() -> str:
        return "Basic"

    def create(self, *args, **kwargs):
        return BasicScheduler(*args, config=self.config, **kwargs)

class BasicActionQueueFactory(SubFactory, generate=ActionQueue):
    def __init__(self, config):
        super().__init__(config)
        self.config = config

    @staticmethod
    def get_name() -> str:
        return "Basic"

    def create(self, *args, **kwargs):
        return BasicActionQueue(*args, config=self.config, **kwargs)


