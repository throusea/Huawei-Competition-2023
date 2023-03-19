from graph import Graph
from edge import Edge
from robot import Robot, RobotState
from workbench import Workbench, NEXT_WORKBENCH
from queue import Queue
import time
import numpy as np
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
        self.idle_queue = Queue()     # item is Edge
        self.running_queue = Queue()  # item is (Edge, frame)


    def init_task(self):

        self.graph.edge_matrix = np.zeros((len(self.graph.workbenches)+1, len(self.graph.workbenches)+1), dtype=Edge)
        # init the task robot can do
        self.graph.create_edges()
        for e in self.graph.edges:
            self.idle_queue.put(e)
        self.graph.anaylse_wb()
        pass

    def select_one_edge(self, rob: Robot):
        # w1: Workbench = self.graph.nearest_active_bench(rob.pos)
        # if w1 == None:
        #     return None

        # w2: Workbench = self.graph.nearest_active_inbench(w1)
        # if w2 == None:
        #     return None
        w1, w2 = self.graph.get_active_edge(rob.pos)
        if w1 == None or w2 == None:
            return None
        w1.setLock(w1.ty)
        w2.setLock(w1.ty)
        # self.running_queue.put((e, frame))
        return Edge(w1, w2)

    def get_robots(self):
        return self.robots

    def get_workbenches(self):
        return self.graph.workbenches
    
    # unlock one Robot which turn from TAKING to DELIVERING
    def unlock_first(self, rob: Robot):
        w1 = rob.loadingTask.fo
        w1.setLock(w1.ty, False)

    # unlock one Robot which turn from DELIVERING to IDLE
    def unlock(self, rob: Robot, frame: int):
        w1 = rob.loadingTask.fo
        w2 = rob.loadingTask.to
        w1.setLock(w1.ty, False)
        w2.setLock(w1.ty, False)

    def update_idle_queue(self, frame: int):
        # while self.running_queue.empty() is False:
            # self.idle_queue.put(self.running_queue.get())
        pass

    def allocate_rob(self):
        cmd_list = []
        for b in self.robots:
            if b.state == RobotState.IDLE:
                e = self.select_one_edge(b)
                b.set_task(e)
    
    def get_all_tasktype_fm_rob(self):
        tasks = []
        for i, rob in enumerate(self.robots):
            if rob.loadingTask != None:
                tasks.append((i, rob.loadingTask.fo.ty, rob.loadingTask.to.ty))
        return tasks