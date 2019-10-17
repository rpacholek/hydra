from ..factory.register_class import Factory
from .queue import ActionQueue


class ActionQueueFactory(Factory, generate=ActionQueue):
    registered_subfactories = {}

    def __init__(self, config):
        super().__init__(config)
        self.config = config.get("action_queue")
        self.basefactory = self.choose_factory()(self.config)

    @staticmethod
    def add_subfactory(subfactory):
        name = subfactory.get_name()
        ActionQueueFactory.registered_subfactories[name] = subfactory

    @staticmethod
    def get_subfactories():
        return list(ActionQueueFactory.registered_subfactories.keys())
