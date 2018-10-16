import os
import pygame
from characters import Character, SpriteSheet

# Resource loading:
DATA_PY = os.path.abspath(os.path.dirname(__file__))
WALK_DIR = os.path.normpath(os.path.join(DATA_PY, '', 'sprites/png/walkcycle/'))
BOW_DIR = os.path.normpath(os.path.join(DATA_PY, '', 'sprites/png/bow/'))
HURT_DIR = os.path.normpath(os.path.join(DATA_PY, '', 'sprites/png/hurt/'))
SLASH_DIR = os.path.normpath(os.path.join(DATA_PY, '', 'sprites/png/slash/'))
SPELL_DIR = os.path.normpath(os.path.join(DATA_PY, '', 'sprites/png/spell/'))
THRUST_DIR = os.path.normpath(os.path.join(DATA_PY, '', 'sprites/png/thrust/'))

class HeroPiece(pygame.sprite.DirtySprite):
    def __init__(self, body_part, item):
        pygame.sprite.DirtySprite.__init__(self)
        self.item = item
        self.body_part = body_part
        self.total_frames = 1
        self.frame = 0
        self.direction = 'N'
        self.y = 0
        self.action = 'walk'
        self.change_x = 0
        self.change_y = 0
        self.stop = True
        self.image = self.getImage(body_part, item)
        self.rect = self.image.get_rect()

    def getImage(self, type, item):
        if self.action == 'walk':
            self.total_frames = 9
            directory = WALK_DIR
        elif self.action == 'bow':
            self.total_frames = 13
            directory = BOW_DIR
        elif self.action == 'hurt':
            self.total_frames = 6
            directory = HURT_DIR
        elif self.action == 'slash':
            self.total_frames = 6
            directory = SLASH_DIR
        elif self.action == 'spell':
            self.total_frames = 7
            directory = SPELL_DIR
        elif self.action == 'thrust':
            self.total_frames = 8
            directory = THRUST_DIR

        if self.direction == 'N':
            self.y = 0
        elif self.direction == 'S':
            self.y = 128
        elif self.direction == 'E':
            self.y = 192
        elif self.direction == 'W':
            self.y = 64

        if self.frame >= self.total_frames:
            self.frame = 0

        sprite_sheet = SpriteSheet(os.path.join(directory, f"{type}_{item}.png"))
        return sprite_sheet.get_image(self.frame * 64, self.y, 64, 64)

    def update(self):
        if not self.stop:
            self.image = self.getImage(self.body_part, self.item)
            self.rect.x += self.change_x
            self.rect.y += self.change_y
            self.frame += 1

class Hero(pygame.sprite.LayeredUpdates):
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)
        self.image = pygame.Surface([10, 10])
        self.rect = self.image.get_rect()
        self.action = 'walk'
        self.equipped = dict(
            torso='',
            legs='',
            belt='',
            feet='',
            hands='',
            weapon='',
            behind='',
            head='',
        )
        self.inventory = []
        body = HeroPiece('BODY', 'male')
        torso = HeroPiece('TORSO', 'robe_shirt_brown')
        legs = HeroPiece('LEGS', 'robe_skirt')
        head = HeroPiece('HEAD', 'robe_hood')
        feet = HeroPiece('FEET', 'shoes_brown')
        belt = HeroPiece('BELT', 'rope')
        # weapon = HeroPiece('WEAPON', 'spear')
        self.add(body)
        self.add(torso)
        self.add(legs)
        self.add(head)
        self.add(feet)
        self.add(belt)
        # self.add(weapon)

    def stop_move(self):
        for sprite in self.sprites():
            sprite.stop = True
            sprite.frame  = 0
            sprite.dirty  = 1
        self.update()

    def go_west(self):
        for sprite in self.sprites():
            sprite.direction = 'W'
            sprite.change_x = -3
            sprite.change_y = 0
            sprite.stop = False
        self.update()

    def go_east(self):
        for sprite in self.sprites():
            sprite.direction = 'E'
            sprite.change_x = 3
            sprite.change_y = 0
            sprite.stop = False
        self.update()

    def go_north(self):
        for sprite in self.sprites():
            sprite.direction = 'N'
            sprite.change_x = 0
            sprite.change_y = -3
            sprite.stop = False
        self.update()

    def go_south(self):
        for sprite in self.sprites():
            sprite.direction = 'S'
            sprite.change_x = 0
            sprite.change_y = 3
            sprite.stop = False
        self.update()

    # def addGold(self, x):
    #     if self.gold + x < 0:
    #         self.gold = 0
    #     else:
    #         self.gold += x
    #     return self.gold
