class Job:
    def __init__(self, task_definition, **kwargs):
        self.taskdef = task_definition
        self.result = []
        self.id = self.__generate_id(task_definition)

    def set_result(self, result):
        self.result.append(result)

    def create_action(self):
        return Action("job.exec")

    def __generate_id(td):
        return f"job-{td.get_short_id()}-{str(uuid.uuid1())[:6]}"
