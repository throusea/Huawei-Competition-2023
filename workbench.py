from item import Item
from enum import Enum

# The disable workbench set if the workbench is disabled
NEXT_WORKBENCH = [
    0,
    0b110000,
    0b1010000,
    0b1100000,
    0b10000000,
    0b10000000,
    0b10000000
]

# class WorkbenchState(Enum):
#     IDLEPRODUCING = 0
#     LOCKING = 1
#     FINISHED = 2
#     DISABLE = 3

class Workbench:
    def __init__(self, id:int, ty: int, pos:tuple, status: int=-1, inputs: int=0, output: int=0):
        self.id = id
        self.ty = ty
        self.status = status
        self.inputs = inputs
        self.output = output # 0 is none and 1 is ok
        self.pos = pos  # position (from transform)

    def __str__(self):
        return ("id:%s, ty:%s, pos:(%s, %s), status:%d, inputs: %s, output:%s"%(self.id, self.ty, self.pos[0], self.pos[1], self.status, self.inputs, self.output))
