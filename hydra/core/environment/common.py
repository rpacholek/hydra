from enum import Enum

class EnvVisibility(Enum):
    Private = 0 # Does not share with anyone - internal use only
    Protected = 1 # Might share with trusted nodes (supervisor or admin client)
    Public = 2 # Might share this information with all nodes

