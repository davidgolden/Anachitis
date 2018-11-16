import os, sys, pygame, yaml, math
from pygame.locals import *
from hero import Hero
import character
# from display import Inventory, DialogBox, AllWindows
import display
import pytmx

import tilerender

DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/'))
SOUND_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/sounds/'))
MAIN_DIR = os.path.normpath(os.path.join(DATA_PY, '../'))


class Game():
    def __init__(self):
        self.__initGame()
        # self.__loadGame()
        while self.running:
            self.clock.tick(60)  # Limit to 60 frames per second
            self.__checkEvents()
            self.__renderScreen()
        self.__exitGame()

    def __initGame(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("David's Awesome Game")
        # load and play music
        # DATA_PY = os.path.abspath(os.path.dirname(__file__))
        pygame.mixer.init()
        # pygame.mixer.music.load(os.path.join(MUSIC_DIR, 'travel.mp3'))
        # pygame.mixer.music.play(-1, 0.0)
        self.running = True

        infoObject = pygame.display.Info()
        # self.screen_size = infoObject.current_w, infoObject.current_h
        self.screen_size = (1000, 800)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.location = [0, 0]

        # pygame.mouse.set_visible(False)
        # self.cursor_img = pygame.image.load(os.path.join(DATA_DIR, 'cursor.png'))
        # self.cursor_rect = self.cursor_img.get_rect()

        self.__loadHero()

        self.active_sprite_list = pygame.sprite.Group()

        self.__loadScenes()

        # self.active_windows = AllWindows()

        pygame.mouse.set_cursor(*pygame.cursors.tri_left)

    def __loadHero(self):
        self.hero = Hero()  # initiate hero once
        self.inventory = display.Inventory()

        # place hero at center of screen
        self.hero.rect.x, self.hero.rect.y = self.screen_size[0] / 2, self.screen_size[1] / 2

        # at load, no go_to is set, so it is set to current position
        self.go_to_x = self.hero.rect.x
        self.go_to_y = self.hero.rect.y

        self.hero_group = pygame.sprite.GroupSingle(self.hero)

    def __loadScenes(self, lazy=False):
        # load starting coordinates
        # with open(os.path.join(DATA_DIR, 'hero.yaml')) as file:
        #     location = yaml.load(file)['location']
        #     self.coord = [int(i) for i in location.split(',')]

        tile_renderer = tilerender.Renderer(os.path.join(MAIN_DIR, "map.tmx"))
        self.map_surface, self.fringe_layer = tile_renderer.make_map(self.hero.rect.x, self.hero.rect.y)

        self.map_rect = self.map_surface.get_rect()

        self.blockers = tile_renderer.get_blockers()

        sprite_data = {
            'name': 'Tim',
            'file_path': '/sprites/png/walkcycle/BODY_oldman.png',
            'static': True,
            'x': 0,
            'y': 144,
            'frames': 9,
            'location': (500, 500),
            'wander': pygame.Rect(550, 550, 100, 100),
            'dialog':
                {
                    1: {
                        'text': 'Hello, how are you?',
                        'prompt': True,
                        'options': [2, 3],
                    },
                    2: {
                        'text': 'Great!',
                        'prompt': False,
                        'goto': 4
                    },
                    3: {
                        'text': 'Horrible...',
                        'prompt': False,
                        'goto': 5
                    },
                    4: {
                        'text': 'What do you want to do today?',
                        'prompt': True,
                        'options': [6]
                    },
                    5: {
                        'text': 'Whats wrong?',
                        'prompt': True,
                        'options': [7]
                    },
                    6: {
                        'text': 'Kill stuff!',
                        'prompt': False,
                        'condition': 1 + 1 == 2,
                        'action': 'do stuff!'
                    },
                    7: {
                        'text': 'Im wounded!',
                        'prompt': False,
                    }

                },

        }

        wizard = character.NPC(sprite_data)
        self.active_sprite_list.add(wizard)

    def __checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            pos = pygame.mouse.get_pos()

            self.__check_clickables(pos, False)

            if pygame.mouse.get_pressed()[0]:
                if not self.__check_clickables(pos, True) and not len(display.active_windows):
                    self.go_to_x, self.go_to_y = pos
                    self.go_to_x -= 32
                    self.go_to_y -= 32

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

                # if event.key == K_i:
                #     if self.active_window == self.inventory.inventory_canvas:
                #         self.active_window = False
                #     else:
                #         self.active_window = self.inventory.inventory_canvas
                #         self.inventory.run()
                #     if pygame.mixer.get_init():
                #         open_inventory_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'open_inventory.wav'))
                #         open_inventory_sound.play(0)

                if event.key == K_s:
                    self.hero.save()

            # if event.type == MOUSEBUTTONDOWN and self.inventory.get_rect().collidepoint(pygame.mouse.get_pos()):
            #     self.inventory.handle_click(pygame.mouse.get_pos())
            #     self.hero.repaintSprite()

    def __check_clickables(self, pos, clicked=False):
        if clicked and len(display.active_windows):
            for window in display.active_windows.windows:
                if window.click_button(pos):
                    return True

        elif clicked:
            for sprite in self.active_sprite_list:
                if sprite.rect.collidepoint(pos):
                    return sprite.click_action()

        if not clicked and len(display.active_windows):
            for window in display.active_windows.windows:
                if window.collide_buttons(pos):
                    return True
                else:
                    window.esc_buttons()

        elif not clicked:
            for sprite in self.active_sprite_list:
                if sprite.collidepoint(pos):
                    sprite.highlighted = True
                else:
                    sprite.highlighted = False

        return False

    def update_hero_position(self):
        t = 5
        if pygame.Rect(self.go_to_x, self.go_to_y, t, t).colliderect(
                pygame.Rect(self.hero.rect.x, self.hero.rect.y, t, t)):
            self.hero.stop_move()
        else:
            self.hero.stop = False
            dx = self.go_to_x - self.hero.rect.x  # this is difference between mouse position and hero location
            dy = self.go_to_y - self.hero.rect.y
            angle = math.atan2(dy, dx)

            deg = round(math.degrees(angle))
            speed = 15

            cos = speed * math.cos(angle)
            sin = speed * math.sin(angle)

            self.location[0] += round(cos)
            self.location[1] += round(sin)

            self.blockers.update(-round(cos), -round(sin))
            self.active_sprite_list.update((-round(cos), -round(sin)))

            self.go_to_x -= round(cos)
            self.go_to_y -= round(sin)

            self.hero.update(deg)

            if pygame.sprite.spritecollideany(self.hero, self.blockers):
                self.location[0] -= round(cos)
                self.location[1] -= round(sin)
                self.blockers.update(round(cos), round(sin))

            if pygame.sprite.spritecollideany(self.hero, self.active_sprite_list):
                self.location[0] -= round(cos)
                self.location[1] -= round(sin)
                self.active_sprite_list.update((round(cos), round(sin)))

    def __renderScreen(self):
        self.screen.fill((0, 128, 0))

        self.update_hero_position()

        hero_location = (-self.location[0] + self.hero.rect.x, -self.location[1] + self.hero.rect.y)

        self.screen.blit(self.map_surface, hero_location)

        self.hero_group.draw(self.screen)

        self.active_sprite_list.update()
        self.active_sprite_list.draw(self.screen)  # draw active sprites

        self.screen.blit(self.fringe_layer, hero_location)

        display.active_windows.draw(self.screen)

        # pygame.freetype.init()  # need to initialize font library before use
        # font = pygame.freetype.Font(os.path.join(DATA_DIR, 'fonts/enchanted_land.otf'), 30)
        # inventory = font.render(f"pos: {self.location}", (0, 0, 0), (255, 221, 138))
        # self.screen.blit(inventory[0], (0, 0))

        pygame.display.flip()

    # def __saveGame(self):
    # self.hero.save()

    # def __loadGame(self):
    #     self.hero.load()

    def __exitGame(self):
        # self.__saveGame()
        pygame.quit()
