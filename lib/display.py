import os, pygame, yaml
import pygame.freetype

DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/'))
IMAGE_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/images/'))
FONT_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/fonts/'))
WALK_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sprites/png/walkcycle/'))
SOUND_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sounds/'))


class AllWindows:
    """AllWindows tracks Window instances"""

    def __init__(self):
        self.windows = []

    def __len__(self):
        return len(self.windows)

    def add_window(self, window):
        self.windows.append(window)

    def remove_window(self):
        self.windows = []

    def draw(self, surface):
        if self.windows:
            for window in self.windows:
                surface.blit(window.render(), window.origin)


active_windows = AllWindows()


class Window:
    def __init__(self, primary_surface, origin):
        self.surface = primary_surface
        self.rect = primary_surface.get_rect()
        self.button_list = []
        self.origin = origin
        self.selection = None

    def add_button(self, button, pos):
        button.rect.x = pos[0] + self.origin[0]
        button.rect.y = pos[1] + self.origin[1]
        button.pos = pos
        self.button_list.append(button)
        self.surface.blit(button.surface, pos)

    def remove_button(self, button):
        for b in self.button_list:
            if b == button:
                self.button_list.remove(b)

    def render(self):
        return self.surface

    def collide_buttons(self, pos):
        if self.button_list:
            for button in self.button_list:
                if button.rect.collidepoint(pos):
                    button.on_hover()
                    return self.surface.blit(button.surface, button.pos)
        return False

    def esc_buttons(self):
        for button in self.button_list:
            button.on_esc_hover()
            self.surface.blit(button.surface, button.pos)

    def click_button(self, pos):
        print('click button called')
        if self.button_list:
            for button in self.button_list:
                if button.rect.collidepoint(pos):
                    return button.on_click()
        return False


