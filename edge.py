from workbench import Workbench
from enum import Enum
import myutil

# It is like a task
class EdgeState(Enum):
    IDLE = 0
    RUNNING = 1


class Edge:
    def __init__(self, fo: Workbench, to: Workbench):
        self.fo = fo
        self.to = to
        self.dis = myutil.dist(fo.pos, to.pos)
        self.state = EdgeState.IDLE
        self.cmd1 = None
        self.cmd2 = None

    def __str__(self):
        return ("Edge:[\nfo:%s\nto:%s\ndis:%s, state:%s\n]"%(self.fo, self.to, self.dis, self.state))
    
    def get_frame(self):
        return (int) (self.dis * 25 / 3)
