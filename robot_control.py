from robot import Robot
from workbench import Workbench
import math

class RobotControl:
    currentRobot: Robot
    kp_f = 0.5
    kd_f = 0.5
    kp_r = 0.5
    kd_r = 0.5

    def getRobot(self, robot: Robot):  # get the robot as the subject of the next operations.
        self.currentRobot = robot

    def forward(self, bench: Workbench):
        distance = ((bench.pos[0] - self.currentRobot.pos[0]) ** 2 + (bench.pos[1] - self.currentRobot.pos[1]) ** 2) ** 0.5
        next_vel=max(-2,min(self.kp_f*distance-self.kd_f*self.currentRobot.vel,6))
        print("forward %d %f" % (self.currentRobot.id, next_vel))

    def rotate(self, bench: Workbench):
        angle = math.atan((bench.pos[1] - self.currentRobot.pos[1])/(bench.pos[0] - self.currentRobot.pos[0]))
        if bench.pos[1]<self.currentRobot.pos[1]:
            angle=angle+math.pi
        next_w=max(-math.pi,min(self.kp_r*angle-self.kd_r*self.currentRobot.w,math.pi))
        print("rotate %d %f" % (self.currentRobot.id, next_w))

    def buy(self):
        print("buy %d" % self.currentRobot.id)

    def sell(self):
        print("sell %d" % self.currentRobot.id)

    def collision_predict(self, robots: [Robot]):
        pass

    def collision_avoid(self, robot1: Robot, robot2: Robot):
        pass
