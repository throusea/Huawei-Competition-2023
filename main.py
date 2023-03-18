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


def read_util_ok():
    while input() != "OK":
        pass


def finish():
    sys.stdout.write('OK\n')
    sys.stdout.flush()


if __name__ == '__main__':


    pplan = PathPlanning(Graph())
    listener = MyListenser(pplan)
    listener.init_data()
    read_util_ok()
    finish()
    while True:
        listener.interact()
        finish()
