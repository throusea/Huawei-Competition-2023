from robot import Robot
from robot import RobotState

class listener():
    'pass'


    def __init__(self, r1_state: RobotState, r2_state: RobotState, r3_state: RobotState, r4_state: RobotState):
        self.r1_last_state = r1_state
        self.r2_last_state = r2_state
        self.r3_last_state = r3_state
        self.r4_last_state = r4_state

    def change_one_robot(self, rob: Robot, ls: RobotState):
        pass
    def change_state(self, r1: Robot, r2: Robot, r3: Robot, r4: Robot, ):
        self.change_one_robot(self, r1, self.r1_last_state, )
        self.change_one_robot(self, r2, self.r2_last_state)
        self.change_one_robot(self, r3, self.r3_last_state)
        self.change_one_robot(self, r4, self.r4_last_state)







