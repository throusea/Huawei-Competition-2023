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
        return ("Edge:[\nfo:%s\nto:%s\ndis:%s\ncmdid:%d\n cmds1:%s\n cmds2:%s\n]"%(self.fo, self.to, self.dis, self.cmdid, self.cmds1, self.cmds2))
    
    def get_frame(self):
        return (int) (self.dis * 25 / 3)