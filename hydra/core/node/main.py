import asyncio
from abc import ABCMeta, abstractmethod

from hydra.core.common.coro import NoneCoroManager
from hydra.core import *


class Main(metaclass=ABCMeta):
    def __init__(self, config, coromanager=NoneCoroManager()):
        self.config = config
        self.log = None

        self.action_queue = get_factory(ActionQueue, config).create()
        self.coromanager = coromanager

        self.async_objects = []

    @abstractmethod
    def get_default_config():
        pass

    # TODO: Better name
    async def start_coro(self):
        for async_func, name in self.async_objects:
            print(f"Run {name} {async_func}")
            coro = asyncio.create_task(
                async_func(coromanager=self.coromanager))
            self.coromanager.register(coro, name)

    async def run(self):
        await self.action_queue.run()
