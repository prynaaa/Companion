import pygame

pygame.init()

screen = pygame.display.set_mode((200, 400), pygame.RESIZABLE) # pygame.NOFRAME once
clock = pygame.time.Clock()
title = 'Companion by Prynaaa'
pygame.display.set_caption(title)

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60) # 60 fps

    pygame.display.update()

pygame.quit()