from ..factory.register_class import Factory

from .task import Task
from .taskdb import TaskContainer
from .job import Job
from .jobdb import JobContainer


class TaskFactory(Factory, generate=Task):
    registered_subfactories = {}

    def __init__(self, config):
        super().__init__(config)
        self.config = config.get("task")
        self.basefactory = self.choose_factory()(self.config)

    @staticmethod
    def add_subfactory(subfactory):
        name = subfactory.get_name()
        TaskFactory.registered_subfactories[name] = subfactory

    @staticmethod
    def get_subfactories():
        return list(TaskFactory.registered_subfactories.keys())


class TaskDBFactory(Factory, generate=TaskContainer):
    registered_subfactories = {}

    def __init__(self, config):
        super().__init__(config)
        self.config = config.get("task")
        self.basefactory = self.choose_factory()(self.config)

    @staticmethod
    def add_subfactory(subfactory):
        name = subfactory.get_name()
        TaskDBFactory.registered_subfactories[name] = subfactory

    @staticmethod
    def get_subfactories():
        return list(TaskDBFactory.registered_subfactories.keys())


class JobFactory(Factory, generate=Job):
    registered_subfactories = {}

    def __init__(self, config):
        super().__init__(config)
        self.config = self.config.get("job")
        self.basefactory = choose_factory()(self.config)

    @staticmethod
    def add_subfactory(subfactory):
        name = subfactory.get_name()
        JobFactory.registered_subfactories[name] = subfactory

    @staticmethod
    def get_subfactories():
        return list(JobFactory.registered_subfactories.keys())


class JobDBFactory(Factory, generate=JobContainer):
    registered_subfactories = {}

    def __init__(self, config):
        super().__init__(config)
        self.config = config.get("job")
        self.basefactory = self.choose_factory()(self.config)

    @staticmethod
    def add_subfactory(subfactory):
        name = subfactory.get_name()
        JobDBFactory.registered_subfactories[name] = subfactory

    @staticmethod
    def get_subfactories():
        return list(JobDBFactory.registered_subfactories.keys())
