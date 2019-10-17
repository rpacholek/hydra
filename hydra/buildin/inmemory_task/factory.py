from hydra.core.factory.register_class import SubFactory
from hydra.core import *

from .task import InMemoryTask, InMemoryTaskContainer
from .job import InMemoryJob, InMemoryJobContainer


class InMemoryTaskFactory(SubFactory, generate=Task):
    registered_subfactories = {}

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.baseclass = InMemoryTask

    @staticmethod
    def get_name():
        return "InMemory"

    def create(self, *args, **kwargs):
        self.baseclass(*args, config=self.config, **kwargs)


class InMemoryTaskContainerFactory(SubFactory, generate=TaskContainer):
    registered_subfactories = {}

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.baseclass = InMemoryTaskContainer

    @staticmethod
    def get_name():
        return "InMemory"

    def create(self, *args, **kwargs):
        self.baseclass(*args, config=self.config, **kwargs)


class InMemoryJobFactory(SubFactory, generate=Job):
    registered_subfactories = {}

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.baseclass = InMemoryJob

    @staticmethod
    def get_name():
        return "InMemory"

    def create(self, *args, **kwargs):
        self.baseclass(*args, config=self.config, **kwargs)


class InMemoryJobContainerFactory(SubFactory, generate=JobContainer):
    registered_subfactories = {}

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.baseclass = InMemoryJobContainer

    @staticmethod
    def get_name():
        return "InMemory"

    def create(self, *args, **kwargs):
        self.baseclass(*args, config=self.config, **kwargs)
