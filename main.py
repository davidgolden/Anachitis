import sys, pygame
from hero import Hero
pygame.init()

size = width, height = 1000, 1000
speed = [2, 6]

screen = pygame.display.set_mode(size)

hero = Hero()
hero.rect.x = 500
hero.rect.y = 500

# Track active sprites to later be able to track collides
# active_sprite_list = pygame.sprite.Group()
# active_sprite_list.add(hero)

clock = pygame.time.Clock()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                hero.go_east()
            elif pygame.key.get_pressed()[pygame.K_LEFT]:
                hero.go_west()
            elif pygame.key.get_pressed()[pygame.K_UP]:
                hero.go_north()
            elif pygame.key.get_pressed()[pygame.K_DOWN]:
                hero.go_south()
        elif event.type == pygame.KEYUP:
            if event.key in(pygame.K_DOWN, pygame.K_UP, pygame.K_LEFT, pygame.K_RIGHT):
                hero.stop_move()

    # Update the player.
    hero.update()
    screen.fill((0,128,0))
    hero.draw(screen)

    # Limit to 60 frames per second
    clock.tick(60)
    pygame.display.flip()
