import pygame, yaml, os
import tilerender

DATA_PY = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.normpath(os.path.join(DATA_PY, '../data/'))

class Scene:
    def __init__(self):
        tile_renderer = tilerender.Renderer(os.path.join(MAIN_DIR, "map.tmx"))
        self.map_surface, self.fringe_layer = tile_renderer.make_map(self.hero.rect.x, self.hero.rect.y)

        self.map_rect = self.map_surface.get_rect()

        self.blockers = tile_renderer.get_blockers()
