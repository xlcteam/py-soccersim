import pygame
from dummy_robot import DummyRobot


def main(arg):
    robot = DummyRobot(arg)
    while True:
        val = robot.ir_sensor.read()
        if val == 1:
            robot.forward(80)
        if val == 2:
            robot.forward_right(80)
        if val == 3:
            robot.reverse_right(80)
        if val == 4 or val == 5:
            robot.reverse(80)
        if val == 6:
            robot.reverse_left(80)
        if val == 7:
            robot.forward_left(80)
