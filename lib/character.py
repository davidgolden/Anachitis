import pygame, os, random, math
from display import DialogBox

DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/'))
WALK_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sprites/png/walkcycle/'))


class Character(pygame.sprite.Sprite):
    def __init__(self, sprite_data):
        pygame.sprite.Sprite.__init__(self)
        self.change_x = 0
        self.change_y = 0
        self.direction = 'S'
        self.stop = True
        self.frame = 0
        self.position = sprite_data.get('location', (0, 0))
        self.wander_rect = sprite_data.get('wander', False)

        self.wandering = False

        self.name = sprite_data.get('name', '')
        # self.file_path = sprite_data.get('file_path', ''),
        self.file_path = sprite_data['file_path']
        self.static = sprite_data.get('static', True)
        self.x = sprite_data.get('x', 0)
        self.y = sprite_data.get('y', 0)
        self.frames = sprite_data.get('frames', 1)
        self.dialog = sprite_data.get('dialog', '')

        self.__paintSprite()

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.position[0], self.position[1]
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

        canvas = pygame.Surface([32, 48], pygame.SRCALPHA)  # build surface

        area = (-self.frame * 64 - 16, -self.y, 32, 48)
        self.image_file = pygame.image.load(os.path.join(WALK_DIR, 'BODY_oldman.png')).convert_alpha()

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
        if self.wander_rect.contains(pygame.Rect(self.rect.x, self.rect.y, t, t)):
            return True  # if wander_rect no longer contains self, stop
        return False

    def update(self, pos=None):
        # determine y value of sprite list
        self.__paintSprite()

        if pos:
            self.rect.move_ip(pos[0], pos[1])
            self.wander_rect.move_ip(pos[0], pos[1])

        if self.wandering and not self.check_collisions():
            self.wandering = False
        elif not self.wandering:
            self.go_to_destination()

        if self.wandering:
            self.rect.x += self.change_x
            self.rect.y += self.change_y

            if self.deg > -45 and self.deg < 45:
                self.direction = 'E'
                self.y = 208
            if self.deg > 45 and self.deg < 135:
                self.direction = 'S'
                self.y = 144
            if (self.deg > 135 and self.deg < 180) or (self.deg > -180 and self.deg < -135):
                self.direction = 'W'
                self.y = 80
            if self.deg > -135 and self.deg < -45:
                self.direction = 'N'
                self.y = 16

            self.frame += 1
        else:
            self.stop_move()

    def stop_move(self):
        self.stop = True
        self.frame = 0
        # self.dirty = 1
        self.__paintSprite()

    # def update_stat(self, stat, new_value):
    #     with open(os.path.join(DATA_DIR, 'hero.yaml')) as file:
    #         data = yaml.load(file)
    #         data['stats'][stat] = new_value
    #     with open(os.path.join(DATA_DIR, 'herlo.yaml'), 'w') as file:
    #         try:
    #             yaml.dump(data, file, default_flow_style=False)
    #         except yaml.YAMLError as exc:
    #             print(exc)


class NPC(Character):
    def __init__(self, sprite_data):
        self.highlighted = False
        Character.__init__(self, sprite_data)

        self.name = sprite_data.get('name', '')
        self.dialog = sprite_data.get('dialog', '')

    def click_action(self):
        """Default action to take if sprite is clicked"""
        dialog_box = DialogBox((400, 400), self.dialog)
        return dialog_box.render()