class Button:
    def __init__(self, bounds, action):
        self.bounds = bounds
        self.action = action
        self.surface = pygame.Surface((bounds.width, bounds.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.pos = (0, 0)

    def on_click(self):
        self.action()


class TextButton(Button):
    def __init__(self, bounds, action, option, font):
        Button.__init__(self, bounds, action)
        self.font = font
        self.option = option

        font.render_to(self.surface, (0, bounds.height), self.option.text)

        self.hovering = False

    def render_text_button(self, text, surface, pos, fgcolor, bgcolor=(219, 191, 123)):
        self.font.render_to(surface, pos, text, fgcolor, bgcolor)

    def on_hover(self):
        if not self.hovering:
            self.render_text_button(self.option.text, self.surface, (0, self.bounds.height), (255, 255, 255))
            self.hovering = True

    def on_esc_hover(self):
        if self.hovering:
            self.render_text_button(self.option.text, self.surface, (0, self.bounds.height), (0, 0, 0))
            self.hovering = False

    def on_click(self):
        if self.option.get('action'):
            self.action(self.option.get('action'))


class ImageButton(Button):
    def __init__(self, bounds, action, image, esc_image=None):
        Button.__init__(self, bounds, action)
        self.image = image
        self.esc_image = esc_image
        self.hovering = False
        self.surface.blit(self.image, (0, 0))

    def on_hover(self):
        if not self.hovering:
            self.surface.blit(self.esc_image, (0, 0))
            self.hovering = True

    def on_esc_hover(self):
        if self.hovering:
            if self.esc_image:
                self.surface.blit(self.image, (0, 0))
            self.hovering = False


class Item:
    """concerned with item attributes and base images, not with frames or actions"""

    def __init__(self, name):
        with open(os.path.join(DATA_DIR, 'items.yaml'), 'r') as file:
            try:
                data = yaml.load(file)
            except yaml.YAMLError as exc:
                print(exc)

        self.stats = data[name]
        self.sprite_file = os.path.normpath(os.path.join(WALK_DIR, f"{self.stats['file']}.png"))

    def get_image(self):
        image = pygame.image.load(self.sprite_file)
        return image

    def get_stat(self, stat):
        return self.stats[stat]


class Inventory:
    def __init__(self):
        self.inventory_canvas = pygame.image.load(os.path.join(DATA_DIR, 'images/CharacterScreen.png'))

        self.canvas = pygame.Surface([380, 1200])
        self.canvas.fill((255, 221, 138))
        pygame.freetype.init()  # need to initialize font library before use
        self.font = pygame.freetype.Font(os.path.join(FONT_DIR, 'enchanted_land.otf'), 30)
        self.running = False

    def get_rect(self):
        return self.canvas.get_rect()

    def run(self):
        self.font.render_to(self.canvas, (0, 0), 'My Inventory:', (0, 0, 0))
        self.running = True
        if self.running:
            with open(os.path.join(DATA_DIR, 'hero.yaml')) as file:
                data = yaml.load(file)

                """draw equipment slots"""
                self.equipped_slots = {}
                self.locations = [(74, 148), (148, 400), (242, 316), (242, 148), (158, 232), (74, 316), (158, 148),
                                  (158, 316), (74, 232)]
                i = 0
                for k, v in data['equipped'].items():  # render equipped items or blank slots if nothing equipped
                    if k == 'body':
                        continue
                    elif v != '':
                        self.equipped_slots[self.locations[i]] = {'lookup': v.stats['lookup'], 'body': v.stats['body']}
                        surface = pygame.Surface([64, 64])
                        surface.fill((201, 145, 87))
                        image = pygame.image.load(v.sprite_file)
                        surface.blit(image, (0, 0))
                    else:
                        self.equipped_slots[self.locations[i]] = False
                        surface = pygame.Surface([64, 64])
                        surface.fill((201, 145, 87))
                    self.canvas.blit(surface, self.locations[i])
                    i += 1

                """draw inventory slots"""
                self.inventory_slots = {}
                i = 0
                for y in range(0, 3):
                    for x in range(0, 5):
                        if i < len(data['inventory']):
                            self.inventory_slots[(10 + x * 74, 484 + y * 74)] = {
                                'lookup': data['inventory'][i].stats['lookup'],
                                'body': data['inventory'][i].stats['body']}
                            surface = pygame.Surface([64, 64])
                            surface.fill((201, 145, 87))
                            image = pygame.image.load(data['inventory'][i].sprite_file)
                            surface.blit(image, (0, 0))
                        else:
                            self.inventory_slots[(10 + x * 74, 484 + y * 74)] = False
                            surface = pygame.Surface([64, 64])
                            surface.fill((201, 145, 87))
                        # self.canvas.blit(surface, (10+x*74, 484+y*74))
                        self.locations.append((10 + x * 74, 484 + y * 74))
                        i += 1

    def handle_click(self, position):
        """equip or unequip items in inventory"""
        if self.running:
            with open(os.path.join(DATA_DIR, 'hero.yaml')) as file:
                data = yaml.load(file)
                for loc in self.locations:
                    if position[0] > loc[0] and position[0] < loc[0] + 64 and position[1] > loc[1] and position[1] < \
                            loc[1] + 64:
                        if loc in self.equipped_slots and self.equipped_slots[loc]:
                            if pygame.mixer.get_init():
                                open_inventory_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'equip_item.flac'))
                                open_inventory_sound.play(0)

                            lookup = self.equipped_slots[loc]['lookup']
                            body = self.equipped_slots[loc]['body']

                            if data['equipped'][body]:  # check if equipment slot is full
                                data['inventory'].append(Item(lookup))  # if so add that item to inventory
                                data['equipped'][body] = ''  # remove item from slot

                        elif loc in self.inventory_slots and self.inventory_slots[loc]:
                            if pygame.mixer.get_init():
                                open_inventory_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'equip_item.flac'))
                                open_inventory_sound.play(0)

                            lookup = self.inventory_slots[loc]['lookup']
                            body = self.inventory_slots[loc]['body']

                            if data['equipped'][body]:  # check if equipment slot is full
                                data['inventory'].append(
                                    Item(data['equipped'][body].stats['lookup']))  # if so add that item to inventory

                            for item in data['inventory']:  # need to remove first occurence of item in data inventory
                                if item.stats['lookup'] == lookup:
                                    data['inventory'].remove(item)
                                    break;
                            data['equipped'][body] = Item(lookup)  # replace equipment slot

            with open(os.path.join(DATA_DIR, 'hero.yaml'), 'w') as file:
                try:
                    yaml.dump(data, file, default_flow_style=False)
                except yaml.YAMLError as exc:
                    print(exc)
            self.run()  # redraw inventory to update

    def add_item(self, type, item):
        self.inventory.append(Item(type, item))


