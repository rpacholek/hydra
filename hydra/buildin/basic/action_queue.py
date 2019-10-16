import asyncio
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
    
    async def run(self):
        while True:
            action = await self.get_action()
            self.execute(action)
    
    def execute(self, action):
        for executor in self.get_executors(action.action_type):
            executor.exec_action(action)

    def get_executors(self, action_type):
        # TODO: hierarchical resolve
        return self.executors.get(action_type, [])

    ### Executor register
    def register(self, executor):
        for accepted_action in executor.get_accepted_actions():
            self.executors[accepted_action].append(executor)

    ### Queue methods
    def push_action(self, action):
        self.queue.put_nowait(action)

    async def get_action(self):
        return await self.queue.get()

    ### ActionExecutor
    @action_executor("config.action")
    def action_config_change(self, action):
        """
        config.action - change in queue policy
        """
        #TODO
        pass

