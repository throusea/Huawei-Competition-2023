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

def diff_angle(ag1: float, ag2: float): # the included angle between ag1 and ag2 (rotate from ag1 to ag2), in [-pi, pi]
    diff = ag2 - ag1
    if diff > math.pi:
        diff = diff - 2 * math.pi
    if diff < -math.pi:
        diff = diff + 2 * math.pi
    return diff

def resultant_force(forces: [Force]): # the resultant force of many forces
    result=Force(0,0)
    for f in forces:
        result.x = result.x+f.x
        result.y = result.y+f.y
    return result

krf = 20
kef = 15
kb = 6
def repulsion(robot1: Robot, robot2: Robot): # the repulsive force that robot1 get from robot2
    r = myutil.dist(robot1.pos, robot2.pos)
    mag = krf / r ** 2
    ag = angle(robot2.pos, robot1.pos)
    fx = mag * math.cos(ag)
    fy = mag * math.sin(ag)
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
    d = myutil.dist(robot.pos,bench.pos)
    mag = max(1,1/d**2)
    return Force(kb * mag * math.cos(ag), kb * mag * math.sin(ag))

kp_f = 7
kd_f = 4
kp_r = 30
kd_r = 3

def next_velocity_and_angular_velocity(robot: Robot, other: Robot):
    all_forces = []
    for i in range(0,len(other)):
        if other[i].id == robot.id:
            continue
        all_forces.append(repulsion(robot, other[i]))
    all_forces.append(edge_repulsion(robot))
    all_forces.append(attraction(robot))
    force = resultant_force(all_forces)
    dag = diff_angle(robot.rot, force.angle()) # difference angle between robot.rot and force
    kdag = math.cos(dag)
    if kdag > 0:
        kdag = max(0, kdag - 0.2) / 0.8
    else:
        kdag = min(0, kdag + 0.2) / 0.8
    cfm = force.magnitude()*kdag # magnitude of component force on the direction of robot.rot
    return kp_f * cfm - kd_f * robot.vel, kp_r * dag - kd_r * robot.w

class RobotControl:

    flag = [0,0,0,0]

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

