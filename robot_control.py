from robot import Robot, RobotState
from workbench import Workbench
import math
import myutil


class Force:
    def __init__(self, x:float, y:float):
        self.x=x
        self.y=y

    def angle(self):
        return angle((0,0),(self.x,self.y))

    def magnitude(self):
        return myutil.dist((0,0),(self.x,self.y))

def mov_predict(robot: Robot, last: int):
    dx = robot.vel * math.cos(robot.rot) * 0.02 * last
    dy = robot.vel * math.sin(robot.rot) * 0.02 * last
    return robot.pos[0] + dx, robot.pos[1] + dy

def angle(p1: tuple, p2: tuple): # p1 -> p2!
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

def resultant_force(forces: [Force]): # the resultant force of many forces
    result=Force(0,0)
    for f in forces:
        result.x = result.x+f.x
        result.y = result.y+f.y
    return result

krf = 6
kef = 6
kb = 10
def repulsion(robot1: Robot, robot2: Robot): # the repulsive force that robot1 get from robot2
    r = myutil.dist(robot1.pos, robot2.pos)
    mag = krt / r ** 2
    ag = angle(robot2, robot1)
    fx = r * math.cos(ag)
    fy = r * math.sin(ag)
    return Force(fx,fy)

def edge_repulsion(robot: Robot): # the repulsive force that robot get from all the edges
    fl = Force(kef / robot.pos[0] ** 2, 0)
    fr = Force(-kef / (50 - robot.pos[0]) ** 2, 0)
    fc = Force(0, -kef / (50 - robot.pos[1]) ** 2)
    fb = Force(0, kef / robot.pos[1] ** 2)
    return resultant_force([fl,fr,fc,fb])

def attraction(robot: Robot): # the attractive force that robot get from workbench
    if robot.state == RobotState.IDLE:
        return Force(0,0)
    if robot.state == RobotState.TAKING:
        bench = robot.loadingTask.fo
    else:
        bench = robot.loadingTask.to
    ag = angle(robot.pos, bench.pos)
    return Force(kb * math.cos(ag), kb * math.sin(ag))

kp_f = 7
kd_f = 1
kp_r = 30
kd_r = 3

def next_velocity_and_angular_velocity(robot: Robot, other: Robot):
    all_forces = []
    for r in other:
        if r.id == robot.id:
            continue
        all_forces.append(repulsion(robot, r))
    all_forces.append(edge_repulsion(robot))
    all_forces.append(attraction(robot))
    resultant = resultant_force(all_forces)

    return 0,0

class RobotControl:

    def __init__(self):
        pass

    def forward(self, robot: Robot, all_robots: [Robot]):
        nxt = next_velocity_and_angular_velocity(robot, all_robots)
        print("forward %d %f" % (robot.id, nxt[0]))
        print("rotate %d %f" % (robot.id, nxt[1]))

    def buy(self, robot: Robot):
        print("buy %d" % robot.id)

    def sell(self, robot: Robot):
        print("sell %d" % robot.id)

