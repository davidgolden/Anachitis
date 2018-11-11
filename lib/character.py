import pygame, os
from display import DialogBox

DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/'))

WALK_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sprites/png/walkcycle/'))

class Character(pygame.sprite.Sprite):
    def __init__(self, sprite_data):
        pygame.sprite.DirtySprite.__init__(self)
        self.change_x = 0
        self.change_y = 0
        self.direction = 'S'
        self.stop = True
        self.frame = 0

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

        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()

    def highlight(self):
        self.__paintSprite(True)

    def __paintSprite(self, highlight=False):
        """updates self.image with ordered surface of blits corresponding to those listed in self.equipped"""
        if self.frame >= self.frames:
            self.frame = 0

        canvas = pygame.Surface([32,48], pygame.SRCALPHA) # build surface
        area = (-self.frame * 64 - 16, -self.y, 32, 48)

        self.image = pygame.image.load(os.path.join(WALK_DIR, 'BODY_oldman.png'))

        if not highlight:
            canvas.blit(self.image, pygame.Rect(area))
        else:
            canvas.blit(self.image, pygame.Rect(area), None, pygame.BLEND_ADD)

        # canvas.set_colorkey((0,0,0))
        # self.image = canvas.convert_alpha()

    # def update(self, deg):
        # determine y value of sprite list
        # if not self.stop:
        #     if deg > -45 and deg < 45:
        #         self.direction = 'E'
        #         self.y = 192
        #     if deg > 45 and deg < 135:
        #         self.direction = 'S'
        #         self.y = 128
        #     if (deg > 135 and deg < 180) or (deg > -180 and deg < -135):
        #         self.direction = 'W'
        #         self.y = 64
        #     if deg > -135 and deg < -45:
        #         self.direction = 'N'
        #         self.y = 0
        #
        #     self.__paintSprite()
        #     self.frame += 1
        # else:
        #     self.stop_move()

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
        Character.__init__(self, sprite_data)
        self.name = sprite_data.get('name', '')
        self.dialog = sprite_data.get('dialog', '')
        print(self.dialog)

    def click_action(self):
        """Default action to take if sprite is clicked"""
        dialog_box = DialogBox((400,400), self.dialog)
        return dialog_box.render()
