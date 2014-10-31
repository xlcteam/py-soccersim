import pygame
from pygame.locals import *

import Box2D
from Box2D.b2 import *

from env import Env
from robot import Robot
from objects import BoxProp

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

    env = Env('teamA', 'teamB', [WIDTH, HEIGHT], display)

    robotA1 = Robot(env, [140, 200], [21*3, 21*3], -90, (255,0,0), b2world)
    robotA2 = Robot(env, [140, 356], [21*3, 21*3], -90, (255,0,122), b2world)
    robotB1 = Robot(env, [580, 200], [21*3, 21*3], 90, (0,255,0), b2world)
    robotB2 = Robot(env, [580, 356], [21*3, 21*3], 90, (0,255,122), b2world)

    robotA1.vec = [100, 0]

    robots = []
    robots.append(robotA1)
    robots.append(robotA2)
    robots.append(robotB1)
    robots.append(robotB2)

    props = []
    # goal props
    # back
    props.append(BoxProp(env, {'size':[6, 187], 'position':[48, 180]}, b2world))
    props.append(BoxProp(env, {'size':[6, 187], 'position':[673, 180]}, b2world))
    # top
    props.append(BoxProp(env, {'size':[37, 7], 'position':[49, 180]}, b2world))
    props.append(BoxProp(env, {'size':[37, 7], 'position':[643, 180]}, b2world))
    # bottom
    props.append(BoxProp(env, {'size':[37, 7], 'position':[49, 361]}, b2world))
    props.append(BoxProp(env, {'size':[37, 7], 'position':[643, 361]}, b2world))

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

        for prop in props:
            prop.draw()

        b2world.Step(TIME_STEP, 10, 10)
        pygame.display.flip()
        clock.tick(FPS)

        b2world.ClearForces()

    pygame.quit()
    print "Quit"



