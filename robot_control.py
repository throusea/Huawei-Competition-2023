# If you want to remove or regain repulsion force between robots, go to line 99 and 100.

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
    def multiple(self, c:float):
        return Force(self.x*c,self.y*c)

def target(robot:Robot):
    if robot.state == RobotState.IDLE:
        return None
    if robot.state == RobotState.TAKING:
        return robot.loadingTask.cmds1[robot.loadingTask.cmdid]
    else:
        return robot.loadingTask.cmds2[robot.loadingTask.cmdid]

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

def predict_col(r1: Robot, r2: Robot): #碰撞预测
    if r1.itemId == 7 or r2.itemId == 7:
        return True
    rx1 = r1.pos[0]
    ry1 = r1.pos[1]
    rx2 = r2.pos[0]
    ry2 = r2.pos[1]
    rot1 = r1.rot
    rot2 = r2.rot
    for i in range (0, 150):
        rx1 += math.cos(rot1)*r1.vel
        ry1 += math.sin(rot1) * r1.vel
        rx2 += math.cos(rot2) * r2.vel
        ry2 += math.sin(rot2) * r2.vel
        rot1 += r1.w
        rot2 += r2.w
        if myutil.dist((rx1, ry1), (rx2, ry2)) < 5:
            return True
    return False

def repulsion(robot1: Robot, robot2: Robot, frame:int): # the repulsive force that robot1 get from robot2
    kt = 1
    if not predict_col(robot1, robot2):
       kt = 0.4#发现不会碰撞时斥力倍率
    if int(frame) > 8700:
        if(robot1.itemId == 7):
            kt = 0
        elif(robot2.itemId == 7):
            kt = 1
        else:
            kt = 0.005

    r = myutil.dist(robot1.pos, robot2.pos)
    da = diff_angle(robot1.rot, robot2.rot)
    abs_da = max(da, -da)
    #kdag = abs_da / math.pi * 0.8 + 0.2 # Have repulsion force.
    kdag=0 # Completely remove repulsion force.

    mm = 4
    if mm != 4:
        mag = max(1, krf / r ** 2,0) * kdag
    else:
        mag = max(1, krf * max(1 / r ** 2, 4 * math.e ** (-1.2 * r))) * kdag
    ag = angle(robot2.pos, robot1.pos)
    if abs_da > (math.pi*165/180):
        if diff_angle(robot1.rot, ag) > 0:
            ag = float(ag - (1.1*math.cos(diff_angle(robot1.rot, ag)/2)) * math.pi / 2)
        else:
            ag = float(ag + (1.1*math.cos(diff_angle(robot1.rot, ag)/2)) * math.pi / 2)
    fx = mag*math.cos(ag)
    fy = mag*math.sin(ag)
    return Force(fx*kt,fy*kt)

def edge_repulsion(robot: Robot): # the repulsive force that robot get from all the edges
    fl = Force(kef / robot.pos[0] ** 2, 0)
    fr = Force(-kef / (50 - robot.pos[0]) ** 2, 0)
    fc = Force(0, -kef / (50 - robot.pos[1]) ** 2)
    fb = Force(0, kef / robot.pos[1] ** 2)
    return resultant_force([fl,fr,fc,fb])

def attraction(robot: Robot): # the attractive force that robot get from workbench
    tar=target(robot)
    if tar is None:
        return Force(0,0)
    ag = angle(robot.pos, tar)
    d = myutil.dist(robot.pos,tar)
    mag=1
    return Force(kb * mag * math.cos(ag), kb * mag * math.sin(ag))

def bench_drag(robot:Robot):
    tar=target(robot)
    if tar is None:
        return Force(0,0)
    ag = angle(robot.pos, tar)
    d = myutil.dist(robot.pos,tar)
    dag = diff_angle(robot.rot,ag)
    kdag = math.sin(dag)**2
    mag = (1/d) * kbd * robot.vel
    return Force(mag * math.cos(robot.rot+math.pi),mag * math.sin(robot.rot+math.pi))


prio_state = RobotState.DELIVERING
thresh_dist = 2.2

def set_k(k:[], m:int):
    global krf
    global kef
    global kb
    global kbd
    krf = k[0] # repulsion force between robots
    kef = k[1] # repulsion force between robot and edges
    kb = k[2] # attractive force from workbench
    kbd = k[3] # drag force near workbench
    global kp_f
    global kd_f
    global kp_r
    global kd_r
    kp_f = k[6] # p in PID of velocity
    kd_f = k[7] # d in PID of velocity
    kp_r = k[8] # p in PID of angular velocity
    kd_r = k[9] # d in PID of angular velocity

def next_velocity_and_angular_velocity(robot: Robot, other: Robot, frame:int):
    all_forces = []
    benches_nearer = False
    tar=target(robot)
    if tar is not None:
        tar_dist=myutil.dist(robot.pos,tar)
        if robot.state != prio_state:
            tar_dist += thresh_dist
    for i in range(0,len(other)):
        if other[i].id == robot.id:
            continue
        other_tar=target(other[i])
        if (tar is not None) and (other_tar is not None):
            if other_tar[0] == tar[0] and other_tar[1] == tar[1]:
                other_dist = myutil.dist(other[i].pos,other_tar)
                if other[i].state != prio_state:
                    other_dist += thresh_dist
                benches_nearer |= (other_dist<tar_dist)
        all_forces.append(repulsion(robot, other[i], frame))
    if tar is not None:
        if robot.state != prio_state:
            tar_dist -= thresh_dist
        benches_nearer &= (tar_dist < thresh_dist)
    all_forces.append(edge_repulsion(robot))
    if benches_nearer:
        all_forces.append(attraction(robot).multiple(0.1))
    else:
        all_forces.append(attraction(robot))
    all_forces.append(bench_drag(robot))
    force = resultant_force(all_forces)
    dag = diff_angle(robot.rot, force.angle()) # difference angle between robot.rot and force
    kdag = math.pi/2-abs(dag)
    kdag *= abs(kdag)
    #if kdag > 0:
    #    kdag = max(0, kdag - 0.2) / 0.8
    #else:
    #    kdag = min(0, kdag + 0.2) / 0.8
    cfm = force.magnitude()*kdag # magnitude of component force on the direction of robot.rot
    return kp_f * cfm - kd_f * robot.vel, kp_r * dag - kd_r * robot.w

class RobotControl:

    def __init__(self):
        self.frame = 0
        pass

    def set_const(self):
        set_k([13.8,5,11,2, 175,0.25,35,0,25,2], 1)
        pass
    def update_frame(self, frame:int):
        self.frame = frame
        
    def forward(self, robot: Robot, all_robots: [Robot]):
        nxt = next_velocity_and_angular_velocity(robot, all_robots, self.frame)
        print("forward %d %f" % (robot.id, nxt[0]))
        print("rotate %d %f" % (robot.id, nxt[1]))

    def buy(self, robot: Robot):
        print("buy %d" % robot.id)

    def sell(self, robot: Robot):
        print("sell %d" % robot.id)