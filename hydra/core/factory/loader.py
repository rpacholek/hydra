import os.path
import importlib


def install_modules(dirs=[]):
    for dirpath in dirs:
        modules = recursive_file_search(dirpath, "factory.py")
        for module in modules:
            importlib.import_module(module)


def recursive_file_search(path, filename):
    paths = []
    contains_init = False
    with os.scandir(path) as it:
        for entry in it:
            if entry.name.startswith("."):
                # Skip hidden files
                continue
            if entry.is_file() and entry.name == filename:
                filename, extension = filename.rsplit(".", 1)
                paths.append(filename)
            elif entry.is_file() and entry.name == "__init__.py":
                contains_init = True
                continue
            elif entry.is_dir():
                paths += [f"{entry.name}.{p}" for p in recursive_file_search(
                    entry.path, filename)]
    return paths


def get_this():
    import hydra
    return hydra.__file__.rsplit("/", 2)[0]
