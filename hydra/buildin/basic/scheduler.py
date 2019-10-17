import asyncio
from sortedcontainers import SortedList
from enum import Enum
from collections import defaultdict

from hydra.core import *

"""
Default Scheduler

Supports:
    - run on specific label (only one!)
    - labels are string based and the label must match exactly
"""


class BasicScheduler(Scheduler):
    def __init__(self, action_queue, config=None):
        Scheduler.__init__(self, action_queue, config)
        self.scheduler_queue = asyncio.Queue()

        # TODO: Probably should not directly access action_queue
        self.action_queue = action_queue
        self.device_manager = SchedulerDeviceManager()

        self.schedule_items = {}

        self.trigger_queue = defaultdict(list)

    async def run(self, coromanager=None):
        while True:
            item = await self.scheduler_queue.get()

    def check_label(self, sid):
        pass

    def launch(self, sid):
        schedule_item = self.schedule_items[sid]

    # ActionExecutor
    @action_executor("schedule")
    def schedule_action(self, action):
        self.scheduler_queue.put_nowait(action)

    @action_executor("event")
    def event_action(self, action):
        self.scheduler_queue.put_nowait(action)


class SchedulerStatus(Enum):
    Available = 1
    Busy = 2
    Dead = 10


class SchedulerDevice:
    def __init__(self, device_id, labels=[]):
        self.status = SchedulerStatus.Available
        self.device_id = device_id
        self.labels = labels + [None]

    def get_labels(self):
        return self.labels

    def is_available(self):
        return self.status == SchedulerStatus.Available

    def set_status(self, status):
        self.status = status

    def get_id(self):
        return device_id


class SchedulerDeviceManager:
    def __init__(self):
        self.devices = {}
        self.labels = defaultdict(set)

    def register(self, device):
        self.device[device.get_id()] = device
        for label in device.get_labels():
            self.labels[label].add(device.get_id())

    def remove(self, device_id):
        device = self.devices.pop(device_id)
        for label in device.get_labels():
            self.labels[label].discard(device.get_id())

    def get_free_machine(self, label):
        for device in self.devices[label]:
            if device.is_available():
                return device
        return None


class SchedulerItem:
    def __init__(self):
        pass

    def get_time(self):
        return None

    def get_labels(self):
        return None
