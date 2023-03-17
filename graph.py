from workbench import Workbench
from item import ITEM_INPUT
from edge import Edge

class Graph():
    def __init__(self, workbeches: list):
        self.workbenches = workbeches
        self.edges = []
    
    def create_edges(self):
        for w1 in self.workbenches:
            for w2 in self.workbenches:
                if w1.id in ITEM_INPUT[w2.id]:
                    self.workbenches.append(Edge(w1, w2))
        