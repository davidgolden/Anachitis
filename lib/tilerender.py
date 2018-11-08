import pygame as pg

import pytmx, pygame


class Blocker(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(0, 0, 0)):
        pygame.sprite.Sprite.__init__(self)

        self.mask = pygame.mask.Mask((int(width), int(height)))
        self.mask.fill()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = pygame.Rect(x, y, width, height)

    def update(self, x, y):
        self.rect.move_ip(x, y)


class Renderer(object):
    """
    This object renders tile maps from Tiled
    """

    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)

        # Make the scrolling layer
        screen_size = (1000, 800)
        # map_layer = pyscroll.BufferedRenderer(filename, screen_size)

        self.size = tm.width * tm.tilewidth, tm.height * tm.tileheight
        self.tmx_data = tm

        self.blockers_list = pygame.sprite.Group()

    def render(self, base, fringe, offset_x, offset_y):

        tw = self.tmx_data.tilewidth
        th = self.tmx_data.tileheight
        gt = self.tmx_data.get_tile_image_by_gid
        go = self.tmx_data.get_object_by_name

        if self.tmx_data.background_color:
            base.fill((128, 255, 30))
            fringe.fill(0,0,0,0)

        for layer in self.tmx_data.visible_layers:
            print(layer.name)
            if isinstance(layer, pytmx.TiledTileLayer):
                if layer.name == 'Fringe':
                    for x, y, gid in layer:
                        tile = gt(gid)
                        if tile:
                            fringe.blit(tile, (x * tw, y * th))
                # elif layer.name == 'Collision':
                #     for x, y, gid in layer:
                #         tile = gt(gid)
                #         if tile:
                #             blocker = Blocker(x * tw + offset_x, y * th + offset_y, tw, th)
                #             self.blockers_list.add(blocker)
                #             base.blit(tile, (x * tw, y * th))
                else:
                    for x, y, gid in layer:
                        tile = gt(gid)
                        if tile:
                            base.blit(tile, (x * tw, y * th))

            elif isinstance(layer, pytmx.TiledObjectGroup):
                for object in self.tmx_data.objects:
                    properties = object.__dict__
                    blocker = Blocker(properties['x'] + offset_x, properties['y'] + offset_y, properties['width'],
                                      properties['height'])
                    self.blockers_list.add(blocker)
            #
            #     if hasattr(object, 'points'):
            #         pygame.draw.lines(surface, (128, 128, 64),
            #                           object.closed, object.points, 3)

            # elif isinstance(layer, pytmx.TiledImageLayer):
            #     image = gt(layer.gid).convert_alpha()
            #     if image:
            #         surface.blit(image, (0, 0))

    def get_blockers(self):
        return self.blockers_list

    def make_map(self, offset_x, offset_y):
        base_layer = pg.Surface(self.size)
        fringe_layer = pg.Surface((self.size[0], self.size[1]), pg.SRCALPHA, 32)

        self.render(base_layer, fringe_layer, offset_x, offset_y)
        return base_layer, fringe_layer
