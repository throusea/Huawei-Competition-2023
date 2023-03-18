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
        self.graph.edge_matrix = np.zeros((len(self.graph.workbenches)+1, len(self.graph.workbenches)+1))
        # init the task robot can do
        self.graph.create_edges()
        for e in self.graph.edges:
            self.idle_queue.put(e)
        self.graph.anaylse_wb()
        pass

    def select_one_edge(self, rob: Robot):
        w1: Workbench = self.graph.nearest_active_bench(rob.pos)
        w2: Workbench = self.graph.nearest_active_inbench(w1)
        # self.running_queue.put((e, frame))
        return copy(e)

    def get_robots(self):
        return self.robots

    def get_workbenches(self):
        return self.graph.workbenches

    def update_idle_queue(self, frame: int):
        while self.running_queue.empty() is False:
            self.idle_queue.put(self.running_queue.get())

    def allocate_rob(self):
        cmd_list = []
        for b in self.robots:
            if b.state == RobotState.IDLE:
                b.state = RobotState.RUNNING
                e = self.select_one_edge(b)
                b.set_task(e)