import pygame
import Box2D
import math

from sensors.ir import IRSensor

from robothread import RoboException


class Robot:
    def __init__(self, env, pos, dims, rotation, color, name, b2world,
                 manager):

        self.env = env
        self.dims = dims
        self.rotation = rotation
        self.color = color
        self.radius = (21*3)//2
        self.name = name

        self.default_pos = pos

        self.i = 0

        self.rot_mat = (-math.sin(math.radians(self.rotation)),
                        -math.sin(math.radians(self.rotation)))

        # a dictionary which syncs data between user code process and
        # pygame/Box2D process
        self.data = manager.dict()
        self.data['vec'] = (0, 0)
        self.data['ir'] = 0
        self.data['die'] = False
        self.data['rot_mat'] = self.rot_mat

        self.dragging = False
        self.out = False

        self.vec = (0, 0)

        self.originalImg = pygame.Surface(self.dims, pygame.SRCALPHA, 32)
        self.originalImg.convert_alpha()

        center = [self.dims[0]/2, self.dims[1]/2]

        pygame.draw.circle(self.originalImg, self.color, center, self.radius)
        pygame.draw.circle(self.originalImg, (255, 255, 255),
                           [self.dims[0]/2, self.dims[1]/10],
                           self.dims[1]/5)

        self.image = pygame.transform.rotate(self.originalImg, self.rotation)
        self.rect = pygame.Rect(pos[0], pos[1], 0, 0)

        self.body = b2world.CreateDynamicBody(
            position=(pos[0], pos[1]),
            bullet=True,
            angularDamping=0.3,
            linearDamping=0.15,
            angle=math.radians(self.rotation)
        )

        self.body.CreateCircleFixture(
            radius=self.radius,
            density=10.0,
            friction=0,
            restitution=0.4
        )

        self.body.mass = 100.0

        self.ir_sensor = IRSensor(self, (10, 0))

    def draw(self):
        pos = self.body.worldCenter
        self.rect.left = pos.x
        self.rect.top = pos.y

        rect = pygame.Rect(pos.x - self.radius, pos.y - self.radius, 0, 0)
        self.env.display.blit(self.image, rect)

    def out_of_bounds(self):
        if self.rect.top < 73 or self.rect.left < 73 or \
                self.rect.left > 656 or self.rect.top > 473:
            return True
        return False

    def move_outside(self, team):
        x = 0 + self.radius if team == 'A' else self.env.width - self.radius
        if self.env.robots_out[team] == [True, True]:
            if team == 'A':
                x = self.radius * 3
            else:
                x = self.env.width - self.radius * 3

        self.body.position = Box2D.b2Vec2(x, self.env.height + self.radius)

    def update(self):
        self.i += 1

        vec = (0, 0)
        if not self.out and self.out_of_bounds():
            self.out = True
            self.env.robots_out[self.name[0]][int(self.name[1])-1] = True
            self.dragging = False
            self.move_outside(self.name[0])
            self.terminate()
            self.stop()

            self.data['die'] = False

        if self.i == 9:
            self.i = 0
            self.data['ir'] = self.ir_sensor.read()

        if not self.dragging:
            vec = self.data['vec']
        self.body.linearVelocity = vec

    def mouse_over(self, pos):
        wc = self.body.worldCenter
        dx = wc.x - pos[0]
        dy = wc.y - pos[1]

        return math.sqrt(dx ** 2 + dy ** 2) < self.radius

    def event_response(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.mouse_over(event.pos):
                self.dragging = not self.dragging

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.body.position = Box2D.b2Vec2(event.pos[0], event.pos[1])

    def terminate(self):
        self.data['die'] = True

    def move_to_pos(self, pos):
        self.body.position = Box2D.b2Vec2(pos[0], pos[1])

    def stop(self):
        self.data['vec'] = (0, 0)
