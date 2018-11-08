import os, sys, pygame, yaml, math
from pygame.locals import *
from hero import Hero
from display import Inventory
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
            self.clock.tick(60) # Limit to 60 frames per second
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

        self.location = [0,0]

        self.__loadHero()

        tile_renderer = tilerender.Renderer(os.path.join(MAIN_DIR, "map.tmx"))
        self.map_surface, self.fringe_layer = tile_renderer.make_map(self.hero.rect.x, self.hero.rect.y)

        self.map_rect = self.map_surface.get_rect()

        self.blockers = tile_renderer.get_blockers()

        # self.mask = pygame.mask.from_surface(self.map_surface)
        # self.mask.draw(self.hero.mask, self.location)

        # pygame.mouse.set_visible(False)
        # self.cursor_img = pygame.image.load(os.path.join(DATA_DIR, 'cursor.png'))
        # self.cursor_rect = self.cursor_img.get_rect()

        # load starting coordinates
        # with open(os.path.join(DATA_DIR, 'hero.yaml')) as file:
        #     location = yaml.load(file)['location']
        #     self.coord = [int(i) for i in location.split(',')]

        # load correct tiles/scenes for starting coordinates

        # self.__loadScenes()

        self.active_sprite_list = pygame.sprite.Group()
        self.active_sprite_list.add(self.hero)

        self.active_window = False

    def __loadHero(self):
        self.hero = Hero() # initiate hero once
        self.inventory = Inventory()

        # place hero at center of screen
        self.hero.rect.x, self.hero.rect.y = self.screen_size[0] / 2, self.screen_size[1] / 2

        # at load, no go_to is set, so it is set to current position
        self.go_to_x = self.hero.rect.x
        self.go_to_y = self.hero.rect.y

    def __loadScenes(self, lazy=False):
        self.scene_list = []

        # load correct tiles
        # tX, tY, count = 1, 1, 1
        # qX, qY = (self.screen_width - self.hero.rect.x) + 250, (self.screen_height - self.hero.rect.y) + 250
        # for i in range(0,9):
        #     if lazy:
        #         for scene in self.scene_list:
        #             if f"{self.coord[0]}{self.coord[1]}" not in [ scene.id for scene in self.scene_list ]:
        #                 new_scene = Scene((self.coord[0] + tX, self.coord[1] + tY), [qX, qY])
        #                 self.scene_list[self.scene_list.index(scene)] = new_scene
        #     else:
        #         scene = Scene((self.coord[0] + tX, self.coord[1] + tY), [qX, qY])
        #         self.scene_list.append(scene)
        #     qX -=500
        #     tX -= 1
        #     if tX == -2:
        #         tX = 1
        #         tY -= 1
        #     if count % 3 == 0:
        #         qX = (self.screen_width - self.hero.rect.x) + 250
        #         qY -= 500
        #     count += 1
        #
        # for scene in self.scene_list:
        #     if pygame.Rect(scene.quad, (500,500)).contains(self.hero.rect):
        #         print(scene.quad)
        #         self.current_quad = [scene.quad[0], scene.quad[1]]

    def __checkEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.active_window == False and pygame.mouse.get_pressed()[0]:
                self.go_to_x, self.go_to_y = pygame.mouse.get_pos()
                self.go_to_x -= 32
                self.go_to_y -= 32

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

                if event.key == K_i:
                    if self.active_window == self.inventory.inventory_canvas:
                        self.active_window = False
                        # self.inventory.running = False
                    else:
                        self.active_window = self.inventory.inventory_canvas
                        self.inventory.run()
                    if pygame.mixer.get_init():
                        open_inventory_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'open_inventory.wav'))
                        open_inventory_sound.play(0)

                if event.key == K_s:
                    self.hero.save()

            # if event.type == MOUSEBUTTONDOWN and self.inventory.get_rect().collidepoint(pygame.mouse.get_pos()):
            #     self.inventory.handle_click(pygame.mouse.get_pos())
            #     self.hero.repaintSprite()

    def update_hero_position(self):
        t = 5
        if pygame.Rect(self.go_to_x, self.go_to_y, t, t).colliderect(pygame.Rect(self.hero.rect.x, self.hero.rect.y, t, t)):
            self.hero.stop_move()
        else:
            self.hero.stop = False
            dx = self.go_to_x - self.hero.rect.x # this is difference between mouse position and hero location
            dy = self.go_to_y - self.hero.rect.y
            angle = math.atan2(dy, dx)

            deg = round(math.degrees(angle))
            speed = 15

            cos = speed * math.cos(angle)
            sin = speed * math.sin(angle)

            self.location[0] += round(cos)
            self.location[1] += round(sin)

            self.blockers.update(-round(cos), -round(sin))

            self.go_to_x -= round(cos)
            self.go_to_y -= round(sin)

            self.hero.update(deg)

            if pygame.sprite.spritecollideany(self.hero, self.blockers):
                # right_sprite = pygame.sprite.spritecollideany(self.hero, self.blockers)
                # if pygame.sprite.collide_mask(right_sprite, self.hero.mask):
                    self.location[0] -= round(cos)
                    self.location[1] -= round(sin)
                    self.blockers.update(round(cos), round(sin))


    def __renderScreen(self):
        # self.cursor_rect.center = pygame.mouse.get_pos()

        self.screen.fill((0,128,0))

        # just iterate over animated tiles and demo them

        # tmx_map is a TiledMap object
        # tile_properties is a dictionary of all tile properties

        # self.active_sprite_list.update() # update active sprites

        self.update_hero_position()

        self.screen.blit(self.map_surface, (-self.location[0] + self.hero.rect.x, -self.location[1] + self.hero.rect.y))

        self.active_sprite_list.draw(self.screen)  # draw active sprites

        self.screen.blit(self.fringe_layer, (-self.location[0] + self.hero.rect.x, -self.location[1] + self.hero.rect.y))

        if self.active_window:
            self.screen.blit(self.active_window, (0,0))
        # self.screen.blit(self.cursor_img, self.cursor_rect)

        pygame.freetype.init() # need to initialize font library before use
        font = pygame.freetype.Font(os.path.join(DATA_DIR, 'fonts/enchanted_land.otf'),30)
        inventory = font.render(f"pos: {self.location}", (0,0,0), (255,221,138))
        self.screen.blit(inventory[0], (0,0))

        pygame.display.flip()

    # def __saveGame(self):
        # self.hero.save()

    # def __loadGame(self):
    #     self.hero.load()

    def __exitGame(self):
        # self.__saveGame()
        pygame.quit()
