import os, sys, pygame, yaml, display
from pygame.locals import *
from hero import Hero
from display import Inventory

DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/'))

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
        # MUSIC_DIR = os.path.normpath(os.path.join(DATA_PY, '', 'music/'))
        # pygame.mixer.music.load(os.path.join(MUSIC_DIR, 'travel.mp3'))
        # pygame.mixer.music.play(-1, 0.0)
        self.running = True
        self.fullscreen = False

        size = width, height = 1000, 1000
        if self.fullscreen:
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(size)

        self.hero = Hero() # initiate hero once
        self.hero.rect.x = pygame.display.get_surface().get_width() / 2
        self.hero.rect.y = pygame.display.get_surface().get_height() / 2
        self.active_sprite_list = pygame.sprite.Group()
        self.active_sprite_list.add(self.hero)

    def __checkEvents(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

                elif event.key in(K_RIGHT, K_LEFT, K_UP, K_DOWN):
                    self.hero.stop = False
                    if event.key == K_RIGHT:
                        self.hero.start_move('E')
                    elif event.key == K_LEFT:
                        self.hero.start_move('W')
                    elif event.key == K_UP:
                        self.hero.start_move('N')
                    elif event.key == K_DOWN:
                        self.hero.start_move('S')

                if event.key == K_i:
                    if display.windows['inventory']:
                        display.windows['inventory'] = False
                    else:
                        display.windows['inventory'] = self.hero.inventory.open()
                if event.key == K_q:
                    if display.windows['quests']:
                        display.windows['quests'] = False
                    else:
                        display.windows['quests'] = display.quests()
                if event.key == K_s:
                    self.hero.save()
                if event.key == K_t:
                    self.hero.add_item('plate_armor')

            if event.type == MOUSEBUTTONDOWN and self.hero.inventory.get_rect().collidepoint(pygame.mouse.get_pos()):
                self.hero.inventory.handle_click(pygame.mouse.get_pos())

            elif event.type == KEYUP:
                if event.key in (K_RIGHT, K_LEFT, K_UP, K_DOWN):
                    self.hero.stop_move()

    def __renderScreen(self):
        self.screen.fill((0,128,0))
        self.active_sprite_list.update() # update active sprites
        self.active_sprite_list.draw(self.screen) # draw active sprites
        self.screen.blits([ v for v in display.windows.values() if v ]) # render any open windows
        pygame.display.flip()

    def __saveGame(self):
        self.hero.save()

    # def __loadGame(self):
    #     self.hero.load()

    def __exitGame(self):
        self.__saveGame()
        pygame.quit()
