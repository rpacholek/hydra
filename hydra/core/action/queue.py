from abc import ABCMeta, abstractmethod
from .action import Action

class ActionQueue(metaclass=ABCMeta):
    """
    Implementation of this class should take care of execution of the Actions.
    """
    @abstractmethod
    def push_action(self, action: Action):
        pass


