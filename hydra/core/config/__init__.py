import os
from collections import ChainMap

from ..common.serializer import get_serializer

def get_default_config(path):
    return os.path.join(os.path.dirname(path), "default.yaml")

class Config:
    def __init__(self, Type, config_file=""):
        self.serializer = get_serializer()
        self.config_file = config_file

        self.default = self.read_config_file(Type.get_default_config())
        self.user_config = self.read_config_file(config_file)
        
        self.config = ChainMap(self.user_config, self.default)
            

    def read_config_file(self, config_file):
        if config_file and os.path.exists(config_file):
            with open(config_file) as f:
                return self.serializer.load(f.read())
        else:
            return {}

    def get(self, args, default=None):
        conf = self.config
        for arg in args.split("."):
            if isinstance(conf, ChainMap) and arg in conf:
                conf = conf[arg]
            else:
                return default
        return conf

    def shadow(self, arg):
        return ShadowConfig(self, arg)

    def config_listener(self, notify_func, *keys):
        pass

class ShadowConfig:
    # TODO: Expand
    # Insted of config.get("manager") => config.shadow("manager")
    def __init__(self, config, path):
        self.config = config
        self.path = path

    def get(self, args, default=None):
        return self.config(f"{path}.args", default)

    def __get__(self, arg):
        return self.config[arg]

def shadow_copy(config, requires=[], allowed=[]):
    fields_not_found = []
    for requirement in requires:
        if requirement not in config:
            fields_not_found.append(requirement)
    if fields_not_found:
        raise Exception(f"Required fields: {fields_not_found} not in config")
    return {k: config[k] for k in requires + allowed if k in config}


