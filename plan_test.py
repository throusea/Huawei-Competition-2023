from path_planning import PathPlanning
from graph import Graph
from workbench import Workbench
from robot import Robot
import numpy as np

robs = [
    Robot(0, (2, 1)),
    Robot(1, (25, 42)),
    Robot(2, (42, 25)),
    Robot(3, (12, 25))
]

wbs = [
    Workbench(0, 1, (2,1)),
    Workbench(1, 2, (1,11)),
    Workbench(2, 3, (1,21)),
    Workbench(3, 4, (3,2)),
    Workbench(4, 5, (1,41)),
    Workbench(5, 6, (2,1)),
    Workbench(6, 7, (2,11)),
    Workbench(7, 8, (2,21)),
    Workbench(8, 9, (31,31))
]

grid_map = np.zeros((100, 100))

graph = Graph(wbs)

graph.create_edges()
graph.conv_map(grid_map)

pln = PathPlanning(graph, robs)
pln.init_task()

wbs[0].output = 1
wbs[0].status = 10
wbs[1].status = 10
wbs[2].status = 10

print(graph.conv_map2)
print(graph.conv_real_pos2)

# wbs[3].inputs = 0b010
pln.allocate_rob(0)

for r in robs:
    if r.loadingTask != None:
        print(r.loadingTask.fo.ty, r.loadingTask.to.ty)
        print(r.loadingTask.cmds1)
        print(r.loadingTask.cmds2)