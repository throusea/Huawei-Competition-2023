from item import Item
from enum import Enum
class WorkbenchState(Enum):
    EMPTY = 0
    FULL = 1

class Workbench:
    def __init__(self, id:int, pos:tuple, status: int = -1, inputs: list=[], outputs: list=[], container: WorkbenchState = WorkbenchState.EMPTY):
        self.id = id
        self.status = status
        self.inputs = inputs
        self.outputs = outputs
        self.container = container
        self.pos = pos  # position (from transform)