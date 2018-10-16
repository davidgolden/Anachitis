import os, pygame, yaml
import pygame.freetype

DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/'))
FONT_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/fonts/'))
WALK_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sprites/png/walkcycle/'))

windows = {
    'inventory': False,
    'quests': False,
}

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


class ItemSlot:
    def __init__(self, position=(0,0), item=False, width=64, height=64):
        self.item = item
        self.width = width
        self.height = height
        self.x = position[0]
        self.y = position[1]

    def check_if_inside(self, position):
        return position[0] > self.x and position[0] < self.x + self.width and position[1] > self.y and position[1] < self.y + self.height

    def draw(self):
        self.surface = pygame.Surface([64,64])
        self.surface.fill((201,145,87))
        if self.item:
            image = pygame.image.load(self.item.sprite_file)
            self.surface.blit(image, (0,0))
        return self.surface

    def get_item(self):
        """returns tuple of (body part identifier, lookup item name)"""
        return self.item

class Inventory:
    def __init__(self, inventory, equipped):
        self.canvas = pygame.Surface([380,1200])
        self.canvas.fill((255,221,138))
        pygame.freetype.init() # need to initialize font library before use
        self.font = pygame.freetype.Font(os.path.join(FONT_DIR, 'enchanted_land.otf'),30)
        self.inventory = inventory # track actual hero inventory
        self.equipped = equipped # track actual hero equipped

    def get_rect(self):
        return self.canvas.get_rect()

    def open(self):
        close_all_windows()
        self.font.render_to(self.canvas, (0,0), 'My Inventory:', (0,0,0))
        # self.font.render_to(self.canvas, (0,30), f"Gold: {self.hero_stats['gold']}", (0,0,0))

        """draw equipment slots"""
        self.equipped_slots = []
        locations = ((74,148), (148,400), (242,316), (242,148), (158,232), (74,316), (158,148), (158,316), (74,232))
        i = 0
        for k,v in self.equipped.items(): # render equipped items or blank slots if nothing equipped
            if k == 'body':
                continue
            elif v != '':
                slot = ItemSlot(locations[i], self.equipped[k])
                self.equipped_slots.append(slot)
            else:
                slot = ItemSlot(locations[i])
                self.equipped_slots.append(slot)
            self.canvas.blit(slot.draw(), locations[i])
            i += 1

        """draw inventory slots"""
        self.inventory_slots = []
        i = 0
        for y in range(0,3):
            for x in range(0,5):
                if i < len(self.inventory):
                    slot = ItemSlot((10+x*74, 484+y*74), self.inventory[i])
                    self.inventory_slots.append(slot)
                else:
                    slot = ItemSlot()
                    self.inventory_slots.append(slot)
                self.canvas.blit(slot.draw(), (10+x*74, 484+y*74))
                i += 1

        return (self.canvas, (0,0))

    def handle_click(self, position):
        """equip or unequip items in inventory"""
        for slot in self.equipped_slots:
            if slot.check_if_inside(position):
                print(slot.get_item())
        for slot in self.inventory_slots:
            if slot.check_if_inside(position):
                item = slot.get_item() # returns item object from slot
                self.inventory.pop(self.inventory.index(item)) #remove item from inventory
                if self.equipped[item.stats['body']]: # check if equipment slot is full
                    self.inventory.append(self.equipped[item.stats['body']]) # if so add that item to inventory
                self.equipped[item.stats['body']] = item # replace equipment slot

                hero_data = {}
                with open(os.path.join(DATA_DIR, 'hero.yaml'), 'r') as file:
                    try:
                        hero_data = yaml.load(file)
                    except yaml.YAMLError as exc:
                        print(exc)
                hero_data['equipped'] = self.equipped
                hero_data['inventory'] = self.inventory
                with open(os.path.join(DATA_DIR, 'hero.yaml'), 'w') as file:
                    try:
                        yaml.dump(hero_data, file, default_flow_style=False)
                    except yaml.YAMLError as exc:
                        print(exc)

    # def remove_item(self, item):
    #     """accepts lookup item name"""
    #     for item in self.inventory_slots:
    #         if item.stats['lookup'] == item:
    #             print(self.inventory.index(item))

    def add_item(self, type, item):
        self.inventory.append(Item(type, item))

def quests():
    close_all_windows()
    font = pygame.freetype.Font(os.path.join(FONT_DIR, 'enchanted_land.otf'),115)
    inventory = font.render('My Quests', (0,0,0), (255,221,138))
    return (inventory[0], inventory[1])

# inventory = Inventory()
