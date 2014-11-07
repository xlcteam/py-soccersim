import pygame


class Env:
    def __init__(self, teamA, teamB, field_size, display, robots=None,
                 debug=False):
        self.teamA = teamA
        self.teamB = teamB
        self.width = field_size[0]
        self.height = field_size[1]
        self.display = display
        self.ball = None

        self.robots = robots

        self.robots_out = {'A': [False, False], 'B': [False, False]}

        self.debug = debug

        self.field = pygame.image.load('img/field.png')

        self.halftime = 1
        self.teamAscore = 0
        self.teamBscore = 0

    def teamA_add_goal(self):
        self.teamAscore += 1

    def teamB_add_goal(self):
        self.teamBscore += 1

    def draw_field(self):
        self.display.blit(self.field, [0, 0])

    def reset_robots(self):
        for robot in self.robots:
            robot.stop()
            robot.move_to_pos(robot.default_pos)

    def set_ball(self, ball):
        self.ball = ball

    def set_robots(self, robots):
        self.robots = robots
