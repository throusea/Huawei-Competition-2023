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
        # self.acc = acc # accelerate
        self.rot = rot # rotation
        self.w = w     # angle velocity
        self.state = state
        self.loadingItem = loadingItem
        self.loadingTask = None
        self.state = RobotState.IDLE
    
    def set_task(self, e):
        # e.set_cmd(self)
        self.loadingTask = e


# You can define some global value such as maximun force or maximun velocity

class RobotMod:
    def __init__(pMaxVel: float, pMaxAcc: float, pMaxW: float):
        self.pMaxVel = pMaxVel # predicted maximum velocity
        self.pMaxAcc = pMaxAcc # predicted maximum accelerate
        self.pMaxW = pMaxW # predicted maximum angular velocity

class RobotCommand:
    def __init__(self, robot:Robot, target: Workbench):
        self.robot = robot
        self.target = target