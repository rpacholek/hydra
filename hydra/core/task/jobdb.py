from abc import ABCMeta, abstractmethod
from typing import Type

from .job import Job
from ..action.executor import ActionExecutor, action_executor

class JobContainer(ActionExecutor, metaclass=ABCMeta):
    def __init__(self, action_queue, taskdb, **kwargs):
        ActionExecutor.__init__(self)
        
        self.action_queue = action_queue
        self.taskdb = taskdb

    def create_job(self, taskid: str):
        job = self.taskdb.find_job(taskid).create_job()
        self.store_job(job)

    ## Interface
    @abstractmethod
    def store_job(self, job: Type[Job]):
        pass

    @abstractmethod
    def find_job(self, jobid: str) -> Job:
        pass
    
    @abstractmethod
    def remove_job(self, jobid: str):
        pass

    @action_executor("job.result")
    def job_result(self, action):
        pass
