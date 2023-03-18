from item import Item
from enum import Enum

# The disable workbench set if the workbench is disabled
NEXT_WORKBENCH = [
    0,
    110000,
    1010000,
    1100000,
    10000000,
    10000000,
    10000000
]

# class WorkbenchState(Enum):
#     IDLEPRODUCING = 0
#     LOCKING = 1
#     FINISHED = 2
#     DISABLE = 3

class Workbench:
    def __init__(self, id:int, ty: int, pos:tuple, status: int=-1, disable: bool=False, inputs: int=0, output: int=0):
        self.id = id
        self.ty = ty
        self.status = status
        self.inputs = inputs
        self.output = output # 0 is none and 1 is ok
        self.pos = pos  # position (from transform)