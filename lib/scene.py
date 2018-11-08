import pygame, yaml, os

DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/'))

class Scene:
    def __init__(self, tile, quad):
        self.surface = pygame.Surface([500,500])
        self.quad = quad
        with open(os.path.join(DATA_DIR, 'scenes.yaml')) as file:
            data = yaml.load(file)
            self.id = f"{tile[0]}{tile[1]}"
            if f"{tile[0]}_{tile[1]}" in data.keys():
                self.data = data[f"{tile[0]}_{tile[1]}"]
                image = pygame.image.load(os.path.join(DATA_DIR, 'images/tiles/', f"{self.data['tile']}.png"))
                self.surface.blit(image, (0,0))
            else:
                self.surface.fill((0,255,0))

        self.rect = self.surface.get_rect()

    def get_quad(self):
        return self.quad
