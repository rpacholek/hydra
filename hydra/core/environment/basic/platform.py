

class System:

    def get_system_type():
        return "type", platform.system(), Public

    def get_system_version():
        systype = platform.system()
        version = "Unknown"
        if systype == "Linux":
            pass
        elif systype == "Windows":
            pass
        return "version", version, Public
