import pygame
import Box2D

class BoxProp:
    def __init__(self, env, pars, b2world):
        # static rectangle shaped prop
        # pars:
        # size - array [width, height]
        # position - array [x, y], in world meters, of center

        self.env = env
        self.size = pars['size']
        self.pos = pars['position']

        # initialize body
        bdef = Box2D.b2BodyDef()
        bdef.position = Box2D.b2Vec2(self.pos[0], self.pos[1])
        bdef.angle = 0
        bdef.fixedRotation = True
        self.body = b2world.CreateBody(bdef)
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

        # initialize shape
        fixdef = Box2D.b2FixtureDef()
        fixdef.shape = Box2D.b2PolygonShape()
        fixdef.shape.SetAsBox(self.size[0]/2, self.size[1]/2)
        fixdef.restitution = 0.4
        self.body.CreateFixture(fixdef)

    def draw(self):
        # just to see where it is
        pygame.draw.rect(self.env.display, (255, 0, 0), self.rect)
