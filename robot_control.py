import myutil
import numpy as np
from robot import Robot
from robot import RobotState
from edge import Edge
from workbench import Workbench
from path_planning import PathPlanning
from robot_control import RobotControl



class MyListenser:

    def __init__(self, plan: PathPlanning):
        self.plan = plan
        self.rob: [Robot] = self.plan.get_robots()
        self.bench: [Workbench] = self.plan.get_workbenches()
        self.near = [0, 0, 0, 0]
        self.mp = np.zeros(100, 100)
        # self.date = open("date.txt", "w")
        self.frame = 0
        self.m = 0

    def check_dis(self, rob: Robot, bench: Workbench):
        dis: float = myutil.dist(rob.pos, bench.pos)
        v: float = 0.12
        t: float = dis / v
        if (t >= bench.status) and (bench.status != -1):
            return True
        else:
            return False

    def change_robot_command(self, rc: RobotControl, rob: Robot, edge: Edge, near: int, q: bool):#changecommand
        if rob.state == RobotState.IDLE:
            if edge == None:
                return 0
            else:
                rob.state = RobotState.TAKING
                return edge.fo.id
        elif rob.state == RobotState.TAKING:
            if q and rob.itemId == 0:
                self.plan.unlock_all(rob, self.frame)
                rob.state = RobotState.IDLE
                rob.loadingTask = None
                return 0
            if rob.itemId == 0 and near == edge.fo.id:
                rc.buy(rob)

            if rob.itemId != 0:
                rob.state = RobotState.DELIVERING
                self.plan.unlock_first(rob, int(self.frame))
                # if rob.last_w != None:
                #     self.date.write(str.format("update from bench %d to bench %d: %f\n" % (rob.last_w.id, rob.loadingTask.fo.id, self.plan.graph.get_predict_tasktime(rob.last_w, rob.loadingTask.fo))))
                rob.last_w = edge.fo
                return edge.to.id
        else:
            if rob.itemId != 0 and near == edge.to.id:
                rc.sell(rob)

            if rob.itemId == 0:
                rob.state = RobotState.IDLE
                self.plan.unlock(rob, int(self.frame))
                # if rob.last_w != None:
                #     self.date.write(str.format("update from bench %d to bench %d: %f\n" % (rob.last_w.id, rob.loadingTask.to.id, self.plan.graph.get_predict_tasktime(rob.last_w, rob.loadingTask.to))))
                rob.last_w = edge.to
                rob.loadingTask = None
                return 0

    def collect(self):#每一帧的评测机返回的信息在这里读入
        s = input()
        num_bench = int(s)

        for i in range(0, num_bench):#工作台信息
            s = input()
            s = s.split(' ')

            type = s[0]
            ben_pos: tuple = (s[1], s[2])
            self.bench[i].status = int(s[3])
            self.bench[i].inputs = int(s[4])
            self.bench[i].output = int(s[5])

        for i in range(0, 4):#机器人信息
            s = input()
            s = s.split(' ')

            self.near[i] = int(s[0])
            self.rob[i].itemId = int(s[1])
            self.rob[i].w = float(s[4])
            self.rob[i].vel = (float(s[5]) ** 2 + float(s[6]) ** 2) ** 0.5
            self.rob[i].rot = float(s[7])
            self.rob[i].pos = (float(s[8]), float(s[9]))



    def check_EOF(self):#检查EOF，不用改
        try:
            s = input()
            s = s.split()
            self.frame = s[0]
            return True
        except EOFError:
            return False

    # def check_k(self)://这是被删掉的地图特化
    #     m1 = [13.74937475,5,13,2,35, 0.15,35,0,25,2] //斥力较小 工作台引力大
    #     m2 = [55, 5, 11, 2, 50,0.3, 15, 0, 25, 2] // 斥力大
    #     m3 = [13.8,5,11,2, 175,0.25,35,0,25,2] //斥力较小
    #     m4 = [55, 5, 11, 2, 175,0.25, 35, 0, 25, 2]//斥力最大
    #     if self.m == 1:
    #         return m1
    #     elif self.m == 2:
    #         return m2
    #     elif self.m == 3:
    #         return m3
    #     else:
    #         return m4
    def interact(self):
        rc = RobotControl() #新建robotcontrol
        rc.set_const() #设定参数
        if not self.check_EOF(): #EOF
            return False
        self.collect() #收集评测机返回数据
        print(self.frame) #打印当前帧
        rc.update_frame(self.frame) #更新rc的帧
        target = [0]
        self.plan.change_robot_tobech() #planner给robot分配新一轮的任务
        li = self.plan.any_more_great_robot() #planner检测是否有更优任务
        for i in range(0, 4): #给4个机器人更新状态(change_robot_command函数)，并且返回每个机器人的目的workbench，存到target数组中
            #### 一个可行的更改思路，就是把workbench改成node或是什么其他的类型，返回改为机器人该去的node，这样其他的都不用大改
            target.append(self.change_robot_command(rc, self.rob[i], self.rob[i].loadingTask, self.near[i], li[i]))

        # occ = [False, False, False, False]#碰撞检测，现在没用
        #
        # for i in range(0, 4):
        #     if not occ[i]:
        #         rc.forward(self.rob[i], self.rob)

        # self.date.write(str("Frame:%s\n"%(self.frame)))#输出信息
        # self.date.write(str(self.near)+"\n")
        # for i in range(0, 4):
        #     self.date.write(str(self.rob[i]) + "\n")

        # for i in range(0, len(self.bench)):
        #     self.date.write(str(self.bench[i]) + "\n")
        # self.date.write(str(self.plan.graph.q))
        # self.date.write("\n")


        self.plan.allocate_rob(int(self.frame))
        # self.date.flush()

        return True

    def init_data(self): #初始化数据，整场比赛只会执行一次
        cnt_rob = -1 #计数器
        cnt_ben = -1 #计数器
        p = True
        for i in range(1, 101):
            inp = input()
            for j in range(1, 101):
                c = inp[j - 1]
                if c == 'A':#机器人
                    cnt_rob += 1
                    new_rob = Robot(cnt_rob, (float(j - 1) * 0.5 + 0.25, 50 - 0.25 - float(i - 1) * 0.5))
                    self.rob.append(new_rob)
                    # print(str(new_rob.id)+" "+str(new_rob.pos[0])+" "+str(new_rob.pos[1]))
                    self.mp[i-1][j-1] = 0
                elif c == '.': #空地
                    self.mp[i - 1][j - 1] = 0
                elif c == '#':
                    self.mp[i - 1][j - 1] = 1
                else: #工作台，但是新题目下需要加一个if判断是不是障碍物
                    self.mp[i - 1][j - 1] = 0
                    if p:
                        p = False
                        if int(c) == 1:
                            self.m = 1
                        elif int(c) == 6:
                            self.m = 2
                        elif int(c) == 3:
                            self.m = 3
                        elif int(c) == 7:
                            self.m = 4
                    cnt_ben += 1
                    new_ben = Workbench(cnt_ben, int(c), (float(j - 1) * 0.5 + 0.25, 50 - 0.25 - float(i - 1) * 0.5))
                    self.bench.append(new_ben)
        ##这个位置地图已经读入完场了
        ##可以在这个地方加一个新的函数，判断每个3*3和2*2的格子能否向其四周的几个地方运动
        self.plan.init_task()##初始化任务
        pass

    """def close_file(self):
        self.date.close()
        pass"""