def act(robot):
    val = robot.ir_sensor.read()
    if val == 1:
        robot.forward(200)
    if val == 2:
        robot.forward_right(200)
    if val == 3:
        robot.reverse_right(200)
    if val == 4 or val == 5:
        robot.reverse(200)
    if val == 6:
        robot.reverse_left(200)
    if val == 7:
        robot.forward_left(200)
