from item import Item, ITEM_INPUT
from enum import Enum
import myutil

# The disable workbench set if the workbench is disabled
NEXT_WORKBENCH = [
    0,
    0b110000,
    0b1010000,
    0b1100000,
    0b10000000,
    0b10000000,
    0b10000000,
    0,
    0,
    0
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
        self.lockset = 0 # binary set, i-th bit means the i-th item
        self.locktime_dict = [-1] * 10

    def setLock(self, item_id: int, frame: int=0, val: bool=True):
        if myutil.is_in_set(item_id, self.lockset) ^ val == 0:
            # raise Exception("The lock error!")
            return 
        self.lockset ^= 1<<item_id
        if val == True:
            self.locktime_dict[item_id] = frame
        else:
            self.locktime_dict[item_id] = -1
    
    def isLock(self, item_id: int):
        return myutil.is_in_set(item_id, self.lockset)
    
    def getLockTime(self, item_id: int):
        if self.locktime_dict[item_id] == -1:
            # raise Exception(item_id)
            return -1
        return self.locktime_dict[item_id]

    def num_in_inputset(self):
        inputs = ITEM_INPUT[self.ty]
        s = self.inputs & inputs
        no = 0
        for i in range(s.bit_length()):
            if (s & (1<<i)) != 0:
                no += 1
        return no

    def __str__(self):
        return ("id:%s, ty:%s, pos:(%s, %s), lockset: %d, status:%d, inputs: %s, output:%s"%(self.id, self.ty, self.pos[0], self.pos[1], self.lockset, self.status, self.inputs, self.output))
