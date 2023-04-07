from graph import Graph
from edge import Edge
from robot import Robot, RobotState
from workbench import Workbench, NEXT_WORKBENCH
from queue import Queue
import time
import numpy as np
import myutil
from copy import copy

# class Task:
#     def __init__(self, buy_fo, sell_to):
#         # self.subTasks = []
#         self.buy_fo = buy_fo
#         self.sell_to = sell_to

class PathPlanning:
    def __init__(self, graph: Graph, robots: [Robot] = []):
        self.graph = graph
        self.robots = robots
        self.num_of_wid = [0 for _ in range(8)]

    def init_task(self, grid_map):
        self.graph.edge_matrix = np.zeros((len(self.graph.workbenches)+1, len(self.graph.workbenches)+1), dtype=Edge)
        # init the task robot can do
        self.graph.init_all()
        self.graph.conv_map(grid_map)

    def get_robots(self):
        return self.robots

    def get_workbenches(self):
        return self.graph.workbenches

    def select_one_edge(self, rob: Robot, frame: int = 0):
        w1, w2 = self.graph.get_active_edge(rob.pos, rob.last_w, self.robots, frame)
        if w1 == None or w2 == None:
            return None
        e = Edge(w1, w2)
        # print('distance between robot %d and bench %d' % (rob.id, w1.ty), myutil.dist(rob.pos, w1.pos))
        e.cmds1 = self.graph.a_star(rob.pos, w1.pos).copy()
        e.cmds2 = self.graph.a_star(w1.pos, w2.pos).copy()
        w1.setLock(w1.ty, frame)
        w2.setLock(w1.ty, frame)
        # self.running_queue.put((e, frame))
        # raise Exception(str(w1))
        return e
    
    # unlock one Robot which turn from TAKING to DELIVERING
    def unlock_first(self, rob: Robot, frame: int=0):
        w1 = rob.loadingTask.fo
        if rob.last_w != None:
            self.graph.update_tasktime(rob.last_w, w1, frame - w1.getLockTime(w1.ty))
        w1.setLock(w1.ty, val = False)

    # unlock one Robot which turn from DELIVERING to IDLE
    def unlock(self, rob: Robot, frame: int=0):
        if rob.loadingTask == None:
            raise Exception('The task of robot is None!')
        w1 = rob.loadingTask.fo
        w2 = rob.loadingTask.to
        self.graph.update_tasktime(w1, w2, frame - w2.getLockTime(w1.ty))
        w2.setLock(w1.ty, val = False)
    
    def unlock_all(self, rob: Robot, frame: int=0):
        if rob.loadingTask == None:
            raise Exception('The task of robot is None!')
        w1 = rob.loadingTask.fo
        w2 = rob.loadingTask.to
        w1.setLock(w1.ty, val = False)
        w2.setLock(w1.ty, val = False)

    def any_more_great_robot(self):
        b = []
        for r in self.robots:
            if r.state == RobotState.TAKING and self.graph.any_more_great_robot(r.pos, r.loadingTask.fo, self.robots):
                b.append(True)
            else:
                b.append(False)
        return b
    
    def change_robot_tobech(self):
        for r1 in self.robots:
            for r2 in self.robots:
                if r1.id == r2.id:
                    continue
                if r1.itemId == r2.itemId and r1.itemId != 0 and r2.itemId != 0 and r1.loadingTask != None and r2.loadingTask != None and\
                   r1.state == RobotState.DELIVERING and r2.state == RobotState.DELIVERING and\
                   myutil.dist(r1.pos, r1.loadingTask.to.pos) + myutil.dist(r2.pos, r2.loadingTask.to.pos) >\
                   myutil.dist(r1.pos, r2.loadingTask.to.pos) + myutil.dist(r2.pos, r1.loadingTask.to.pos) + 5:
                   t = r1.loadingTask.to
                   r1.loadingTask.to = r2.loadingTask.to
                   r2.loadingTask.to = t

    def allocate_rob(self, frame: int):
        cmd_list = []
        for b in self.robots:
            if b.state == RobotState.IDLE:
                e = self.select_one_edge(b, frame)
                b.set_task(e)
    
    def get_all_tasktype_fm_rob(self):
        tasks = []
        for i, rob in enumerate(self.robots):
            if rob.loadingTask != None:
                tasks.append((i, rob.loadingTask.fo.ty, rob.loadingTask.to.ty))
        return tasks