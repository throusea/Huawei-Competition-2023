from item import Item
from enum import Enum
from workbench import Workbench

class RobotState(Enum):
    IDLE = -1
    TAKING = 0
    LOADING = 1

class Robot():
    def __init__(self, pos: tuple, vel: tuple, acc: float, rot: float, w: float, loadingItem: Item, state: RobotState):
        self.pos = pos # position
        self.vel = vel # velocity
        self.acc = acc # accelerate
        self.rot = rot # rotation
        self.w = w     # angle velocity
        self.state = state
        self.loadingItem = loadingItem
        self.loadingTask = None
        self.state = RobotState.IDLE
    
    def set_task(self, e):
        e.set_cmd(self)
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