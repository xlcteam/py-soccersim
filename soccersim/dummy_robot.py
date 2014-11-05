import math


class DummyIRSensor:
    def __init__(self, robot):
        self.robot = robot

    def read(self):
        return self.robot.dict['ir']


class DummyRobot:
    def __init__(self, dict):
        self.dict = dict

        self.ir_sensor = DummyIRSensor(self)
        self.rot_mat = dict['rot_mat']

    def forward(self, speed):
        self.dict['vec'] = (speed, 0)
        self.rotatize()

    def reverse(self, speed):

        self.dict['vec'] = (-speed, 0)
        self.rotatize()

    def left(self, speed):

        self.dict['vec'] = (0, speed)
        self.rotatize()

    def right(self, speed):

        self.dict['vec'] = (0, -speed)
        self.rotatize()

    def stop(self):
        self.dict['vec'] = (0, 0)

    def forward_left(self, speed):

        self.dict['vec'] = (speed/math.sqrt(2), -(speed/(math.sqrt(2))))
        self.rotatize()

    def forward_right(self, speed):

        self.dict['vec'] = (speed/math.sqrt(2), (speed/(math.sqrt(2))))
        self.rotatize()

    def reverse_left(self, speed):

        self.dict['vec'] = (-(speed/math.sqrt(2)), -(speed/(math.sqrt(2))))
        self.rotatize()

    def reverse_right(self, speed):

        self.dict['vec'] = (-(speed/math.sqrt(2)), (speed/(math.sqrt(2))))
        self.rotatize()

    def rotatize(self):
        self.dict['vec'] = (self.dict['vec'][0] * self.rot_mat[0],
                            self.dict['vec'][1] * self.rot_mat[1])

    def wait(self, milisec):
        while milisec > 1:
            step = 100 if milisec > 500 else milisec
            milisec -= pygame.time.delay(step)
