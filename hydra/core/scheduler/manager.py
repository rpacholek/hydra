
# TODO: Use scheduler node
# TODO: Use scheduler factory for default scheduler

class SchedulerManager(ActionExecutor, ActionQueueInterface):
    def __init__(self, action_queue, config=None):
        ActionExecutor.__init__(self)

        self.default_scheduler = DefaultScheduler(self)
        self.action_queue = action_queue
        self.action_queue.register(self)
    
    ### Action Queue Interface
    def push_action(self, action: Action):
        self.action_queue.push_action(action)

    @property
    def active_queue(self):
        return self.default_scheduler

    ###
    def get_accepted_action_list(self):
        return self.active_queue.get_accepted_action_list()

    def exec_action(self, action):
        self.active_queue.exec_action(action)


