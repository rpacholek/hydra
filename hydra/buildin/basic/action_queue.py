import asyncio
import logging
from collections import defaultdict

from ...core.action.executor import ActionExecutor, action_executor
from ...core.action.queue import ActionQueue


class BasicActionQueue(ActionExecutor, ActionQueue):
    def __init__(self, config):
        ActionExecutor.__init__(self)

        self.config = config
        self.queue = asyncio.Queue()
        self.executors = defaultdict(list)

        self.register(self)

    async def run(self, coromanager=None):
        while True:
            action = await self.get_action()
            logging.debug(f"Queue len: {self.queue.qsize()}")
            self.execute(action)

    def execute(self, action):
        executors = self.get_executors(action.action_type)
        for executor in executors:
            executor.exec_action(action)
        if not executors:
            logging.debug(f"No executor for action {action.get_type()}")
            logging.debug(
                f"Existing executors: {', '.join(self.executors.keys())}")

    def get_executors(self, action_type):
        # TODO: hierarchical resolve
        action_type = f"{action_type}."
        while "." in action_type:
            action_type, _ = action_type.rsplit(".", 1)
            if action_type in self.executors:
                return self.executors[action_type]
        return []

    # Executor register
    def register(self, executor):
        for accepted_action in executor.get_accepted_actions():
            self.executors[accepted_action].append(executor)

    # Queue methods
    def push_action(self, action):
        self.queue.put_nowait(action)
        logging.debug(f"Added - queue len: {self.queue.qsize()}")

    async def get_action(self):
        return await self.queue.get()

    # ActionExecutor
    @action_executor("config.action")
    def action_config_change(self, action):
        """
        config.action - change in queue policy
        """
        # TODO
        pass
