import os, pygame, yaml, asyncio
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

action_data = {
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

class Hero(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.load() # load equipped, inventory, and stats

        # SAVE THIS IN CASE YOU STUIPDLY DELETE YOUR DATA!!!
        # self.equipped = {
        #     'behind': '',
        #     'body': Item('body'),
        #     'feet': '',
        #     'legs': Item('plate_legs'),
        #     'torso': Item('purple_armor'),
        #     'belt': '',
        #     'head': Item('hair_blonde'),
        #     'hands': '',
        #     'weapon': '',
        # }
        # self.inventory = []
        # self.stats = {
        #     'gold': 50
        # }

        self.inventory = Inventory(self.inventory, self.equipped)

        # asyncio.run(self.updateLoop(), debug=True)
        # print('hello')
        # myQueue = asyncio.Queue(loop=loop)
        # loop.run_until_complete(self.updateLoop(myQueue))
        # myQueue = asyncio.Queue()
        # self.updateLoop()

        # asyncio.create_task(self.__retrieveInventory())

        # loop.run_until_complete(self.main(loop))
        # loop.close()

        self.action = 'walk'
        self.change_x = 0
        self.change_y = 0
        self.frame = 0
        self.direction = 'S'
        self.y = 128
        self.stop = True

        self.__updateSpriteFiles()
        self.__paintSprite()
        self.rect = self.image.get_rect()

    # async def updateLoop(self):
    #     await asyncio.sleep(1)
    #     task = asyncio.create_task(self.__retrieveInventory())
        # while True:
        #     task = asyncio.create_task(self.__retrieveInventory())
            # await task
            # task.cancel()
            # print('task done')
            # await asyncio.sleep(1)

    def retrieveInventory(self):
        with open(os.path.join(DATA_DIR, 'hero.yaml')) as file:
            data = yaml.load(file)
            self.inventory = Inventory(data['inventory'], data['equipped'])
            print('got inventory')

    def __paintSprite(self):
        """updates self.image with ordered surface of blits corresponding to those listed in self.equipped"""
        if self.frame >= action_data[self.action]['total_frames']:
            self.frame = 0
        canvas = pygame.Surface([64,64]).convert() # build surface
        image_list = []
        area = (-self.frame * 64, -self.y, 64, 64)
        for k,v in self.equipped.items():
            if v: # iterate over equipped items and if value is truthy, load correct file and append image_list
                image_list.append((self.image_files[k], pygame.Rect(area)))

        canvas.blits(image_list) # return surface blitted with images
        canvas.set_colorkey((0,0,0))
        self.image = canvas

    def __updateSpriteFiles(self):
        """load new image files based on what is equipped. needs to be run on instantiation and on every equipment update"""
        self.image_files = { k: pygame.image.load(os.path.join(action_data[self.action]['directory'], f"{v.get_stat('file')}.png")) for (k,v) in self.equipped.items() if v }

    def update(self):
        # determine y value of sprite list
        if not self.stop:
            if self.direction == 'N':
                self.y = 0
            elif self.direction == 'S':
                self.y = 128
            elif self.direction == 'E':
                self.y = 192
            elif self.direction == 'W':
                self.y = 64

            self.__paintSprite()

            self.rect.x += self.change_x
            self.rect.y += self.change_y
            self.frame += 1
        else:
            self.stop_move()

    def save(self):
        to_save = {
            'equipped': self.equipped,
            'inventory': self.inventory.inventory,
            'stats': self.stats,
        }
        with open(os.path.join(DATA_DIR, 'hero.yaml'), 'w') as file:
            try:
                yaml.dump(to_save, file, default_flow_style=False)
            except yaml.YAMLError as exc:
                print(exc)

    def load(self):
        with open(os.path.join(DATA_DIR, 'hero.yaml'), 'r') as file:
            try:
                data = yaml.load(file)
                self.equipped = data['equipped']
                self.inventory = data['inventory']
                self.stats = data['stats']
            except yaml.YAMLError as exc:
                print(exc)

    def add_item(self, item):
        self.inventory.append(Item(item))

    def equip(self, body, item):
        self.equipped[body] = Item(item)
        self.__updateSpriteFiles()

    def stop_move(self):
        self.stop = True
        self.frame = 0
        self.dirty = 1

    def start_move(self, dir):
        if dir == 'N':
            self.direction = 'N'
            self.change_x = 0
            self.change_y = -3
        elif dir == 'S':
            self.direction = 'S'
            self.change_x = 0
            self.change_y = 3
        elif dir == 'W':
            self.direction = 'W'
            self.change_x = -3
            self.change_y = 0
        elif dir == 'E':
            self.direction = 'E'
            self.change_x = 3
            self.change_y = 0

    def add_gold(self, x):
        if self.stats['gold'] + x < 0:
            self.stats['gold'] = 0
        else:
            self.stats['gold'] += x
        self.save()
        return self.stats['gold']
