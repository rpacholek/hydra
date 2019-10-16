from abc import ABCMeta, abstractmethod

from ..action.executor import ActionExecutor, action_executor

class TaskContainer(ActionExecutor, metaclass=ABCMeta):
    def __init__(self, action_queue, **kwargs):
        ActionExecutor.__init__(self)

        self.action_queue = action_queue

        self.action_queue.register(self)

    @abstractmethod
    def create_task(self, definition, files=[], version=0):
        pass

    @abstractmethod
    def find_task(self, taskid):
        pass

    @abstractmethod
    def add_task(self, task):
        pass

    @abstractmethod
    def delete_task(self, taskid):
        pass
    
