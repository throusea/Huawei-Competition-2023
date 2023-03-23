from path_planning import PathPlanning
from graph import Graph
from workbench import Workbench
from robot import Robot


robs = [
    Robot(0, (25, 25)),
    Robot(1, (25, 42)),
    Robot(2, (42, 25)),
    Robot(3, (12, 25))
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
    Workbench(8, 9, (31,31))
]

graph = Graph(wbs)

graph.create_edges()

pln = PathPlanning(graph, robs)
pln.init_task()

wbs[6].output = 0
wbs[0].status = 10
wbs[1].status = 10
wbs[2].status = 10
pln.allocate_rob()

for r in robs:
    if r.loadingTask != None:
        print(r.loadingTask.fo.ty, r.loadingTask.to.ty)

# print(pln.select_one_edge(robs[0]))

for w1 in graph.workbenches:
    for w2 in graph.workbenches:
        print((int)(graph.get_predict_tasktime(w1, w2)), end=" ")
    print()

print(wbs[0].getLockTime(wbs[0].ty))
# for e in graph.edges:
    # print(e.__str__())
# print(pln.get_all_tasktype_fm_rob())

# print(graph.get_active_edge((0, 0)))

# print(graph.is_benchlocked(wbs[0], 1))