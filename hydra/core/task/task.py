from abc import ABCMeta, abstractmethod
import uuid

class Task(metaclass=ABCMeta):
    """
    This class is ment to contain the definition of what the task is doing.
    An instance of this in context of the system is a job.
    """
    purposes = {
            "trigger": ["header", "trigger"],
            "job": ["header", "task", "job", "scheduler", "worker"]
            }

    def __init__(self, definition, files=[], version=0, **kwargs):
        self.version = version
        self.id = self.__generate_id() 
        self.valid = False
        if self.__validate(definition):
            self.__store(definition)
            self.valid = True
        else:
            pass
            ## Log failure

    def is_correct(self) -> bool:
        return self.valid
    
    def create_job(self):
        return Job(self)

    def get_sub_def(self, purpose):
        assert purpose in Task.purposes
        definition = self.__load()
        return { k:v for k,v in definition.items() if k in Task.purposes[purpose]} 

    def get_trigger_def(self):
        return self.get_sub_def("trigger")

    def get_job_def(self):
        return self.get_sub_def("job")
    
    def __validate(self, definition) -> bool:
        return "header" in definition
    
    @staticmethod
    def __generate_id():
        return f"task-{str(uuid.uuid1())[:18]}"

    def get_short_id():
        return self.id[5:11]

    ## Iterface
    @abstractmethod
    def __store(self, definition):
        pass

    @abstractmethod
    def __load(self):
        pass



