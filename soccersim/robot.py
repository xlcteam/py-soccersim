import pygame
import Box2D
import math


class Robot:
    def __init__(self, env, pos, dims, rotation, color, b2world):
        self.env = env
        self.dims = dims
        self.rotation = rotation
        self.color = color
        self.radius = (21*3)//2

        self.dragging = False

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
            density=1.0,
            friction=0.3,
            restitution=0.4
        )

    def draw(self):
        pos = self.body.worldCenter
        self.rect.left = pos.x
        self.rect.top = pos.y

        rect = pygame.Rect(pos.x - self.radius, pos.y - self.radius, 0, 0)
        self.env.display.blit(self.image, rect)

    def update(self):
        vec = (0, 0)
        if not self.dragging:
            vec = self.vec
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
            vec = Box2D.b2Vec2(event.pos[0], event.pos[1])
            # self.body.SetPosition(vec) # doesnt work...