class DialogBox:
    def __init__(self, origin, dialog, size=(400, 200)):

        self.dialog = dialog
        self.current_dialog = dialog[0]  # always begin dialog with first item value

        self.origin = origin
        self.size = size
        pygame.freetype.init()  # need to initialize font library before use
        self.font = pygame.freetype.Font(os.path.join(FONT_DIR, 'enchanted_land.otf'), 30)
        self.font.fgcolor = (0, 0, 0)

        self.dialog_window = Window(pygame.Surface(self.size, pygame.SRCALPHA), self.origin)
        self.image = pygame.image.load(os.path.join(DATA_DIR, 'tiles/textbox.png')).convert_alpha()
        self.dialog_window.surface.blit(self.image, (0, 0))
        self.option_button_list = []

    def get_text_container(self, text, start=(15, 0)):
        self.font.origin = True
        words = text.split(' ')
        width, height = self.dialog_window.surface.get_size()
        line_spacing = self.font.get_sized_height() + 2
        x, y = start[0], line_spacing + start[1]
        space = self.font.get_rect(' ')
        font_height = line_spacing

        container = pygame.Rect(start[0], start[1] + line_spacing, 0, 0)

        for word in words:
            bounds = self.font.get_rect(word)
            container.width += bounds.width
            if x + bounds.width + bounds.x >= width - 15:
                x, y = start[0], y + line_spacing + start[1]
                font_height += line_spacing
            if x + bounds.width + bounds.x >= width:
                raise ValueError("word too wide for the surface")
            if y + bounds.height - bounds.y >= height:
                raise ValueError("text to long for the surface")
            x += bounds.width + space.width
        container.height = font_height

        if container.width > width:
            container.width = width

        return container

    def remove_option_buttons(self):
        for button in self.option_button_list:
            self.dialog_window.remove_button(button)

    def handle_option_click(self, goto):
        for dialog in self.dialog:
            if dialog.attrib.get('id') == goto:
                self.current_dialog = dialog
        self.dialog_window.surface.blit(self.image, (0, 0))
        self.remove_option_buttons()
        self.render()

    def render(self):
        prompt = self.current_dialog.find('text').text
        rect = self.get_text_container(prompt)
        self.font.render_to(self.dialog_window.surface, (rect.x, rect.y), prompt)
        offset_y = 10

        options = self.current_dialog.find('options')

        if options:
            for option in options.findall('option'):
                bounds = self.get_text_container(option.text, (15, offset_y))
                option_button = TextButton(bounds,
                                           lambda action: self.handle_option_click(action.replace('dialog', '')), option,
                                           self.font)
                self.dialog_window.add_button(option_button, (bounds.x, bounds.y))
                self.option_button_list.append(option_button)
                offset_y += bounds.height + 10

        exit_image = pygame.image.load(os.path.join(IMAGE_DIR, 'exit.png'))
        exit_esc_image = pygame.image.load(os.path.join(IMAGE_DIR, 'exit_esc.png'))

        exit_button = ImageButton(pygame.Rect(0, 0, 18, 18), lambda: active_windows.remove_window(), exit_image,
                                  exit_esc_image)
        self.dialog_window.add_button(exit_button, (self.dialog_window.rect.width - 24, 10))

        active_windows.add_window(self.dialog_window)
