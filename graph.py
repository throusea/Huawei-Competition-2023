from workbench import Workbench, NEXT_WORKBENCH
from item import ITEM_INPUT
from edge import Edge
import numpy as np
import math
import myutil

class Graph():
    def __init__(self, workbenches: [Workbench] = []):
        self.workbenches = workbenches
        self.edge_matrix = np.zeros((len(workbenches)+1, len(workbenches)+1), dtype=Edge)
        self.edges = []
        self.num_of_wid = [0] * 10
        self.disable_bench = 0
    
    def create_edges(self):
        for i, w1 in enumerate(self.workbenches):
            for j, w2 in enumerate(self.workbenches):
                if myutil.is_in_set(w1.ty, ITEM_INPUT[w2.ty]):
                    e = Edge(w1, w2)
                    self.edges.append(e)
                    self.edge_matrix[i][j] = e
                else:
                    self.edge_matrix[i][j] = None

    
    def anaylse_wb(self):
        wbs = self.workbenches
        for w in wbs:
            self.num_of_wid[w.ty] += 1
        for i in range(1,10):
            if self.num_of_wid[i] == 0:
                self.disable_bench |= NEXT_WORKBENCH[i]
    
    def is_active_outbench(self, w: Workbench):
        return myutil.is_in_set(w.ty, self.disable_bench) == False and w.output == 1
    
    def is_active_inbench(self, w1: Workbench, w2: Workbench):
        return (myutil.is_in_set(w2.ty, self.disable_bench) == False) and (myutil.is_in_set(w1.ty, ITEM_INPUT[w2.ty])) and (myutil.is_in_set(w1.ty, w2.inputs)) == False

    def nearest_active_bench(self, pos: (float, float)):
        near_w = None
        dist = 114514
        for w in (self.workbenches):
            if self.is_active_outbench(w) and myutil.dist(w.pos, pos) < dist:
                dist = myutil.dist(w.pos, pos)
                near_w = w
        return near_w
    
    def nearest_active_inbench(self, w1: Workbench):
        near_w = None
        dist = 114514
        for w2 in self.workbenches:
            if w2 == None:
                raise Exception("Workbenches is None")
            if w1.id == w2.id:
                continue
            # if self.is_active_inbench(w1, w2) and w2.ty == 4:
                # raise Exception(format("Error! %d" % w1.ty))
            if self.is_active_inbench(w1, w2) == True and myutil.dist(w1.pos, w2.pos) < dist:
                dist = myutil.dist(w1.pos, w2.pos)
                near_w = w2
        return near_w

    def print_edges(self):
        print(self.edge_matrix)
        