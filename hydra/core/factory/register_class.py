from abc import ABCMeta, abstractmethod
from collections import defaultdict

factory_registery = {}
awaiting_registery = defaultdict(list)


def get_factory_registery():
    for key in list(awaiting_registery.keys()):
        if key in factory_registery:
            for awaitcls in awaiting_registery[key]:
                factory_registery[key].add_subfactory(awaitcls)
            del awaiting_registery[key]
    return factory_registery


class Factory(metaclass=ABCMeta):
    def __init_subclass__(cls, *args, generate=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if generate:
            factory_registery[generate] = cls
        else:
            pass
        # TODO: log.error("Unknown type factory")

    def __init__(self, config):
        self.basefactory = None

    def choose_factory(self):
        if not self.config:
            raise Exception("Config in factory not set")
        name = self.config.get("type", "__type_not_set__")
        if name in self.registered_subfactories:
            return self.registered_subfactories[name]
        else:
            raise Exception(f"TaskFactory could not find {name} subfactory")

    def create(self, *args, **kwargs):
        if self.basefactory:
            return self.basefactory.create(*args, **kwargs)
        raise Exception("Factory not set")

    @staticmethod
    @abstractmethod
    def get_subfactories():
        pass

    @staticmethod
    def add_subfactory(subfactory):
        pass
        # TODO: log.error("NotImplemented")


class SubFactory(metaclass=ABCMeta):
    def __init_subclass__(cls, *, generate=None, **kwargs):
        super().__init_subclass__(**kwargs)
        if generate:
            if generate in factory_registery:
                factory_registery[generate].add_subfactory(cls)
            else:
                awaiting_registery[generate].append(cls)

    def __init__(self, config):
        pass

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass
