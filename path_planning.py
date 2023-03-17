from graph import Graph
from edge import Edge
from robot import Robot, RobotState
from workbench import Workbench, DISABLE_WORKBENCH
from queue import Queue
import time

# class Task:
#     def __init__(self, buy_fo, sell_to):
#         # self.subTasks = []
#         self.buy_fo = buy_fo
#         self.sell_to = sell_to

class PathPlanning:
    def __init__(self, graph: Graph, robots: list):
        self.graph = graph
        self.robots = robots
        self.num_of_wid = [0 for _ in range(8)]
        self.idle_queue = Queue()     # item is Edge
        self.running_queue = Queue()  # item is (Edge, time)
    
    def anaylse_wb(self):
        wbs = self.graph.workbenches
        for w in wbs:
            self.num_of_wid[w.id] += 1
        for i in range(8):
            if self.num_of_wid[i] == 0:
                # DISABLE_WORKBWNCH[i]
                pass

    def init_task(self):
        # init the task robot can do
        for e in self.graph.edges:
            self.idle_queue.put(e)
        pass

    def select_one_edge(self):
        e: Edge = self.idle_queue.get()
        self.running_queue.put((e, time.time()))
        return e

    def execute(self):
        cmd_list = []
        for b in self.robots:
            if b.state == RobotState.IDLE:
                b.state = RobotState.RUNNING
                e = self.select_one_edge()
                b.set_task(e)
