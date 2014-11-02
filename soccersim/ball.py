import pygame
import Box2D
import math


class Ball:
    def __init__(self, env, pos, dims, color, field, robots, b2world):
        self.env = env
        self.dims = dims
        self.color = color
        self.rect = pygame.Rect(pos[0], pos[1], 0, 0)
        self.radius = dims[0] // 2
        self.field = field
        self.robots = robots
        self.dragging = False

        self.image = pygame.Surface(self.dims, pygame.SRCALPHA, 32)
        self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color,
                           [self.dims[0]//2, self.dims[1]//2],
                           self.radius)

        self.body = b2world.CreateDynamicBody(
            position=(pos[0], pos[1]),
            bullet=True,
            angularDamping=0.3,
            linearDamping=0.15
        )

        self.body.CreateCircleFixture(
            radius=self.radius,
            density=1.0,
            friction=0.3,
            restitution=0.4,
        )

        self.neutral_spots = {
            "topleft": [224, 185],
            "topright": [503, 185],
            "bottomleft": [224, 363],
            "bottomright": [503, 363],
            "center": [self.field[0]//2,
                       self.field[1]//2]
        }

        self.following_spots = {
            "topleft": ["topleft", "bottomleft", "center",
                        "topright", "bottomright"],
            "topright": ["topright", "bottomright", "center",
                         "topleft", "bottomleft"],
            "bottomleft": ["bottomleft", "topleft", "center",
                           "bottomright", "topright"],
            "bottomright": ["bottomright", "topright", "center",
                            "bottomleft", "topleft"]}

    def draw(self):
        pos = self.body.worldCenter
        self.rect.left = pos.x
        self.rect.top = pos.y

        rect = pygame.Rect(pos.x - self.radius, pos.y - self.radius, 0, 0)
        self.env.display.blit(self.image, rect)

    def move_to_uns(self, spot):
        self.body.position = Box2D.b2Vec2(self.neutral_spots[spot][0],
                                        self.neutral_spots[spot][1])
        self.body.linearVelocity = (0, 0)

    def occupied(self, spot):
        """Return true/false whether the spot is occupied"""
        for robot in self.robots:
            dx = self.neutral_spots[spot][0] - robot.rect.left
            dy = self.neutral_spots[spot][1] - robot.rect.top
            if math.sqrt(dx*dx+dy*dy) < robot.radius + self.radius:
                return True

        return False

    def check_uns(self):
        self.dragging = False

        side = "top" if self.rect.top < self.field[1]/2 else "bottom"
        side += "left" if self.rect.left < self.field[0]/2 else "right"

        for spot in self.following_spots[side]:
            if not self.occupied(spot):
                self.move_to_uns(spot)
                return

    def ball_outside(self):
        if self.rect.top < 73 or self.rect.left < 73:
            return True
        elif self.rect.left > 656 or self.rect.top > 473:
            return True

        return False

    def stay_in(self):
        if self.ball_outside():
            self.check_uns()

    def mouse_over(self, pos):
        dx = self.rect.left - pos[0]
        dy = self.rect.top - pos[1]

        return math.sqrt(dx*dx+dy*dy) < self.radius

    def event_response(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.mouse_over(event.pos):
                self.dragging = not self.dragging

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.body.position = Box2D.b2Vec2(event.pos[0], event.pos[1])
