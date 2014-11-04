import math


class IRSensor:
    """The IR sensor which returns the way in which the IR Ball is most likely
    located."""

    def __init__(self, robot, pos):
        self.robot = robot
        self.pos = pos

    def read(self):
        dtop = self.robot.env.ball.rect.top - self.robot.rect.top
        dleft = self.robot.env.ball.rect.left - self.robot.rect.left

        angle = math.atan2(dtop, dleft)
        angle *= (180 / math.pi)

        # make sure angle is from <0, 360>
        if (angle < 0):
            angle += 360
        angle = round(angle)

        sensor = 0

        if (angle > (360-360/21)):
            sensor = 7
        elif (angle < (360/21)):
            sensor = 1
        else:
            sensor = math.ceil((angle-(360/21))/((360-360/21)/6)) + 1

        return sensor
