from hydra.core.task.task import Task
from hydra.core.task.taskdb import TaskContainer

class InMemoryTask(Task):
    def __init__(self, definition, files=[], version=0, **kwargs):
        super().__init__(definition, files, version, **kwargs)
        self.definition = None

    def __store(self, definition):
        self.definition = definition

    def __load(self):
        return self.definition

class InMemoryTaskContainer(TaskContainer):
    def __init__(self, action_queue, **kwargs):
        super().__init__(action_queue, **kwargs)
        self.database = {}

    def find_task(self, taskid):
        return self.database.get(taskid)

    def add_task(self, task):
        self.database[task.id] = task

    def delete_task(self, taskid):
        if taskid in self.database:
            del self.database[taskid]

    def create_task(self, *args, **kwargs):
        return InMemoryTask(*args, **kwargs)

