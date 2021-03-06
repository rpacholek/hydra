from ..core.action.action import Action


def options_error(category):
    def _er(*args):
        print(f"Commend not found: {category} - {args}")
        return None
    return _er


def options(var, category="help", *args):
    func = var.get(category, options_error(category))
    return func(*args)


class ActionCreator:
    def __init__(self):
        self._root = {
            "task": self.task,
            "help": lambda *_: self.help(self._root),
        }

        self._task = {
            "create": self.task_create,
            "run": self.task_run,
            "help": lambda *_: self.help(self._task),
        }

    def parse(self, *args):
        return options(self._root, *args)

    def help(self, what):
        print(f"Available commands: {', '.join(what.keys())}")

    def task(self, *args):
        return options(self._task, *args)

    def task_create(self, name, *command):
        return Action(
            action_type="task.create",
            content={
                "name": name,
                "type": "exec",
                "exec": command
            }
        )

    def task_run(self, name, *args):
        return Action(
            action_type="task.run",
            content={
                "name": name,
            })
