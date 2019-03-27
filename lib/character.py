import pygame, os, random, math, time
from display import DialogBox

DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/'))
SPRITE_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sprites/'))


class Character(pygame.sprite.Sprite):
    def __init__(self, sprite_data):
        pygame.sprite.Sprite.__init__(self)
        self.change_x = 0
        self.change_y = 0
        self.direction = 'S'
        self.stop = True
        self.frame = 0

        pos = sprite_data.attrib.get('location').split(',')
        self.position = (pos[0], pos[1])

        wrd = sprite_data.attrib.get('wander').split(',')
        self.wander_rect = pygame.Rect(int(wrd[0]), int(wrd[1]), int(wrd[2]), int(wrd[3]))

        self.wandering = False
        self.idle = 0

        self.name = sprite_data.attrib.get('name', '')
        self.file_path = sprite_data.attrib.get('file_path')
        self.static = sprite_data.attrib.get('static', True)

        self.frames = int(sprite_data.attrib.get('frames', 1))

        self.x = int(sprite_data.attrib.get('x', 0))
        self.y = int(sprite_data.attrib.get('y', 0))
        self.width = int(sprite_data.attrib.get('width', 64))
        self.height = int(sprite_data.attrib.get('height', 64))

        # self.dialog = sprite_data.get('dialog', '')

        self.__paintSprite()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = int(self.position[0]), int(self.position[1])
        self.dest_x, self.dest_y = self.rect.x, self.rect.y

        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()
        self.highlighted = False

    def collidepoint(self, pos):
        if self.rect.collidepoint((pos[0], pos[1])):
            return True
        return False

    def __paintSprite(self):
        """updates self.image with ordered surface of blits corresponding to those listed in self.equipped"""
        if self.frame >= self.frames:
            self.frame = 0

        canvas = pygame.Surface([self.width, self.height], pygame.SRCALPHA)  # build surface

        area = (-self.frame * self.width, -self.y, self.width, self.height)

        self.image_file = pygame.image.load(os.path.join(SPRITE_DIR, self.file_path)).convert_alpha()

        if not self.highlighted:
            canvas.blit(self.image_file, pygame.Rect(area))
        else:
            self.image_file.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
            canvas.blit(self.image_file, pygame.Rect(area))

        self.image = canvas

        # canvas.set_colorkey((0,0,0))
        # self.image = canvas.convert_alpha()

    def go_to_destination(self):
        self.wandering = True
        self.dest_x = random.randint(self.wander_rect.x - self.wander_rect.width, self.wander_rect.x)
        self.dest_y = random.randint(self.wander_rect.y - self.wander_rect.height, self.wander_rect.y)

        dx = self.dest_x - self.rect.x  # this is difference between mouse position and character location
        dy = self.dest_y - self.rect.y
        angle = math.atan2(dy, dx)

        self.deg = round(math.degrees(angle))
        speed = 5

        cos = speed * math.cos(angle)
        sin = speed * math.sin(angle)

        self.change_x = round(cos)
        self.change_y = round(sin)

    def check_collisions(self):
        """check if sprite collides with bounding wander_rect or other blockers
        should return true if a collision occurs and false if not"""
        t = 15  # tolerance
        if pygame.Rect(self.dest_x, self.dest_y, t, t).colliderect(pygame.Rect(self.rect.x, self.rect.y, t, t)):
            return True  # if arrived at destination, stop
        elif self.wander_rect.contains(pygame.Rect(self.rect.x, self.rect.y, t, t)):
            return True  # if wander_rect no longer contains self, stop
        return False

    def update(self, pos=None):
        # determine y value of sprite list
        self.__paintSprite()

        if pos:  # position is present when hero is moving
            self.rect.move_ip(pos[0], pos[1])
            self.wander_rect.move_ip(pos[0], pos[1])

        if self.wandering and not self.check_collisions():
            self.wandering = False
        elif not self.wandering and self.wander_rect:  # check for wander_rect to control for static sprites
            self.go_to_destination()

        if self.wandering and self.deg:
            self.rect.x += self.change_x
            self.rect.y += self.change_y

            if self.deg > -45 and self.deg < 45:
                self.direction = 'E'
                self.y = 192
            elif self.deg > 45 and self.deg < 135:
                self.direction = 'S'
                self.y = 128
            elif (self.deg > 135 and self.deg < 180) or (self.deg > -180 and self.deg < -135):
                self.direction = 'W'
                self.y = 64
            elif self.deg > -135 and self.deg < -45:
                self.direction = 'N'
                self.y = 0

            self.frame += 1
        else:
            self.stop_move()

    def stop_move(self):
        self.stop = True
        self.frame = 0
        self.__paintSprite()

class NPC(Character):
    def __init__(self, sprite_data):
        self.highlighted = False
        Character.__init__(self, sprite_data)

        self.name = sprite_data.get('name', '')
        self.dialog = sprite_data.findall('dialog')

    def click_action(self):
        """Default action to take if sprite is clicked"""
        dialog_box = DialogBox((400, 400), self.dialog)
        return dialog_box.render()

class Enemy(Character):
    def __init__(self, sprite_data):
        self.highlighted = False
        Character.__init__(self, sprite_data)

        self.name = sprite_data.get('name', '')

    def click_action(self):
        """Default action to take if sprite is clicked"""
        pass
