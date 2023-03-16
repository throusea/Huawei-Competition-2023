import math

from robot import Robot
from robot import RobotState
from robot import RobotCommand
from edge import Edge
from workbench import Workbench

class listener:

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








