from robot import Robot, RobotState
from workbench import Workbench
import math
import myutil


def mov_predict(robot: Robot, last: int):
    dx = robot.vel * math.cos(robot.rot) * 0.02 * last
    dy = robot.vel * math.sin(robot.rot) * 0.02 * last
    return robot.pos[0] + dx, robot.pos[1] + dy

def angle(p1: tuple, p2: tuple): # p2 -> p1!
    if p2[0] == p1[0]:
        if p2[1] > p1[0]:
            ag = math.pi / 2
        else:
            ag = -math.pi / 2
    else:
        ag = math.atan((p2[1] - p1[1]) / (p2[0] - p1[0]))
    if ag < 0:
        ag = ag + math.pi
    if p2[1] < p1[1]:
        ag = ag + math.pi
    return ag

def resultant_force(forces: [Force]):
    result=Force(0,0)
    for f in forces:
        result.x = result.x+f.x
        result.y = result.y+f.y
    return result
class Force:

    def __init__(self, x:float, y:float):
        self.x=x
        self.y=y

    def angle(self):
        return angle((0,0),(self.x,self.y))

class RobotControl:
    kp_f = 7
    kd_f = 1
    kp_r = 30
    kd_r = 3

    forward_ban = [False, False, False, False]
    last_frame = [0, 0, 0, 0]
    avoid_type = [0, 0, 0, 0] # 0->stop, m->turn m degrees

    def forward(self, robot: Robot):
        if robot.state == RobotState.IDLE:
            return
        if robot.state == RobotState.TAKING:
            bench = robot.loadingTask.fo
        else:
            bench = robot.loadingTask.to
        if self.forward_ban[robot.id]:
            if self.last_frame[robot.id] == 0:
                self.forward_ban[robot.id] = False
                self.avoid_type[robot.id] = 0
            else:
                self.last_frame[robot.id] = self.last_frame[robot.id]-1
                if self.avoid_type[robot.id] == 0:
                    print("forward %d %f" % (robot.id, -robot.vel*self.kd_f))
                    print("rotate %d %f" % (robot.id, -robot.w*self.kd_r))
                else:
                    distance = ((bench.pos[0] - robot.pos[0]) ** 2 + (
                            bench.pos[1] - robot.pos[1]) ** 2) ** 0.5
                    next_vel = max(-2, min(self.kp_f * distance - self.kd_f * robot.vel, 6))
                    print("forward %d %f" % (robot.id, next_vel))
                    print("rotate %d %f" % (robot.id, self.avoid_type[robot.id]))
                return

        ag = angle(robot.pos, bench.pos)
        if ag - robot.rot > math.pi:
            da = ag-robot.rot-2*math.pi
        elif ag - robot.rot < -math.pi:
            da = ag-robot.rot+2*math.pi
        else:
            da = ag - robot.rot
        next_w = max(-math.pi, min(self.kp_r * da - self.kd_r * robot.w, math.pi))
        print("rotate %d %f" % (robot.id, next_w))

        if 0.1 > da > -0.1:
            distance = ((bench.pos[0] - robot.pos[0]) ** 2 + (
                    bench.pos[1] - robot.pos[1]) ** 2) ** 0.5
            next_vel = max(-2, min(self.kp_f * distance - self.kd_f * robot.vel, 6))
            print("forward %d %f" % (robot.id, next_vel))
        else:
            print("forward %d %f" % (robot.id, -robot.vel*self.kd_f))


    def buy(self, robot: Robot):
        print("buy %d" % robot.id)

    def sell(self, robot: Robot):
        print("sell %d" % robot.id)

