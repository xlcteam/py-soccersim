import pygame
from pygame.locals import *
import sys
import imp
import os

import Box2D
from Box2D.b2 import *

from env import Env
from robot import Robot
from objects import BoxProp
from ball import Ball

from robothread import RoboThread


def import_(filename):
    path, name = os.path.split(filename)
    name, ext = os.path.splitext(name)

    modname = "%s_%s" % ("imp_", name)

    file, filename, data = imp.find_module(name, [path])
    mod = imp.load_module(name, file, filename, data)
    return mod

if __name__ == "__main__":
    WIDTH = 729
    HEIGHT = 546
    TABLE_WIDTH = WIDTH
    TABLE_HEIGHT = 65

    FPS = 30.0
    TIME_STEP = 1.0/FPS

    if len(sys.argv) < 3:
        print "usage: {0} teamA teamB".format(sys.argv[0])
        sys.exit(-1)

    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT+TABLE_HEIGHT))
    display.fill((0, 86, 27))
    pygame.display.set_caption('SoccerSim')

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 60)

    b2world = Box2D.b2World(gravity=(0, 0), doSleep=False)

    env = Env('teamA', 'teamB', [WIDTH, HEIGHT], display, debug=True)

    robotA1 = Robot(env, (140, 200), (21*3, 21*3), -90, (255, 0, 0), 'A1',
                    b2world)
    robotA2 = Robot(env, (140, 356), (21*3, 21*3), -90, (255, 0, 122), 'A2',
                    b2world)
    robotB1 = Robot(env, (580, 200), (21*3, 21*3), 90, (0, 255, 0), 'B1',
                    b2world)
    robotB2 = Robot(env, (580, 356), (21*3, 21*3), 90, (0, 255, 122), 'B2',
                    b2world)

    robots = []
    robo_threads = []

    robots.append(robotA1)
    robots.append(robotA2)
    robots.append(robotB1)
    robots.append(robotB2)

    rA1 = imp.load_source('robot1', sys.argv[1] + '/robot1.py')
    robo_threads.append(RoboThread(target=rA1.main, kwargs={'robot': robotA1}))

    rA2 = imp.load_source('robot2', sys.argv[1] + '/robot2.py')
    robo_threads.append(RoboThread(target=rA2.main, kwargs={'robot': robotA2}))

    rB1 = imp.load_source('robot1', sys.argv[2] + '/robot1.py')
    robo_threads.append(RoboThread(target=rB1.main, kwargs={'robot': robotB1}))

    rB2 = imp.load_source('robot2', sys.argv[2] + '/robot2.py')
    robo_threads.append(RoboThread(target=rB2.main, kwargs={'robot': robotB2}))

    ball = Ball(env, (WIDTH//2, HEIGHT//2), (8*3, 8*3), (100, 75, 81),
                (WIDTH, HEIGHT), robots, b2world)

    props = []
    # back
    props.append(BoxProp(env, size=[7, 187], pos=[50, 272], world=b2world))
    props.append(BoxProp(env, size=[7, 187], pos=[675, 272], world=b2world))
    # top
    props.append(BoxProp(env, size=[37, 7], pos=[66, 183], world=b2world))
    props.append(BoxProp(env, size=[37, 7], pos=[660, 183], world=b2world))
    # bottom
    props.append(BoxProp(env, size=[37, 7], pos=[66, 364], world=b2world))
    props.append(BoxProp(env, size=[37, 7], pos=[660, 364], world=b2world))

    # mantinels
    props.append(BoxProp(env, size=[WIDTH, 3], pos=[WIDTH/2, 0],
                         world=b2world))
    props.append(BoxProp(env, size=[WIDTH, 3], pos=[WIDTH/2, HEIGHT],
                         world=b2world))
    props.append(BoxProp(env, size=[3, HEIGHT], pos=[0, HEIGHT/2],
                         world=b2world))
    props.append(BoxProp(env, size=[3, HEIGHT], pos=[WIDTH, HEIGHT/2],
                         world=b2world))

    for robot in robots:
        robot.stop()

    # start robo threads (user specified code for robots)
    for thread in robo_threads:
        thread.start()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
                for robot in robots:
                    robot.event_response(event)
                ball.event_response(event)

        display.fill((0, 86, 27))

        # for better code readability rend is pygame.font.Font.render
        score_image = font.render('{0} : {1}'.format(env.teamAscore,
                                                     env.teamBscore),
                                  True, (255, 255, 255))
        textpos = score_image.get_rect(centerx=WIDTH/2,
                                       centery=HEIGHT+TABLE_HEIGHT/2)
        display.blit(score_image, textpos)

        env.draw_field()
        for robot in robots:
            robot.update()
            robot.draw()

        ball.stay_in()
        ball.draw()

        for prop in props:
            prop.draw()

        b2world.Step(TIME_STEP, 10, 10)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
