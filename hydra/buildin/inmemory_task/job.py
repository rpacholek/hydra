from hydra.core.task.job import Job
from hydra.core.task.jobdb import JobContainer


class InMemoryJob(Job):
    def __init__(self, task_definition, **kwargs):
        super().__init__(task_definition, **kwargs)


class InMemoryJobContainer(JobContainer):
    def __init__(self, action_queue, taskdb, **kwargs):
        super().__init__(action_queue, taskdb, **kwargs)
        self.db = {}

    def store_job(job):
        self.db[job.id] = job

    def find_job(jobid):
        return self.db.get(jobid, None)

    def remove_job(jobid):
        if jobid in self.db:
            del self.db[jobid]
