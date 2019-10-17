from enum import Enum


class EnvVisibility(Enum):
    Private = 0  # Does not share with anyone - internal use only
    # Might share with trusted nodes (supervisor or admin client)
    Protected = 1
    Public = 2  # Might share this information with all nodes
