def main(robot):
    while True:
        val = robot.ir_sensor.read()
        if val == 1:
            robot.forward(80)
        if val == 2 or val == 3:
            robot.right(80)
        if val > 3 and val < 5:
            robot.reverse(80)
        if val == 6 or val == 7:
            robot.left(80)
