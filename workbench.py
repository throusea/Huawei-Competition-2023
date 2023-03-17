from item import Item
from enum import Enum

DISABLE_WORKBWNCH = [
    [],
    [4,5],
    [4,6],
    [5,6],
    [7],
    [7],
    [7]
]

class WorkbenchState(Enum):
    IDLEPRODUCING = 0
    LOCKING = 1
    FINISHED = 2
    DISABLE = 3

class Workbench:
    def __init__(self, id:int, pos:tuple, status: int = -1, inputs: list=[], outputs: list=[], container: WorkbenchState = WorkbenchState.EMPTY):
        self.id = id
        self.status = status
        self.inputs = inputs
        self.outputs = outputs
        self.container = container
        self.pos = pos  # position (from transform)