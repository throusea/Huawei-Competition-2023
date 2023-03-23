from workbench import Workbench, NEXT_WORKBENCH
from item import ITEM_INPUT, ITEM_BUY, ITEM_SELL
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
        self.q = np.zeros((50, 50), dtype=float)
        self.learn_rate = 0.1
    
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
    
    def init_predict_tasktime(self):
        for w1 in self.workbenches:
            for w2 in self.workbenches:
                self.q[w1.id][w2.id] = myutil.dist(w1.pos, w2.pos) / 5 * 50 * 1.1

    def get_predict_tasktime(self, w1: Workbench, w2: Workbench):
        return self.q[w1.id][w2.id]
    
    def get_predict_tasktime_on_pos(self, r_pos: (float, float), w2: Workbench):
        return myutil.dist(r_pos, w2.pos) / 5 * 50 * 1.1
    
    def update_tasktime(self, w1: Workbench, w2: Workbench, f: float):
        return 
        self.q[w1.id][w2.id] += self.learn_rate * (f - self.q[w1.id][w2.id])
    
    def is_active_outbench(self, w: Workbench, t: float):
        return myutil.is_in_set(w.ty, self.disable_bench) == False and (w.output == 1 or (t >= w.status and w.status != -1))
    
    def is_active_inbench(self, w1: Workbench, w2: Workbench):
        return (myutil.is_in_set(w2.ty, self.disable_bench) == False) and (myutil.is_in_set(w1.ty, ITEM_INPUT[w2.ty])) and (myutil.is_in_set(w1.ty, w2.inputs)) == False
    
    def is_benchlocked(self, w: Workbench, item_id: int):
        return w.isLock(item_id)

    def nearest_active_bench(self, pos: (float, float)):
        near_w = None
        dist = 114514
        for w in (self.workbenches):
            if self.is_active_outbench(w) and myutil.dist(w.pos, pos) < dist and self.is_benchlocked(w, w.ty) == False:
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
            if self.is_active_inbench(w1, w2) == True and myutil.dist(w1.pos, w2.pos) < dist and self.is_benchlocked(w2, w1.ty) == False:
                dist = myutil.dist(w1.pos, w2.pos)
                near_w = w2
        return near_w
    
    def get_profit(self, item_id: int):
        return ITEM_SELL[item_id] - ITEM_BUY[item_id]

    def get_active_edge(self, r_pos, near_w: Workbench=None):
        ans_w = (None, None)
        # dist = (114514, 1919810)
        t = (114514, 1919810) 
        profit = 0
        for w1 in self.workbenches:
            if w1 == None:
                raise Exception("Workbenches is None")
            for w2 in self.workbenches:
                if w1 == w2:
                    continue
                # dist_tmp = (myutil.dist(r_pos, w1.pos), myutil.dist(w1.pos, w2.pos))
                
                t1 = self.get_predict_tasktime(near_w, w1) if near_w != None else self.get_predict_tasktime_on_pos(r_pos, w1)
                t2 = self.get_predict_tasktime(w1, w2)
                if self.is_active_outbench(w1, t1) and self.is_active_inbench(w1, w2) and\
                   self.get_profit(w1.ty) / (t1 + t2) > profit / (t[0] + t[1]) and\
                   self.is_benchlocked(w1, w1.ty) == False and self.is_benchlocked(w2, w1.ty) == False:
                    # dist = dist_tmp
                    t = (t1, t2)
                    profit = self.get_profit(w1.ty)
                    ans_w = (w1, w2)
        # if ans_w[0] != None and ans_w[1] != None:
        #     raise Exception(str(ans_w[0]))
        return ans_w

    def print_edges(self):
        print(self.edge_matrix)
        