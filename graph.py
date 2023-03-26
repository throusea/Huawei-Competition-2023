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
        self.p_list = [0, 0, 0]
        self.k_p = 0
        self.k_dist = 1.414 # parameter in pre task
        self.k_t = 1
    
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
        self.k_p = min(self.num_of_wid[7], (self.num_of_wid[1]+self.num_of_wid[2]+self.num_of_wid[3])-self.k_t)
    
    def init_predict_tasktime(self):
        for w1 in self.workbenches:
            for w2 in self.workbenches:
                self.q[w1.id][w2.id] = myutil.dist(w1.pos, w2.pos) / 5 * 50 * 1.1

    def get_predict_tasktime(self, w1: Workbench, w2: Workbench):
        return self.q[w1.id][w2.id]
    
    def get_predict_tasktime_on_pos(self, r_pos: (float, float), w2: Workbench):
        return myutil.dist(r_pos, w2.pos) / 5 * 50 * 1.1
    
    def update_tasktime(self, w1: Workbench, w2: Workbench, f: float):
        if w1.id != w2.id:
            self.q[w1.id][w2.id] += self.learn_rate * (f - self.q[w1.id][w2.id])
    
    def get_waiting_time(self, w: Workbench):
        if w.ty == 7:
            return 50
        return 0
    
    def is_active_outbench(self, w: Workbench, t: float):
        return myutil.is_in_set(w.ty, self.disable_bench) == False and (w.output == 1 or (t + self.get_waiting_time(w) >= w.status and w.status != -1))
    
    def is_active_inbench(self, w1: Workbench, w2: Workbench):
        return (myutil.is_in_set(w2.ty, self.disable_bench) == False) and (myutil.is_in_set(w1.ty, ITEM_INPUT[w2.ty])) and (myutil.is_in_set(w1.ty, w2.inputs)) == False
    
    def is_benchlocked(self, w: Workbench, item_id: int):
        return w.isLock(item_id)
    
    def is_bench_predict_unlock(self, out_w: Workbench, frame: int):
        if out_w.ty > 3 or out_w.getLockTime(out_w.ty) == -1:
            return False
        return out_w.getLockTime(out_w.ty) + 55 <= frame

    def bonus(self, w: Workbench, robots: [Robot], frame: int):
        no = w.num_in_inputset()
        b = 1
        k = frame / 9000
        if self.num_of_wid[w.ty] >= 4:
            for r in robots:
                if r.loadingTask != None and r.loadingTask.to.id == w.id:
                    b *= (1.5+k)
        if self.num_of_wid[7] > 0:
            if w.ty == 9:
                return 0.01
            elif no == 0:
                return 1 * b
            elif no == 1:
                return 1.4 * b
            elif no == 2:
                return 1.7 * b
        else:
            if no == 0:
                return 1
            elif no == 1:
                return 1.1
        return 1

    def p_in_bench(self, robots: [Robot]):
        p_list = [0, 0, 0]
        t_list = [4, 5, 6]
        for i, t in enumerate(t_list):
            o = 0
            for w in self.workbenches:
                if w.ty == t:
                    if (w.status != -1 or w.output == 1):
                        o += 1
                    if w.num_in_inputset() > 0:
                        o += 0.4 * w.num_in_inputset()
                if myutil.is_in_set(t, w.inputs):
                    o += 1
            for r in robots:
                if r.itemId == t:
                    o += 1
                elif r.loadingTask != None and r.loadingTask.to.ty == t:
                    o += 0.4
            p_list[i] = o ** 2
        for i in range(len(p_list)):
            p_list[i] = p_list[i] - self.k_p + 1
            if p_list[i] < 0:
                p_list[i] = 0

        s = p_list[0] + p_list[1] + p_list[2]
        if s != 0:
            p_list[0] /= s
            p_list[1] /= s
            p_list[2] /= s
        for i in range(3):
            if p_list[i] == 0:
                p_list[i] = 114514
            else:
                p_list[i] = 1/p_list[i]
        s = p_list[0] + p_list[1] + p_list[2]
        p_list[0] /= s
        p_list[1] /= s
        p_list[2] /= s 
        self.p_list = p_list
    
    def indep(self, w: Workbench, robots: [Robot], frame: int):
        o = 0
        if self.num_of_wid[7] == 0 or frame > 8000:
            return 1
        if w.ty > 3 and w.ty < 7:
            return self.p_list[w.ty-4]
        else:
            return 1
    
    def get_profit(self, item_id: int, in_w: Workbench, robots: [Robot], frame: int):
        return (ITEM_SELL[item_id] - ITEM_BUY[item_id]) * self.bonus(in_w, robots, frame) * self.indep(in_w, robots, frame)
    
    def any_more_great_robot(self, r_pos: (float, float), w: Workbench, robots: [Robot]):
        for r in robots:
            if r.loadingTask != None:
                task = r.loadingTask
                if task.to.id == w.id and myutil.dist(r.pos, w.pos) < myutil.dist(r_pos, w.pos) + 10:
                    return True
            else:
                if r.state == -1 and myutil.dist(r.pos, w.pos) < myutil.dist(r_pos, w.pos):
                    return True
        return False

    def compare_to_ans(self, new_w: (Workbench, Workbench), old_w: (Workbench, Workbench)):
        if old_w[0] == None or old_w[1] == None:
            return 1
        if new_w[0].ty == old_w[0].ty and new_w[1].ty == old_w[1].ty:
            if new_w[1].output > old_w[1].output:
                return 1.5
        return 1
    
    def pre_edge_task(self, r_pos, w: (Workbench, Workbench), frame: int, near_w: Workbench):
        if frame > 8000:
            return w
        w_tmp = (None, None)
        for w1 in self.workbenches:
            for w2 in self.workbenches:
                if w1 == w2:
                    continue
                t1 = self.get_predict_tasktime(near_w, w1) if near_w != None else self.get_predict_tasktime_on_pos(r_pos, w1)
                if self.is_active_outbench(w1, t1) and self.is_active_inbench(w1, w2) and\
                   (self.is_benchlocked(w1, w1.ty) == False or self.is_bench_predict_unlock(w1, frame) == True) and self.is_benchlocked(w2, w1.ty) == False and\
                   w2.id == w[0].id and myutil.dist(r_pos, w1.pos) + myutil.dist(w1.pos, w2.pos) < myutil.dist(r_pos, w[0].pos) * self.k_dist:
                   w_tmp = (w1, w2)
                #    raise Exception(str.format("%d %d %d %d\n" % (w1.ty,w2.ty,w[0].ty,w[1].ty)))
                   break
        if w_tmp[0] == None:
            return w
        else:
            return w_tmp

    def get_active_edge(self, r_pos, near_w: Workbench=None, robots: [Robot]=None, frame: int=0):
        ans_w = (None, None)
        # dist = (114514, 1919810)
        t = (114514, 1919810)
        profit = 0

        self.p_in_bench(robots)
        for w1 in self.workbenches:
            if w1 == None:
                raise Exception("Workbenches is None")
            for w2 in self.workbenches:
                if w1 == w2:
                    continue
                
                t1 = self.get_predict_tasktime(near_w, w1) if near_w != None else self.get_predict_tasktime_on_pos(r_pos, w1)
                t2 = self.get_predict_tasktime(w1, w2)
                if self.is_active_outbench(w1, t1) and self.is_active_inbench(w1, w2) and\
                   (self.get_profit(w1.ty, w2, robots, frame) * self.compare_to_ans((w1, w2), ans_w) / (t1 + t2) > profit / (t[0] + t[1])) and\
                   (self.is_benchlocked(w1, w1.ty) == False or self.is_bench_predict_unlock(w1, frame) == True) and self.is_benchlocked(w2, w1.ty) == False and\
                   self.any_more_great_robot(r_pos, w1, robots) == False and (t1+t2) * 1.35 <= TOTAL_FRAME - frame:
                    t = (t1, t2)
                    profit = self.get_profit(w1.ty, w2, robots, frame)
                    ans_w = (w1, w2)
        ans_w = self.pre_edge_task(r_pos, ans_w, frame, near_w)
        if type(ans_w) != tuple:
            raise Exception(str(ans_w))
        return ans_w

    def print_edges(self):
        print(self.edge_matrix)
        