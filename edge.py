from workbench import Workbench
import math

class Edge:
    def __init__(self, fo: Workbench, to: Workbench):
        self.fo = fo
        self.to = to
        self.dis = math.dist(fo.pos, to.pos)