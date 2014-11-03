import pygame


class Env:
    def __init__(self, teamA, teamB, field_size, display, debug=False):
        self.teamA = teamA
        self.teamB = teamB
        self.width = field_size[0]
        self.height = field_size[1]
        self.display = display
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
