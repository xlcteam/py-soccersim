import pygame
import Box2D
import math

from sensors.ir import IRSensor

from robothread import RoboException


class Robot:
    def __init__(self, env, pos, dims, rotation, color, name, b2world):

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

        self.dragging = False
        self.out = False

        self.original_img = pygame.Surface(self.dims, pygame.SRCALPHA, 32)
        self.original_img.convert_alpha()

        center = [self.dims[0]/2, self.dims[1]/2]

        pygame.draw.circle(self.original_img, self.color, center, self.radius)
        pygame.draw.circle(self.original_img, (255, 255, 255),
                           [self.dims[0]/2, self.dims[1]/10],
                           self.dims[1]/5)

        self.image = pygame.transform.rotate(self.original_img, self.rotation)
        self.rect = pygame.Rect(pos[0], pos[1], 0, 0)

        self.body = b2world.CreateDynamicBody(
            position=(pos[0], pos[1]),
            bullet=True,
            angularDamping=0.1,
            linearDamping=0.05,
            angle=math.radians(self.rotation)
        )

        self.body.CreateCircleFixture(
            radius=self.radius,
            density=5.0,
            friction=0,
            restitution=0.5
        )

        self.body.mass = 100.0

        self.ir_sensor = IRSensor(self, (10, 0))

        self.vec = (0, 0)

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
            self.stop()

        if not self.dragging:
            vec = self.vec
        self.body.linearVelocity = vec

    def sense(self):
        pass

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

    def move_to_pos(self, pos):
        self.body.position = Box2D.b2Vec2(pos[0], pos[1])

    def stop(self):
        self.vec = (0, 0)

    def forward(self, speed):
        self.vec = (speed, 0)
        self.rotatize()

    def reverse(self, speed):
        self.vec = (-speed, 0)
        self.rotatize()

    def left(self, speed):
        self.vec = (0, speed)
        self.rotatize()

    def right(self, speed):
        self.vec = (0, -speed)
        self.rotatize()

    def forward_left(self, speed):
        self.vec = (speed/math.sqrt(2), -(speed/(math.sqrt(2))))
        self.rotatize()

    def forward_right(self, speed):
        self.vec = (speed/math.sqrt(2), (speed/(math.sqrt(2))))
        self.rotatize()

    def reverse_left(self, speed):
        self.vec = (-(speed/math.sqrt(2)), -(speed/(math.sqrt(2))))
        self.rotatize()

    def reverse_right(self, speed):
        self.vec = (-(speed/math.sqrt(2)), (speed/(math.sqrt(2))))
        self.rotatize()

    def rotatize(self):
        self.vec = (self.vec[0] * self.rot_mat[0],
                    self.vec[1] * self.rot_mat[1])
