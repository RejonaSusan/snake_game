import pygame, sys

pygame.init()
cell_size = 40
cell_num = 20
screen = pygame.display.set_mode((cell_size*cell_num,cell_size*cell_num))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((175, 215, 70))
    pygame.display.update()
    clock.tick(60)
 