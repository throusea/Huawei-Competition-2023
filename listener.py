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
        self.bench : [Workbench] = self.plan.get_workbenches()
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
            if edge == None:
                return 0
            if edge.fo.output == 1:
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
        s = input()
        s = s.split(' ')

        frame = int(s[0])
        money = int(s[1])
        s = input()
        num_bench = int(s)

        for i in range(0, num_bench):
            s = input()
            s = s.split(' ')

            type = s[0]
            ben_pos : tuple = (s[1], s[2])
            self.bench[i].status = int(s[3])
            self.bench[i].inputs = int(s[4])
            self.bench[i].output = int(s[5])

        for i in range(0, 4):
            s = input()
            s = s.split(' ')

            self.near[i] = int(s[0])+1
            self.rob[i].itemId = int(s[1])
            self.rob[i].w = float(s[4])
            self.rob[i].vel = (float(s[5])**2 + float(s[6])**2)**0.5
            self.rob[i].rot = float(s[7])
            self.rob[i].pos = (float(s[8]), float(s[9]))

        return frame
    def interact(self):
        rc = RobotControl()
        frame = self.collect()
        print(frame)
        target = [0]
        for i in range (0, 4):
            target.append(self.change_robot_command(rc, self.rob[i], self.rob[i].loadingTask, self.near[i]))

        col = rc.collision_predict(self.rob)
        occ = [False, False, False, False]
        for i in range(0, 4):
            for j in range(i+1, 4):
                if col[i][j]:
                    occ[i] = True
                    occ[j] = True
                    rc.collision_avoid(self.rob[i], self.rob[j])

        for i in range (0, 4):
            if not occ[i]:
                rc.forward(self.rob[i])

        self.plan.update_idle_queue(frame)
        self.plan.init_task()
    def init_data(self):
        cnt_rob = -1
        cnt_ben = -1

        for i in range(1, 101):
            inp = input()
            for j in range(1, 101):
                c = inp[j-1]
                if c == 'A':
                    cnt_rob += 1
                    new_rob = Robot(cnt_rob, (float(j-1)*0.5+0.25, 50-0.25-float(i-1)*0.5))
                    self.rob.append(new_rob)
                    #print(str(new_rob.id)+" "+str(new_rob.pos[0])+" "+str(new_rob.pos[1]))
                elif c == '.':
                    pass
                else:
                    cnt_ben += 1
                    new_ben = Workbench(cnt_ben, int(c), (float(j-1)*0.5+0.25, 50-0.25-float(i-1)*0.5))
                    self.bench.append(new_ben)

        self.plan.init_task()





