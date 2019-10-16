from abc import ABCMeta, abstractmethod

class CoroManager(metaclass=ABCMeta):
    @abstractmethod
    def register(coro, name):
        pass

class NoneCoroManager(CoroManager):
    def register(self, coro, name):
        pass

# TODO: Full implementation of CoroManager
