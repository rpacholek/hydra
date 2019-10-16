from .register_class import get_factory_registery

def get_factory(ftype, config=None):
    factory_registery = get_factory_registery()
    if ftype in factory_registery:
        if config:
            return factory_registery[ftype](config)
        else:
            return factory_registery[ftype]
    raise Exception(f"Factory for type '{ftype.__name__}' not registered") 

def check_available_factories():
    factory_registery = get_factory_registery()
    return {key.__name__: value.get_subfactories() and list(value.get_subfactories()) for key, value in factory_registery.items()} 
