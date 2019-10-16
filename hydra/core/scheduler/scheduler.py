from abc import ABCMeta, abstractmethod

from ..action.executor import ActionExecutor

class Scheduler(ActionExecutor, metaclass=ABCMeta):
    def __init__(self, action_queue, config=None):
        ActionExecutor.__init__(self)
        
        self.action_queue = action_queue

    @abstractmethod
    async def run(self, coromanager=None):
        pass

