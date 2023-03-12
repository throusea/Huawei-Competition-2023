from item import Item
from enum import Enum

class WorkbenchState(Enum):
    IDLEPRODUCING = 0
    LOCKING = 1
    FINISHED = 2

class Workbench:
    def __init__(self, id:int, pos:tuple, status: WorkbenchState=WorkbenchState.IDLEPRODUCING, inputs: list=[], outputs: list=[]):
        self.id = id
        self.status = status
        self.inputs = inputs
        self.outputs = outputs
        self.pos = pos  # position (from transform)