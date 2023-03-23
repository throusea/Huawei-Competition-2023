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

    def collision_predict(self, robots: [Robot]):
        result = [[False, False, False, False], [False, False, False, False], [False, False, False, False],
                  [False, False, False, False]]
        #if len(self.forward_ban) > 0:
        #    return result
        for i in range(1, 26):
            poses = []
            for j in range(0, 4):
                poses.append(mov_predict(robots[j], i))
            for j in range(0, 3):
                for k in range(j + 1, 4):
                    dist = ((poses[j][0] - poses[k][0]) ** 2 + (poses[j][1] - poses[k][1]) ** 2) ** 0.5
                    if dist < 0.8:
                        result[j][k] = result[k][j] = True
                        return result
        return result

    def collision_avoid(self, robot1: Robot, robot2: Robot):
        if robot1.state == RobotState.IDLE:
            return
        if robot2.state == RobotState.IDLE:
            return

        if robot1.state != RobotState.DELIVERING and robot2.state != RobotState.DELIVERING:
            self.forward(robot1)
            self.forward(robot2)
            return

        if robot1.state == RobotState.TAKING:
            bench1 = robot1.loadingTask.fo
        else:
            bench1 = robot1.loadingTask.to

        if robot2.state == RobotState.TAKING:
            bench2 = robot2.loadingTask.fo
        else:
            bench2 = robot2.loadingTask.to
        if robot1.vel < 0.01:
            self.forward_ban[robot2.id] = True
            self.last_frame[robot2.id] = 25
            ag1=angle(robot1.pos, bench1.pos)
            da1=ag1-robot2.rot
            if da1 > 0 or da1 < -math.pi/2:
                self.avoid_type[robot2.id]=-math.pi/2
            else:
                self.avoid_type[robot2.id]=math.pi/2
        elif robot2.vel < 0.01:
            self.forward_ban[robot1.id] = True
            self.last_frame[robot1.id] = 25
            ag2=angle(robot2.pos, bench2.pos)
            da2=ag2-robot1.rot
            if da2 > 0 or da2 < -math.pi/2:
                self.avoid_type[robot1.id]=-math.pi/2
            else:
                self.avoid_type[robot1.id]=math.pi/2
        else:
            da=robot1.rot-robot2.rot
            if da > math.pi:
                da = da-math.pi
            if da < -math.pi:
                da = da+math.pi
            if da < - math.pi*5/6 or da > math.pi*5/6:
                self.forward_ban[robot1.id]=True
                self.last_frame[robot1.id]=25
                self.forward_ban[robot2.id]=True
                self.last_frame[robot2.id]=25
                self.avoid_type[robot1.id]=math.pi/2
                self.avoid_type[robot2.id]=math.pi/2
            else:
                self.forward_ban[robot1.id]=True
                self.last_frame[robot1.id]=25
                self.avoid_type[robot1.id]=0
        self.forward(robot1)
        self.forward(robot2)

