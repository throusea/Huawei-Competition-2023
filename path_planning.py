from graph import Graph
from robot import Robot

class PathPlanning:
    def __init__(self, graph: Graph, robots: list):
        self.graph = graph
        self.robots = robots