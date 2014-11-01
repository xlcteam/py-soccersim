import pygame
import Box2D


class Ball:
    def __init__(self, env, pos, dims, color, field, b2world):
        self.env = env
        self.dims = dims
        self.color = color
        self.rect = pygame.Rect(pos[0], pos[1], 0, 0)
        self.radius = dims[0] // 2
        self.field = field

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

        self.neutral_spots = { "topleft" : [224, 185],
                               "topright": [503, 185],
                               "bottomleft": [224, 363],
                               "bottomright": [503, 363],
                               "center": [self.field[0]//2,
                                          self.field[1]//2]
                            }

        self.following_spots = {
            "topleft" : ["topleft", "bottomleft", "center", 
                        "topright", "bottomright"],
            "topright": ["topright", "bottomright", "center", 
                        "topleft", "bottomleft"],
            "bottomleft": ["bottomleft", "topleft", "center", 
                        "bottomright", "topright"],
            "bottomright": ["bottomright", "topright", "center", 
                        "bottomleft", "topleft"]}

    def draw(self):
        pos = self.body.worldCenter
        rect = pygame.Rect(pos.x - self.radius, pos.y - self.radius, 0, 0)
        self.env.display.blit(self.image, rect)
