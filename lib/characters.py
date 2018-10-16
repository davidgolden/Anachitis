import pygame
import os

# Resource loading:
DATA_PY = os.path.abspath(os.path.dirname(__file__))
WALK_DIR = os.path.normpath(os.path.join(DATA_PY, '', 'sprites/png/walkcycle/'))

class Character(pygame.sprite.DirtySprite):
    def __init__(self, color=(0,0,0), width=10, height=10, max_health=10):
    # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.current_health = max_health
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([10, 10])
        self.image.fill(color)
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.max_health = max_health

    # def addHealth(self, x):
    #     if x < 0 and self.current_health + x > 0:
    #         self.current_health = self.current_health + x
    #     elif x < 0:
    #         self.current_health = 0
    #     elif x > 0 and self.current_health + x > self.max_health:
    #         self.current_health = self.max_health
    #     elif x > 0:
    #         self.current_health = self.current_health + self.max_health
    #     return self.current_health

class SpriteSheet:
    """ Class used to grab images out of a sprite sheet. """
    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width, height])

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0,0), (x,y, width, height)).convert()

        # Assuming black works as the transparent color
        image.set_colorkey((0,0,0))

        return image
