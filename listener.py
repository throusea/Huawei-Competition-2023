import math
from robot import Robot
from robot import RobotState
from edge import Edge
from workbench import Workbench
from path_planning import PathPlanning
from robot_control import RobotControl

class MyListenser:

    def __init__(self, plan: PathPlanning):
        self.plan = plan
        self.rob : [Robot] = self.plan.get_robots()
        self.bench : [] = self.plan.get_workbench()
        self.near = [0, 0, 0, 0, 0]

    def check_dis(self, rob: Robot, bench: Workbench):
        dis: float = math.dist(rob.pos, bench.pos)
        v: float = 0.12
        t: float = dis/v
        if (t >= bench.status) and (bench.status != -1):
            return True
        else:
            return False


    def change_robot_command(self, rc: RobotControl,  rob: Robot, edge: Edge, near : int):
        if rob.state == RobotState.IDLE:
            if edge.fo.container == 1:
                rob.state = RobotState.TAKING
                return edge.fo.id
            else:
                if self.check_dis(rob, edge.fo):
                    return edge.fo.id
                else:
                    return int(0)
        elif rob.state == RobotState.TAKING:
            if rob.itemId == 0 and near == edge.fo.id:
                rc.buy(rob)

            if rob.itemId != 0:
                rob.state = RobotState.LOADING
                return edge.to.id
        else:
            if rob.itemId != 0 and near == edge.to.id:
                rc.sell(rob)

            if rob.itemId == 0:
                rob.state = RobotState.IDLE
                return 0



    def collect(self):
        p : int = 0
        frame = int(input())
        money = int(input())
        num_bench = int(input())

        for i in range(1, num_bench+1):
            typ = input()
            ben_pos : tuple = (input(), input())
            self.bench[i].state = int(input())
            self.bench[i].inputs = int(input())
            self.bench[i].output = int(input())


        for i in range(1, 5):
            l = []
            for j in range(1, 11):
                l.append(input())
            self.near[i] = int(l[0])+1
            self.rob[i].itemId = int(l[1])
            self.rob[i].w = float(l[4])
            self.rob[i].vel = ( float(l[5]), float(l[6]))
            self.rob[i].rot = float(l[7])
            self.rob[i].pos = ( float(l[8]), float(l[9]))
        return frame
    def interact(self):
        rc = RobotControl()
        frame = self.collect()
        target = [0]
        for i in range (1, 5):
            target.append(self.change_robot_command(rc, self.rob[i], self.rob[i].loadingTask, self.near[i]))

        col = rc.collision_pred(self.rob)
        if col != 0:
            p1 = 0
            p2 = 0
            for i in range(1, 5):
                if ((1<<i)&col) != 0:
                    if p1 == 0:
                        p1 = i
                    else:
                        p2 = i
        rc.collsion_avoid(self.rob[p1], self.rob[p2])

        for i in range (1, 5):
            if ((1<<i)&col) == 0:
                rc.forward(self.rob[i], self.bench[target[i]])

        self.plan.update_idle_queue(frame)
        self.plan.init_task()

    def init_data(self):
        cnt_rob = 0
        cnt_ben = 0

        for i in range(1, 101):
            for j in range(1, 101):
                c = input()
                if c == 'A':
                    cnt_rob += 1
                    new_rob = Robot(cnt_rob, (float(i-1)*0.5+0.25, 50-0.25-float(i-1)*0.5))
                    self.rob.append(new_rob)
                elif c == '.':
                    pass
                else:
                    cnt_ben += 1
                    new_ben = Workbench(cnt_ben, int(c), (float(i-1)*0.5+0.25, 50-0.25-float(i-1)*0.5))
                    self.bench.append(new_ben)

        self.plan.init_task()





