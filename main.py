#!/bin/bash
import sys
from path_planning import PathPlanning
from robot_control import RobotControl
from graph import Graph
from robot import Robot
from item import Item
from edge import Edge
from workbench import Workbench
from listener import MyListenser

def init_test():
    workbenches = [
        Workbench(0, (1, 1)),
        Workbench(0, (2, 2))
    ]
    edges = [
        Edge(workbenches[0], workbenches[1]),
        Edge(workbenches[1], workbenches[0])
    ]
    graph = Graph(  )
    robots = [
        Robot((0, 0), (0, 0), 1, 1, 1, Item(1)),
        Robot((0, 0), (1, 1), 1, 50, 4, Item(2))
    ]
    pplan = PathPlanning(graph, robots)
    bCont = RobotControl()
    listener = MyListenser(pplan, bCont)
    listener.collect(robots, workbenches)
    pass

def read_util_ok():
    while input() != "OK":
        pass


def finish():
    sys.stdout.write('OK\n')
    sys.stdout.flush()


if __name__ == '__main__':
    init_test() # judge whether the initiation (or the code) is OK
    read_util_ok()
    finish()
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        parts = line.split(' ')
        frame_id = int(parts[0])
        read_util_ok()

        sys.stdout.write('%d\n' % frame_id)
        line_speed, angle_speed = 3, 1.5
        for robot_id in range(4):
            sys.stdout.write('forward %d %d\n' % (robot_id, line_speed))
            sys.stdout.write('rotate %d %f\n' % (robot_id, angle_speed))
        finish()
