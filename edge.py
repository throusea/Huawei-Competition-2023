from workbench import Workbench
from enum import Enum
import myutil

class Edge:
    def __init__(self, fo: Workbench, to: Workbench):
        self.fo = fo
        self.to = to
        self.dis = myutil.dist(fo.pos, to.pos)
        self.cmdid = 0
        self.cmds1 = []
        self.cmds2 = []

    def __str__(self):
        return ("Edge:[\nfo:%s\nto:%s\ndis:%s\n]"%(self.fo, self.to, self.dis))
    
    def get_frame(self):
        return (int) (self.dis * 25 / 3)