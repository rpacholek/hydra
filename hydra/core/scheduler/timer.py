from sortedcontainers import SortedList
from croniter import croniter

"""
The timer does not support one time cancelation. 
The timer does notifies the task and it should decide if the task should be performed or ignored.
"""


class Timer(ActionExecutor):
    def __init__(self, action_queue):
        ActionExecutor.__init__(self)

        self.time_queue = SortedList(key=lambda t, sid: t)
        self.task_set = dict()
        self.action_queue = action_queue
        self.action_queue.register(self)

    def register(self, taskid, schedule: List[str]):
        self.task_set[taskid] = [croniter(sched) for sched in schedule]
        self.schedule_next(taskid)

    def launch(self, taskid):
        # self.action_queue.append()
        self.schedule_next(taskid)

    def schedule_next(self, taskid):
        nearest_time = min([c.get_next() for c in self.task_set[taskid]])
        self.time_queue.add((nearest_time, taskid))

    async def run():
        while True:
            if self.time_queue[0] < time.time():
                t, tid = self.time_queue.pop(0)
                self.launch(tid)
            else:
                # Check every minute if there is anything to launch
                asyncio.sleep(60)

    def get_accepted_action_list(self):
        return ["timer.schedule"]

    def exec_action(self, action):
        pass
