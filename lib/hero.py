import os, pygame, yaml
from display import Inventory, Item

# Resource loading:
DATA_PY = os.path.abspath(os.path.dirname(__file__))
WALK_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sprites/png/walkcycle/'))
BOW_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sprites/png/bow/'))
HURT_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sprites/png/hurt/'))
SLASH_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sprites/png/slash/'))
SPELL_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sprites/png/spell/'))
THRUST_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sprites/png/thrust/'))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/'))
FONT_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/fonts/'))

class Hero(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)

        self.action_data = {
            'walk': {
                'total_frames': 9,
                'directory': WALK_DIR
            },
            'bow': {
                'total_frames': 13,
                'directory': BOW_DIR
            },
            'hurt': {
                'total_frames': 6,
                'directory': HURT_DIR
            },
            'slash': {
                'total_frames': 6,
                'directory': SLASH_DIR
            },
            'spell': {
                'total_frames': 7,
                'directory': SPELL_DIR
            },
            'thrust': {
                'total_frames': 8,
                'directory': THRUST_DIR
            },
        }

        self.action = 'walk'
        self.change_x = 0
        self.change_y = 0
        self.frame = 0
        self.direction = 'S'
        self.y = 144
        self.stop = True

        self.__updateSpriteFiles()
        self.__paintSprite()
        self.rect = self.image.get_rect()

        self.mask = pygame.mask.from_surface(self.image)
        self.mask.fill()

    def __paintSprite(self):
        """updates self.image with ordered surface of blits corresponding to those listed in self.equipped"""
        if self.frame >= self.action_data[self.action]['total_frames']:
            self.frame = 0
        canvas = pygame.Surface([32,48], pygame.SRCALPHA) # build surface
        image_list = []
        area = (-self.frame * 64 - 16, -self.y, 32, 48)

        with open(os.path.join(DATA_DIR, 'hero.yaml')) as file:
            data = yaml.load(file)
            for k,v in data['equipped'].items():
                if v: # iterate over equipped items and if value is truthy, load correct file and append image_list
                    image_list.append((self.image_files[k].convert_alpha(), pygame.Rect(area)))

        canvas.blits(image_list) # return surface blitted with images
        self.image = canvas.convert_alpha()

    def __updateSpriteFiles(self):
        """load new image files based on what is equipped. needs to be run on instantiation and on every equipment update"""
        with open(os.path.join(DATA_DIR, 'hero.yaml')) as file:
            data = yaml.load(file)
            self.image_files = { k: pygame.image.load(os.path.join(self.action_data[self.action]['directory'], f"{v.get_stat('file')}.png")) for (k,v) in data['equipped'].items() if v }

    def update(self, deg):
        # determine y value of sprite list
        if not self.stop:
            if deg > -45 and deg < 45:
                self.direction = 'E'
                self.y = 208
            if deg > 45 and deg < 135:
                self.direction = 'S'
                self.y = 144
            if (deg > 135 and deg < 180) or (deg > -180 and deg < -135):
                self.direction = 'W'
                self.y = 80
            if deg > -135 and deg < -45:
                self.direction = 'N'
                self.y = 16

            self.__paintSprite()
            self.frame += 1
        else:
            self.stop_move()

    def repaintSprite(self):
        self.__updateSpriteFiles()
        self.__paintSprite()

    def stop_move(self):
        self.stop = True
        self.frame = 0
        self.dirty = 1
        self.__paintSprite()

    def update_stat(self, stat, new_value):
        with open(os.path.join(DATA_DIR, 'hero.yaml')) as file:
            data = yaml.load(file)
            data['stats'][stat] = new_value
        with open(os.path.join(DATA_DIR, 'herlo.yaml'), 'w') as file:
            try:
                yaml.dump(data, file, default_flow_style=False)
            except yaml.YAMLError as exc:
                print(exc)
