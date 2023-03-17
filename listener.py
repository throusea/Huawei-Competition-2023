import math

from robot import Robot
from robot import RobotState
from robot import RobotCommand
from edge import Edge
from workbench import Workbench
from path_planning import PathPlanning
from robot_control import RobotControl

class MyListenser:

    def __init__(self, plan: PathPlanning, ctrl: RobotControl):
        self.plan = plan
        self.ctrl = ctrl

    def check_dis(self, robcom: RobotCommand, bench: Workbench):
        rob: Robot = robcom.robot
        dis: float = math.dist(rob.pos, bench.pos)
        v: float = 0.12
        t: float = dis/v
        if (t >= bench.status) and (bench.status != -1):
            return True
        else:
            return False


    def change_robotcommand(self, robcom: RobotCommand, edge: Edge):
        rob: Robot = robcom.robot
        if rob.state == RobotState.IDLE and self.check_dis(robcom, edge.relay): #change date to taking
            robcom.robot.state = RobotState.TAKING
            robcom.target = edge.relay
        elif rob.state == RobotState.TAKING and rob.loadingItem is not None: #change date to loading
            robcom.robot.state = RobotState.LOADING
            robcom.target = edge.relay
        elif rob.state == RobotState.LOADING and rob.loadingItem is None: #change date to idle
            robcom.robot.state = RobotState.IDLE
        return


    def collect(self, rob: [Robot], bench: [Workbench]):
        frame: int = input()
        money: int = input()
        num_bench: int = input()
        for i in range(1, num_bench+1):
            garbage = input()
            garbage = input()
            garbage = input()
            bench[i].state = input()
            ### miss to define whether the materials are ready or not
            con:int = input()
            if con == 1:
                bench[i].container = WorkbenchState.FULL
            else:
                bench[i].container = WorkbenchState.EMPTY


        for i in range(1, 5):
            ### miss to define the nearest workbench
            rob[i].loadingitem = input() ###need to be change
            ### miss to define the time and collision coefficient
            rob[i].w = input()
            rob[i].vel = (input(), input())
            rob[i].rot = input()
            rob[i].pos = (input(), input())







