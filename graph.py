from workbench import Workbench, NEXT_WORKBENCH
from item import ITEM_INPUT, ITEM_BUY, ITEM_SELL
from edge import Edge
from robot import Robot
import numpy as np
import random
import math
import myutil

TOTAL_FRAME = 9000

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
        self.q[w1.id][w2.id] += self.learn_rate * (f - self.q[w1.id][w2.id])
    
    def is_active_outbench(self, w: Workbench, t: float):
        return myutil.is_in_set(w.ty, self.disable_bench) == False and (w.output == 1 or (t+150 >= w.status and w.status != -1))
    
    def is_active_inbench(self, w1: Workbench, w2: Workbench):
        return (myutil.is_in_set(w2.ty, self.disable_bench) == False) and (myutil.is_in_set(w1.ty, ITEM_INPUT[w2.ty])) and (myutil.is_in_set(w1.ty, w2.inputs)) == False
    
    def is_benchlocked(self, w: Workbench, item_id: int):
        return w.isLock(item_id)
    
    def is_bench_predict_unlock(self, out_w: Workbench, frame: int):
        if out_w.ty > 3 or out_w.getLockTime(out_w.ty) == -1:
            return False
        return out_w.getLockTime(out_w.ty) + 45 <= frame

    def bonus(self, w: Workbench, robots: [Robot]):
        no = w.num_in_inputset()
        b = 1
        if self.num_of_wid[w.ty] >= 6:
            for r in robots:
                if r.loadingTask != None and r.loadingTask.to.id == w.id:
                    b *= 2
        if self.num_of_wid[7] > 0:
            if w.ty == 9:
                return 0.01
            elif no == 0:
                return 1 * b
            elif no == 1:
                return 1.4 * b
            elif no == 2:
                return 2 * b
        else:
            if no == 0:
                return 1
            elif no == 1:
                return 1.5
        return 1
    
    def indep(self, w: Workbench, robots: [Robot]):
        o = 0
        if self.num_of_wid[7] == 0:
            return 1
        for wbs in self.workbenches:
            if  (wbs.status != -1 or wbs.output == 1) and wbs.ty == w.ty:
                o += 1
            if myutil.is_in_set(w.ty, wbs.inputs):
                o += 1
        for r in robots:
            if r.itemId == w.ty:
                o += 1
        if w.ty > 3:
            if o - self.num_of_wid[7] > 0:
                return 0.5 ** (o-self.num_of_wid[7])
            elif o > 1 and self.num_of_wid[7] >= 4:
                return 0.4
            else:
                return 1
        else:
            return 1
        # if o == 0:
        #     return 50
        # else:
        #     return 1
        
    def target(self, item_id: int, in_w: Workbench):
        if self.num_of_wid[7] == 0:
            # if item_id <= 3 and in_w.ty == 9:
            #     return 0.01
            return 1
        else:
            if in_w.ty > 3 and self.num_of_wid[in_w.ty] <= 1:
                return 1
        return 1
    
    def get_profit(self, item_id: int, in_w: Workbench, robots: [Robot]):
        return (ITEM_SELL[item_id] - ITEM_BUY[item_id]) * self.bonus(in_w, robots) * self.indep(in_w, robots) * self.target(item_id, in_w)
    
    def any_more_great_robot(self, r_pos: (float, float), w: Workbench, robots: [Robot]):
        for r in robots:
            if r.loadingTask != None:
                task = r.loadingTask
                if task.to.id == w.id and myutil.dist(r.pos, w.pos) < myutil.dist(r_pos, w.pos):
                    return True
            else:
                if myutil.dist(r.pos, w.pos) < myutil.dist(r_pos, w.pos):
                    return True
        return False

    def compare_to_ans(self, new_w: (Workbench, Workbench), old_w: (Workbench, Workbench)):
        if old_w[0] == None or old_w[1] == None:
            return 1
        if new_w[0].ty == old_w[0].ty and new_w[1].ty == old_w[1].ty:
            if new_w[1].output > old_w[1].output:
                return 1.5
        return 1

    def get_active_edge(self, r_pos, near_w: Workbench=None, robots: [Robot]=None, frame: int=0):
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
                   (self.get_profit(w1.ty, w2, robots) * self.compare_to_ans((w1, w2), ans_w) / (t1 + t2) > profit / (t[0] + t[1])) and\
                   (self.is_benchlocked(w1, w1.ty) == False or self.is_bench_predict_unlock(w1, frame) == True) and self.is_benchlocked(w2, w1.ty) == False and\
                   self.any_more_great_robot(r_pos, w1, robots) == False and (t1+t2) * 1.15 <= TOTAL_FRAME - frame:
                    # dist = dist_tmp
                    t = (t1, t2)
                    profit = self.get_profit(w1.ty, w2, robots)
                    ans_w = (w1, w2)
        # if ans_w[0] != None and ans_w[1] != None:
        #     raise Exception(str(ans_w[0]))
        return ans_w

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

    def print_edges(self):
        print(self.edge_matrix)
        