from abc import ABCMeta, abstractmethod

class Serializable(metaclass=ABCMeta):
    @abstractmethod
    def dump(self):
        # Expect to return standard type: dict, list, int, str, ...
        return None

    @abstractmethod
    def load(self, data):
        pass

def get_serializer():
    import yaml

    return yaml
