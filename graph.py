from typing import Tuple

import convolution
from workbench import Workbench, NEXT_WORKBENCH
from item import ITEM_INPUT, ITEM_BUY, ITEM_SELL
from edge import Edge
from robot import Robot
from queue import PriorityQueue
import numpy as np
import random
import math
import myutil
import convolution as conv

TOTAL_FRAME = 9000


class Graph():
    def __init__(self, workbenches: [Workbench] = [], grid_map = None):
        self.workbenches = workbenches
        self.edge_matrix = np.zeros((len(workbenches)+1, len(workbenches)+1), dtype=Edge)
        self.conv_map2 = []
        self.conv_real_pos = []

        self.num_of_wid = [0] * 10
        self.disable_bench = 0
        self.q = np.zeros((50, 50), dtype=float)
        self.p_list = [0, 0, 0]
        self.k_p = 0
        self.learn_rate = 0.141
        self.k_dist = 1.414 # parameter in pre task
        self.k_t = 1
        self.k_d = 10 # parameter in any more robot
        self.k_las = 1.05 # parameter at the end of time
    
    def create_edges(self):
        for i, w1 in enumerate(self.workbenches):
            for j, w2 in enumerate(self.workbenches):
                if myutil.is_in_set(w1.ty, ITEM_INPUT[w2.ty]):
                    e = Edge(w1, w2)
                    self.edge_matrix[i][j] = e
                else:
                    self.edge_matrix[i][j] = None
    
    def conv_map(self, grid_map):
        self.conv_map2, self.conv_real_pos = conv.conv(grid_map, np.array([[1, 1], [1, 1]]))

    def get_hval(self, grid_pos, w_pos):
        return myutil.dist(self.conv_real_pos[grid_pos], w_pos)
    
    def get_gval(self, g_pos1, g_pos2):
        return myutil.dist(self.conv_real_pos[g_pos1], self.conv_real_pos[g_pos2])

    def get_adjacent_pos(self, grid_pos):
        grid_list = []
        dx = [0, 0, 1, -1, 1, 1, -1, -1]
        dy = [1, -1, 0, 0, 1, -1, 1, -1]
        pos = grid_pos
        for i in range(8):
            n_pos = (pos[0]+dx[i], pos[1]+dy[i])
            if self.conv_map2[n_pos] == 1:
                continue
            if n_pos[0] < 0 or n_pos[0] >= 100:
                continue
            if n_pos[1] < 0 or n_pos[1] >= 100:
                continue
            grid_list.append(n_pos)
        return grid_list
    
    def get_init_pos_2(self, real_pos: tuple):
        """Description
        get the initial position for the robot in convoluted map.

        Args:
            real_pos (tuple): real position of robot

        Returns:
            list[]: the initial position list for robot
        """
        transformed_pos=convolution.get_transformed_pos(real_pos)
        x2_pos=(transformed_pos[0]*2,transformed_pos[1]*2)
        grid_list=[]
        xf=math.floor(x2_pos[0])-1
        xc=math.ceil(x2_pos[0])-1
        yf=math.floor(x2_pos[1])-1
        yc=math.ceil(x2_pos[1])-1
        if xf>=0&yf>=0&self.conv_map2[xf][yf]!=1:
            grid_list.append((xf,yf))
        if xf>=0&yc<=98&self.conv_map2[xf][yc]!=1:
            grid_list.append((xf,yc))
        if xc<=98&yf>=0&self.conv_map2[xc][yf]!=1:
            grid_list.append((xc,yf))
        if xc<=98&yc<=98&self.conv_map2[xc][yc]!=1:
            grid_list.append((xc,yc))
        return grid_list

    def get_init_pos_3(self, real_pos: tuple):
        transformed_pos = convolution.get_transformed_pos(real_pos)
        return math.floor(transformed_pos[0] * 2) - 1, math.floor(transformed_pos[1] * 2) - 1

    def a_star(self, real_pos: tuple, w_pos: tuple):
        """

        Args:
            real_pos (tuple): the real position of robot
            w_pos (tuple): the real position of workbench

        Returns:
            list[(float, float)]: position list
        """
        p_q = PriorityQueue()
        # i_list = self.get_init_pos(real_pos)
        g_pos = conv.get_grid_pos(real_pos)

        p_q.put((0, g_pos))
        fa = {}
        las_pos = None
        cmds = []
        while p_q.empty() == False:
            val, g_pos = p_q.get()
            if conv.close(self.conv_real_pos(g_pos), w_pos):
                las_pos = g_pos
                break
            grid_list = self.get_adjacent_pos(g_pos)
            for cell in grid_list:
                p_q.put((val+self.get_gval(g_pos, cell)+self.get_hval(cell, w_pos), cell))
                fa[cell] = g_pos
        while fa.get(p) != None:
            cmds.append(p)
            p = fa[p]
        return cmds


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
        return myutil.dist(r_pos, w2.pos) / 5 * 50 * 1.2
    
    def update_tasktime(self, w1: Workbench, w2: Workbench, f: float):
        if w1.id != w2.id:
            self.q[w1.id][w2.id] += self.learn_rate * (f - self.q[w1.id][w2.id])
    
    def get_waiting_time(self, w: Workbench, frame: int):
        if self.num_of_wid[7] == 0:
            return 0
        if w.ty == 7:
            if frame > 8000:
                return 100
            else:
                return 50
        elif w.ty > 3:
            if frame > 8000:
                return 50
            else:
                return 25
        return 0
    
    def is_active_outbench(self, w: Workbench, t: float, frame: int):
        return myutil.is_in_set(w.ty, self.disable_bench) == False and (w.output == 1 or (t + self.get_waiting_time(w, frame) >= w.status and w.status != -1))
    
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
                    b *= (1.2+k)
        if self.num_of_wid[7] > 0:
            if w.ty == 9:
                return 0.2
            elif no == 0:
                return 1 * b
            elif no == 1:
                return 1.414 * b
            elif no == 2:
                return 1.732 * b
        else:
            if no == 0:
                return 1
            elif no == 1:
                return 1.2
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
                if task.to.id == w.id and myutil.dist(r.pos, w.pos) < myutil.dist(r_pos, w.pos) + self.k_d:
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
                return 1.414
        return 1
    
    def pre_edge_task(self, r_pos, w: (Workbench, Workbench), frame: int, near_w: Workbench):
        if frame > 8500 or w[0] == None:
            return w
        w_tmp = (None, None)
        for w1 in self.workbenches:
            for w2 in self.workbenches:
                if w1 == w2:
                    continue
                t1 = self.get_predict_tasktime(near_w, w1) if near_w != None else self.get_predict_tasktime_on_pos(r_pos, w1)
                if self.is_active_outbench(w1, t1, frame) and self.is_active_inbench(w1, w2) and\
                   (self.is_benchlocked(w1, w1.ty) == False or self.is_bench_predict_unlock(w1, frame) == True) and self.is_benchlocked(w2, w1.ty) == False and\
                   w2.id == w[0].id and myutil.dist(r_pos, w1.pos) + myutil.dist(w1.pos, w2.pos) < myutil.dist(r_pos, w[0].pos) * self.k_dist:
                    if w_tmp[0] == None:
                        w_tmp = (w1, w2)
                    elif myutil.dist(r_pos, w_tmp[0].pos) + myutil.dist(w_tmp[0].pos, w_tmp[1].pos) > myutil.dist(r_pos, w1.pos) + myutil.dist(w1.pos, w2.pos):
                        w_tmp = (w1, w2)
                #    raise Exception(str.format("%d %d %d %d\n" % (w1.ty,w2.ty,w[0].ty,w[1].ty)))
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
                if self.is_active_outbench(w1, t1, frame) and self.is_active_inbench(w1, w2) and\
                   (self.get_profit(w1.ty, w2, robots, frame) * self.compare_to_ans((w1, w2), ans_w) / (t1 + t2) > profit / (t[0] + t[1])) and\
                   (self.is_benchlocked(w1, w1.ty) == False or self.is_bench_predict_unlock(w1, frame) == True) and self.is_benchlocked(w2, w1.ty) == False and\
                   self.any_more_great_robot(r_pos, w1, robots) == False and (t1+t2) * self.k_las <= TOTAL_FRAME - frame:
                    t = (t1, t2)
                    profit = self.get_profit(w1.ty, w2, robots, frame)
                    ans_w = (w1, w2)
        ans_w = self.pre_edge_task(r_pos, ans_w, frame, near_w)
        if type(ans_w) != tuple:
            raise Exception(str(ans_w))
        return ans_w

    def print_edges(self):
        print(self.edge_matrix)
        