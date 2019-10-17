from typing import List

from .action import Action
"""
Actions are hierarchical.
E.g. event.node, event.queue
"""


def action_executor(action_pattern):
    def decorator(func):
        func.__dict__["action_pattern"] = action_pattern
        return func
    return lambda func: decorator(func)


class ActionExecutor():
    def __init__(self, *args, **kwargs):
        self.action_executors = {}

        for name in dir(self):
            item = self.__getattribute__(name)
            if callable(item) and type(item).__name__ == "method":
                # TODO: not catching @classmethod
                # Its not a static function
                if "action_pattern" in item.__func__.__dict__:
                    # Function registered using decorator
                    self.action_executors[item.__func__.__dict__[
                        "action_pattern"]] = item

    def get_accepted_actions(self) -> List[str]:
        return list(self.action_executors.keys())

    def exec_action(self, action: Action):
        action_type = action.get_type()
        for pattern, func in self.action_executors.items():
            if action_cmp(action_type, pattern):
                func(action)
