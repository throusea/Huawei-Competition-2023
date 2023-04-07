from item import Item
from enum import Enum
from workbench import Workbench

class RobotState(Enum):
    IDLE = -1
    TAKING = 0  # the state to take the item
    DELIVERING = 1 # the state to sell the item

class Robot():
    def __init__(self,id: int,  pos: tuple, vel: float=0, rot: float=0, w: float=0, loadingItem: int=-1, state: RobotState=RobotState.IDLE):
        self.id = id #id
        self.pos = pos # position
        self.vel = vel # velocity
        self.rot = rot # rotation
        self.w = w     # angle velocity
        self.state = state
        self.itemId = loadingItem
        self.loadingTask = None
        self.last_w = None

    def __str__(self):
        return ("id:%s, pos:(%s, %s), vel:%s, rot:%s, w:%s, state:%s, loadingItem:%s, loadingTask:%s, last_w:%s"%(self.id, self.pos[0], self.pos[1], self.vel, self.rot, self.w, self.state, self.itemId, self.loadingTask, self.last_w))
    
    def set_task(self, e):
        # e.set_cmd(self)
        self.loadingTask = e

