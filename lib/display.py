import os, pygame, yaml
import pygame.freetype

DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/'))
FONT_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/fonts/'))
WALK_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sprites/png/walkcycle/'))
SOUND_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sounds/'))

def close_all_windows():
    windows.update((k,False) for k in windows)

class Item:
    """concerned with item attributes and base images, not with frames or actions"""
    def __init__(self, name):
        with open(os.path.join(DATA_DIR, 'items.yaml'), 'r') as file:
            try:
                data = yaml.load(file)
            except yaml.YAMLError as exc:
                print(exc)

        self.stats = data[name]
        self.sprite_file = os.path.normpath(os.path.join(WALK_DIR, f"{self.stats['file']}.png" ))

    def get_image(self):
        image = pygame.image.load(self.sprite_file)
        return image

    def get_stat(self, stat):
        return self.stats[stat]

class Inventory:
    def __init__(self):
        self.inventory_canvas = pygame.image.load(os.path.join(DATA_DIR, 'images/CharacterScreen.png'))

        self.canvas = pygame.Surface([380,1200])
        self.canvas.fill((255,221,138))
        pygame.freetype.init() # need to initialize font library before use
        self.font = pygame.freetype.Font(os.path.join(FONT_DIR, 'enchanted_land.otf'),30)
        self.running = False

    def get_rect(self):
        return self.canvas.get_rect()

    def run(self):
        self.font.render_to(self.canvas, (0,0), 'My Inventory:', (0,0,0))
        self.running = True
        if self.running:
            with open(os.path.join(DATA_DIR, 'hero.yaml')) as file:
                data = yaml.load(file)

                """draw equipment slots"""
                self.equipped_slots = {}
                self.locations = [(74,148), (148,400), (242,316), (242,148), (158,232), (74,316), (158,148), (158,316), (74,232)]
                i = 0
                for k,v in data['equipped'].items(): # render equipped items or blank slots if nothing equipped
                    if k == 'body':
                        continue
                    elif v != '':
                        self.equipped_slots[self.locations[i]] = {'lookup': v.stats['lookup'], 'body': v.stats['body']}
                        surface = pygame.Surface([64,64])
                        surface.fill((201,145,87))
                        image = pygame.image.load(v.sprite_file)
                        surface.blit(image, (0,0))
                    else:
                        self.equipped_slots[self.locations[i]] = False
                        surface = pygame.Surface([64,64])
                        surface.fill((201,145,87))
                    self.canvas.blit(surface, self.locations[i])
                    i += 1

                """draw inventory slots"""
                self.inventory_slots = {}
                i = 0
                for y in range(0,3):
                    for x in range(0,5):
                        if i < len(data['inventory']):
                            self.inventory_slots[(10+x*74, 484+y*74)] = {'lookup': data['inventory'][i].stats['lookup'], 'body': data['inventory'][i].stats['body'] }
                            surface = pygame.Surface([64,64])
                            surface.fill((201,145,87))
                            image = pygame.image.load(data['inventory'][i].sprite_file)
                            surface.blit(image, (0,0))
                        else:
                            self.inventory_slots[(10+x*74, 484+y*74)] = False
                            surface = pygame.Surface([64,64])
                            surface.fill((201,145,87))
                        # self.canvas.blit(surface, (10+x*74, 484+y*74))
                        self.locations.append((10+x*74, 484+y*74))
                        i += 1

    def handle_click(self, position):
        """equip or unequip items in inventory"""
        if self.running:
            with open(os.path.join(DATA_DIR, 'hero.yaml')) as file:
                data = yaml.load(file)
                for loc in self.locations:
                    if position[0] > loc[0] and position[0] < loc[0] + 64 and position[1] > loc[1] and position[1] < loc[1] + 64:
                        if loc in self.equipped_slots and self.equipped_slots[loc]:
                            if pygame.mixer.get_init():
                                open_inventory_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'equip_item.flac'))
                                open_inventory_sound.play(0)

                            lookup = self.equipped_slots[loc]['lookup']
                            body = self.equipped_slots[loc]['body']

                            if data['equipped'][body]: # check if equipment slot is full
                                data['inventory'].append(Item(lookup)) # if so add that item to inventory
                                data['equipped'][body] = '' # remove item from slot

                        elif loc in self.inventory_slots and self.inventory_slots[loc]:
                            if pygame.mixer.get_init():
                                open_inventory_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'equip_item.flac'))
                                open_inventory_sound.play(0)

                            lookup = self.inventory_slots[loc]['lookup']
                            body = self.inventory_slots[loc]['body']

                            if data['equipped'][body]: # check if equipment slot is full
                                data['inventory'].append(Item(data['equipped'][body].stats['lookup'])) # if so add that item to inventory

                            for item in data['inventory']: # need to remove first occurence of item in data inventory
                                if item.stats['lookup'] == lookup:
                                    data['inventory'].remove(item)
                                    break;
                            data['equipped'][body] = Item(lookup) # replace equipment slot

            with open(os.path.join(DATA_DIR, 'hero.yaml'), 'w') as file:
                try:
                    yaml.dump(data, file, default_flow_style=False)
                except yaml.YAMLError as exc:
                    print(exc)
            self.run() # redraw inventory to update

    def add_item(self, type, item):
        self.inventory.append(Item(type, item))

def quests():
    close_all_windows()
    font = pygame.freetype.Font(os.path.join(FONT_DIR, 'enchanted_land.otf'),115)
    inventory = font.render('My Quests', (0,0,0), (255,221,138))
    return (inventory[0], inventory[1])
