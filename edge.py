from workbench import Workbench
from robot import RobotCommand, Robot
from enum import Enum
import math

# It is like a task
class EdgeState(Enum):
    IDLE = 0
    RUNNING = 1


class Edge:
    def __init__(self, fo: Workbench, to: Workbench):
        self.fo = fo
        self.to = to
        self.dis = math.dist(fo.pos, to.pos)
        self.state = EdgeState.IDLE
        self.cmd1 = None
        self.cmd2 = None
    
    # def set_cmd(self, robot: Robot):
    #     self.cmd1 = RobotCommand(robot, self.fo)
    #     self.cmd2 = RobotCommand(robot, self.to)
    
    def get_frame(self):
        return (int) (self.dis * 25 / 3)
