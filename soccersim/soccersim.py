import pygame
from pygame.locals import *

import Box2D
from Box2D.b2 import *

from env import Env
from robot import Robot
from objects import BoxProp
from ball import Ball

if __name__ == "__main__":
    WIDTH = 729
    HEIGHT = 546
    FPS = 30.0
    TIME_STEP = 1.0/FPS

    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('SoccerSim')

    clock = pygame.time.Clock()

    b2world = Box2D.b2World(gravity=(0, 0), doSleep=False)

    env = Env('teamA', 'teamB', [WIDTH, HEIGHT], display, debug=True)

    ball = Ball(env, (WIDTH//2, HEIGHT//2), (8*3, 8*3), (100, 75, 81),
                (WIDTH, HEIGHT), b2world)

    robotA1 = Robot(env, (140, 200), (21*3, 21*3), -90, (255, 0, 0), b2world)
    robotA2 = Robot(env, (140, 356), (21*3, 21*3), -90, (255, 0, 122), b2world)
    robotB1 = Robot(env, (580, 200), (21*3, 21*3), 90, (0, 255, 0), b2world)
    robotB2 = Robot(env, (580, 356), (21*3, 21*3), 90, (0, 255, 122), b2world)

    robotA1.vec = (100, 0)
    robotA2.vec = (100, 0)

    robots = []
    robots.append(robotA1)
    robots.append(robotA2)
    robots.append(robotB1)
    robots.append(robotB2)

    props = []
    # back
    props.append(BoxProp(env, size=[6, 187], pos=[50, 272], world=b2world))
    props.append(BoxProp(env, size=[6, 187], pos=[673, 272], world=b2world))
    # top
    props.append(BoxProp(env, size=[37, 7], pos=[66, 183], world=b2world))
    props.append(BoxProp(env, size=[37, 7], pos=[660, 183], world=b2world))
    # bottom
    props.append(BoxProp(env, size=[37, 7], pos=[66, 364], world=b2world))
    props.append(BoxProp(env, size=[37, 7], pos=[660, 364], world=b2world))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
                for robot in robots:
                    robot.event_response(event)

        env.draw_field()
        for robot in robots:
            robot.update()
            robot.draw()

        ball.draw()

        for prop in props:
            prop.draw()

        b2world.Step(TIME_STEP, 10, 10)
        pygame.display.flip()
        clock.tick(FPS)

        b2world.ClearForces()

    pygame.quit()
    print "Quit"