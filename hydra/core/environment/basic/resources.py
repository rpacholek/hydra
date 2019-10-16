import platform

from ..common.EnvVisibility import *

class CPUResource:
    def get_name():
        return "CPU"

    @resource
    def get_architecture():
        return "architecture", platform.machine(), Public

    @resource
    def get_processor_type():
        return "type", platform.processor(), Protected

    @resource
    def get_cores():
        return "core_number", multiprocessing.cpu_count(), Public

class MemoryResource:
    def get_name():
        return "memory"

    @resource
    def get_memory_size():
        #TODO
        return "total_memory", 0, Public

    """
    @dynamic_resouce
    def get_available_memory():
        return "available_memory", 0, Protected
    """

