from workbench import Workbench
from item import ITEM_INPUT
from edge import Edge
import numpy as np
import math

def is_in_set(b: int, b_set: int):
    return (b_set & (1<<b)) != 0

class Graph():
    def __init__(self, workbeches: [Workbench]):
        self.workbenches = workbeches
        self.edge_matrix = np.zeros((len(workbeches)+1, len(workbeches)+1))
        self.edges = None
        self.disable_bench = 0
    
    def create_edges(self):
        for i, w1 in enumerate(self.workbenches):
            for j, w2 in enumerate(self.workbenches):
                if w1.id in ITEM_INPUT[w2.id]:
                    e = Edge(w1, w2)
                    self.workbenches.append(e)
                    self.edge_matrix[i][j] = e
                else:
                    self.edge_matrix[i][j] = None
    
    def anaylse_wb(self):
        wbs = self.workbenches
        for w in wbs:
            self.num_of_wid[w.id] += 1
        for i in range(8):
            if self.num_of_wid[i] == 0:
                self.disable_bench |= NEXT_WORKBENCH[i+1]
    
    def is_active_outbench(self, w: Workbench):
        return is_in_set(w.id, self.disable_bench) == False and w.output == 1
    
    def is_active_inbench(self, w1: Workbench, w2: Workbench):
        return is_in_set(w2.id, self.disable_bench) == False and is_in_set(w1.id, w2.inputs) == False

    def nearest_active_bench(self, pos: (float, float)):
        near_w = None
        dist = 114514
        for w in (self.workbenches):
            if self.is_active_outbench(w) and math.dist(w.pos, pos) < dist:
                dist = math.dist(w.pos, pos)
                near_w = w
        return near_w
    
    def nearest_active_inbench(self, w1: Workbench):
        near_w = None
        dis = 114514
        for w2 in self.workbenches:
            if self.is_active_inbench(w2) and math.dist(w1.pos. w2.pos):
                dist = math.dist(w1.pos, w2.pos)
                near_w = w2
        return near_w

    def print_edges(self):
        print(self.edge_matrix)
        