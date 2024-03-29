from path_planning import PathPlanning
from graph import Graph
from workbench import Workbench
from robot import Robot


robs = [
    Robot((25, 25)),
    Robot((25, 42)),
    Robot((42, 25)),
    Robot((12, 25))
]

wbs = [
    Workbench(0, 1, (1,1)),
    Workbench(1, 2, (1,11)),
    Workbench(2, 3, (1,21)),
    Workbench(3, 4, (1,31)),
    Workbench(4, 5, (1,41)),
    Workbench(5, 6, (2,1)),
    Workbench(6, 7, (2,11)),
    Workbench(7, 8, (2,21)),
    Workbench(8, 9, (2,31))
]

graph = Graph(wbs)

graph.create_edges()

pln = PathPlanning(graph, robs)

wbs[0].output = 1
wbs[1].output = 1
wbs[2].output = 1
pln.allocate_rob()
print(pln.get_all_tasktype_fm_rob())