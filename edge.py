from workbench import Workbench
import math

class Edge:
    def __init__(self, depart: Workbench, relay: Workbench, to: Workbench):
        self.depart = depart
        self.relay = relay
        self.to = to
        self.dis = math.dist(depart.pos, relay.pos)+math.dist(relay.pos, to.pos);