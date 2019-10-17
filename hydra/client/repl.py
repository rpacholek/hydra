import asyncio

from ..core.common.io import input
from .action_creator import ActionCreator


class REPL:
    def __init__(self, action_queue, config, *args, **kwargs):
        self.action_queue = action_queue
        self.config = config

    async def run(self):
        await asyncio.sleep(1)
        print("Insert command: ")
        action_creator = ActionCreator()
        while True:
            input_data = await input("~> ")
            action = action_creator.parse(*input_data.split())
            if action:
                self.action_queue.push_action(action)
