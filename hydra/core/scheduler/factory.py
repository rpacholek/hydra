from ..factory.register_class import Factory
from .scheduler import Scheduler

class SchedulerFactory(Factory, generate=Scheduler):
    registered_subfactories = {}

    def __init__(self, config):
        super().__init__(config)
        self.config = config.get("scheduler")
        self.basefactory = self.choose_factory()(self.config)

    @staticmethod
    def add_subfactory(subfactory):
        name = subfactory.get_name()
        SchedulerFactory.registered_subfactories[name] = subfactory

    @staticmethod
    def get_subfactories():
        return list(SchedulerFactory.registered_subfactories.keys())

