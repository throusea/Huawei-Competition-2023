from robot import Robot, RobotState
from workbench import Workbench
import math
import myutil


def mov_predict(robot: Robot, last: int):
    dx = robot.vel * math.cos(robot.rot) * 0.02 * last
    dy = robot.vel * math.sin(robot.rot) * 0.02 * last
    return robot.pos[0] + dx, robot.pos[1] + dy


class RobotControl:
    kp_f = 10
    kd_f = 2
    kp_r = 30
    kd_r = 5

    forward_ban = []

    def forward(self, robot: Robot):
        for i in self.forward_ban:
            if i == robot.id:
                self.rotate(robot)
                return
        if robot.state == RobotState.IDLE:
            return
        if robot.state == RobotState.TAKING:
            bench = robot.loadingTask.fo
        else:
            bench = robot.loadingTask.to
        distance = ((bench.pos[0] - robot.pos[0]) ** 2 + (
                bench.pos[1] - robot.pos[1]) ** 2) ** 0.5
        next_vel = max(-2, min(self.kp_f * distance - self.kd_f * robot.vel, 6))
        print("forward %d %f" % (robot.id, next_vel))
        self.rotate(robot)

    def rotate(self, robot: Robot):
        if robot.state == RobotState.TAKING:
            bench = robot.loadingTask.fo
        else:
            bench = robot.loadingTask.to
        if bench.pos[0] == robot.pos[0]:
            if bench.pos[1] > robot.pos[0]:
                angle = math.pi/2
            else:
                angle = -math.pi/2
        else:
            angle = math.atan((bench.pos[1] - robot.pos[1]) / (bench.pos[0] - robot.pos[0]))
        if angle < 0:
            angle = angle + math.pi
        if bench.pos[1] < robot.pos[1]:
            angle = angle + math.pi
        da = angle - robot.rot
        next_w = max(-math.pi, min(self.kp_r * da - self.kd_r * robot.w, math.pi))
        print("rotate %d %f" % (robot.id, next_w))

    def buy(self, robot: Robot):
        print("buy %d" % robot.id)

    def sell(self, robot: Robot):
        print("sell %d" % robot.id)

    def collision_predict(self, robots: [Robot]):
        result = [[False, False, False, False], [False, False, False, False], [False, False, False, False],
                  [False, False, False, False]]
        for i in range(1, 16):
            poses = []
            for j in range(0, 4):
                poses.append(mov_predict(robots[j], i))
            for j in range(0, 3):
                for k in range(j + 1, 4):
                    dist = ((poses[j][0] - poses[k][0]) ** 2 + (poses[j][1] - poses[k][1]) ** 2) ** 0.5
                    if dist < 1.3:
                        result[j][k] = result[k][j] = True
                        return result
        return result

    def collision_avoid(self, robot1: Robot, robot2: Robot):
        self.forward_ban.clear()
        if robot1.state == RobotState.IDLE:
            return
        if robot2.state == RobotState.IDLE:
            return
        self.forward_ban.append(robot1.id)
        self.forward_ban.append(robot2.id)

        if robot1.state == RobotState.TAKING:
            bench1 = robot1.loadingTask.fo
        else:
            bench1 = robot1.loadingTask.to
        distance1 = ((bench1.pos[0] - robot1.pos[0]) ** 2 + (
                bench1.pos[1] - robot1.pos[1]) ** 2) ** 0.5
        next_vel1 = max(-2, min(self.kp_f * distance1 - self.kd_f * robot1.vel, 6))

        if robot2.state == RobotState.TAKING:
            bench2 = robot2.loadingTask.fo
        else:
            bench2 = robot2.loadingTask.to
        distance2 = ((bench2.pos[0] - robot2.pos[0]) ** 2 + (
                bench2.pos[1] - robot2.pos[1]) ** 2) ** 0.5
        next_vel2 = max(-2, min(self.kp_f * distance2 - self.kd_f * robot2.vel, 6))

        if next_vel1 > robot1.vel:
            if next_vel2 > robot2.vel:
                print("forward %d %f" % (robot1.id, next_vel1))
                print("forward %d %f" % (robot2.id, robot2.vel-1))
            else:
                print("forward %d %f" % (robot1.id, next_vel1))
                print("forward %d %f" % (robot2.id, next_vel2))
        else:
            if next_vel2 > robot2.vel:
                print("forward %d %f" % (robot1.id, next_vel1))
                print("forward %d %f" % (robot2.id, next_vel2))
            else:
                print("forward %d %f" % (robot1.id, next_vel1))
                print("forward %d %f" % (robot2.id, -2))

