from typing import List

from .action import Action
from .helper import action_cmp
"""
Actions are hierarchical.
E.g. event.node, event.queue
"""


def action_executor(action_pattern, *patterns):
    def decorator(func):
        if type(action_pattern) == str:
            func.__dict__["action_pattern"] = action_pattern
            for pattern in patterns:
                func.__dict__["action_pattern"] = pattern
        elif type(action_pattern) == list:
            for pattern in action_pattern:
                func.__dict__["action_pattern"] = pattern

        return func
    return lambda func: decorator(func)


def executor_forwarder(cls):
    patterns = []
    for name in dir(cls):
        item = getattr(cls, name)
        if callable(item) and type(item).__name__ == "function":
            if "action_pattern" in item.__dict__:
                patterns.append(item.__dict__["action_pattern"])
    return patterns


class ActionExecutor:
    def __init__(self, *args, debug=False, **kwargs):
        self.action_executors = {}

        for name in dir(self):
            item = self.__getattribute__(name)
            if callable(item) and type(item).__name__ == "method":
                # TODO: not catching @classmethod
                # Its not a static function
                if "action_pattern" in item.__func__.__dict__:
                    # Function registered using decorator
                    pattern = item.__func__.__dict__["action_pattern"]
                    self.register_action_pattern(pattern, item)

    def register_action_pattern(self, pattern, function):
        self.action_executors[pattern] = function

    def get_accepted_actions(self) -> List[str]:
        return list(self.action_executors.keys())

    def exec_action(self, action: Action):
        action_type = action.get_type()
        for pattern, func in self.action_executors.items():
            if action_cmp(action_type, pattern):
                func(action)
